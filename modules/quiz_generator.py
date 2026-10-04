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

    api_key = get_api_key()

    if not api_key:
        st.error("❌ GROQ_API_KEY is not configured.")
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

        # Show API error details
        if response.status_code != 200:
            st.error(
                f"❌ Groq API Error "
                f"({response.status_code}): "
                f"{response.text}"
            )
            return None

        data = response.json()

        if "choices" not in data:
            st.error(
                f"❌ Unexpected Groq response: {data}"
            )
            return None

        content = data["choices"][0]["message"]["content"]

        if not content:
            st.error("❌ Groq returned an empty response.")
            return None

        content = clean_json(content)

        try:
            question = json.loads(content)
        except json.JSONDecodeError as e:
            st.error(
                f"❌ Invalid JSON returned by Groq: {e}\n\n"
                f"Response:\n{content}"
            )
            return None

        if not isinstance(question, dict):
            st.error("❌ AI response is not a JSON object.")
            return None

        if "question" not in question:
            st.error("❌ AI response is missing 'question'.")
            return None

        if "options" not in question:
            st.error("❌ AI response is missing 'options'.")
            return None

        if "answer" not in question:
            st.error("❌ AI response is missing 'answer'.")
            return None

        options = question["options"]

        if not isinstance(options, list):
            st.error("❌ AI options are not in list format.")
            return None

        if len(options) != 4:
            st.error(
                f"❌ AI generated {len(options)} options "
                f"instead of exactly 4."
            )
            return None

        options = [
            str(option).strip()
            for option in options
        ]

        # Make sure all 4 options are different
        if len(
            set(option.lower() for option in options)
        ) != 4:
            st.error("❌ AI generated duplicate options.")
            return None

        answer = str(
            question["answer"]
        ).strip()

        # Find exact correct option
        correct_answer = None

        for option in options:

            if option.lower() == answer.lower():

                correct_answer = option
                break

        if correct_answer is None:
            st.error(
                "❌ The correct answer does not match "
                "any of the generated options."
            )
            return None

        # Prevent duplicate questions
        previous_questions_lower = [
            q["question"].strip().lower()
            for q in previous_questions
        ]

        current_question = (
            str(question["question"]).strip()
        )

        if current_question.lower() in previous_questions_lower:
            st.warning(
                "⚠️ AI generated a duplicate question. "
                "Trying again..."
            )
            return None

        # Randomize options
        random.shuffle(options)

        return {
            "question": current_question,
            "options": options,
            "answer": correct_answer
        }

    except requests.exceptions.Timeout:
        st.error(
            "⏳ Groq request timed out. "
            "Please try generating the quiz again."
        )
        return None

    except requests.exceptions.ConnectionError as e:
        st.error(
            f"❌ Could not connect to Groq API: {e}"
        )
        return None

    except requests.exceptions.RequestException as e:
        st.error(
            f"❌ Request error: {e}"
        )
        return None

    except Exception as e:
        st.error(
            f"❌ Quiz generation error: {e}"
        )
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