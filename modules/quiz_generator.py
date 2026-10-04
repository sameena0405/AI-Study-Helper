import requests
import json
import re


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2"


def clean_json(text):
    text = text.strip()

    text = re.sub(
        r"```json",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"```",
        "",
        text
    )

    return text.strip()


def generate_one_question(
    subject,
    topic,
    difficulty,
    question_number,
    previous_questions
):

    previous = "\n".join(
        f"- {q['question']}"
        for q in previous_questions
    )

    prompt = f"""
You are an AI quiz generator for students.

Subject: {subject}
Topic: {topic}
Difficulty: {difficulty}

Create ONE high-quality multiple-choice question.

Requirements:
- The question must be directly related to the subject and topic.
- Test understanding of the topic.
- Do not create fill-in-the-blank questions.
- Give exactly 4 options.
- Only ONE option must be correct.
- All options must be plausible.
- Do not repeat previous questions.
- Keep the question suitable for the selected difficulty.

Previous questions:
{previous if previous else "None"}

Return ONLY valid JSON in exactly this format:

{{
    "question": "Your question here",
    "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
    ],
    "answer": "The exact correct option"
}}
"""

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "stream": False,
                "format": "json"
            },
            timeout=180
        )

        response.raise_for_status()

        data = response.json()

        content = data["message"]["content"]

        content = clean_json(content)

        question = json.loads(content)

        if isinstance(question, list):

            if not question:
                return None

            question = question[0]

        if not isinstance(question, dict):
            return None

        if "question" not in question:
            return None

        if "options" not in question:
            return None

        if "answer" not in question:
            return None

        options = question["options"]

        if not isinstance(options, list):
            return None

        if len(options) != 4:
            return None

        options = [
            str(option).strip()
            for option in options
        ]

        # Check duplicate options
        if len(
            set(option.lower() for option in options)
        ) != 4:
            return None

        answer = str(
            question["answer"]
        ).strip()

        # Match answer with one of the options
        correct_answer = None

        for option in options:

            if option.lower() == answer.lower():

                correct_answer = option
                break

        if correct_answer is None:
            return None

        # Check duplicate questions
        previous_questions_lower = [
            q["question"].strip().lower()
            for q in previous_questions
        ]

        if (
            question["question"].strip().lower()
            in previous_questions_lower
        ):
            return None

        return {
            "question": question["question"].strip(),
            "options": options,
            "answer": correct_answer
        }

    except Exception:
        return None


def generate_quiz(
    subject,
    topic,
    difficulty="Medium",
    count=5
):

    quiz = []

    for i in range(1, count + 1):

        # Try up to 4 times for each question
        for attempt in range(4):

            question = generate_one_question(
                subject,
                topic,
                difficulty,
                i,
                quiz
            )

            if question is not None:

                quiz.append(question)

                break

    return quiz