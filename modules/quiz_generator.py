import os
import requests
import json
import re
import random
import streamlit as st


GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-20b"


def get_api_key():
    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        return os.environ.get("GROQ_API_KEY")


def clean_json(text):
    text = text.strip()
    text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)
    return text.strip()


def generate_one_question(
    subject,
    topic,
    difficulty,
    question_number,
    previous_questions
):

    api_key = get_api_key()

    if not api_key:
        return None

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
        "Option 1",
        "Option 2",
        "Option 3",
        "Option 4"
    ],
    "answer": "The exact correct option"
}}
"""

    try:

        response = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_completion_tokens": 1024,
                "response_format": {
                    "type": "json_object"
                }
            },
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        content = data["choices"][0]["message"]["content"]

        question = json.loads(clean_json(content))

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

        # Make sure all 4 options are different
        if len(
            set(option.lower() for option in options)
        ) != 4:
            return None

        answer = str(question["answer"]).strip()

        # Find the exact correct option
        correct_answer = None

        for option in options:

            if option.lower() == answer.lower():

                correct_answer = option
                break

        if correct_answer is None:
            return None

        # Prevent duplicate questions
        previous_questions_lower = [
            q["question"].strip().lower()
            for q in previous_questions
        ]

        if question["question"].strip().lower() in previous_questions_lower:
            return None

        # ==========================================
        # RANDOMIZE OPTIONS
        # ==========================================

        random.shuffle(options)

        # ==========================================
        # RETURN QUESTION
        # ==========================================

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