import os
import requests
import json
import re
import random
import time
import streamlit as st


MODEL = "gemini-3.8-flash"

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models"
)


def get_api_key():

    try:
        return st.secrets["GEMINI_API_KEY"]

    except Exception:
        return os.environ.get("GEMINI_API_KEY")


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


def generate_quiz(
    subject,
    topic,
    difficulty="Medium",
    count=5
):

    # Reset error states
    st.session_state.quiz_quota_exceeded = False
    st.session_state.quiz_service_busy = False
    st.session_state.quiz_generation_error = False

    api_key = get_api_key()

    if not api_key:

        st.session_state.quiz_generation_error = True

        st.error(
            "❌ GEMINI_API_KEY is not configured."
        )

        return []


    prompt = f"""
Create a quiz for a student.

Subject: {subject}
Topic: {topic}
Difficulty: {difficulty}

Create exactly {count} multiple-choice questions.

Rules:

- Every question must be directly related to the topic.
- Each question must have exactly 4 options.
- Only one option must be correct.
- All options must be plausible.
- Do not repeat questions.
- The correct answer must exactly match one option.
- Questions should test understanding.

Return ONLY valid JSON.

Use exactly this format:

{{
  "questions": [
    {{
      "question": "Question",
      "options": [
        "Option 1",
        "Option 2",
        "Option 3",
        "Option 4"
      ],
      "answer": "Correct option"
    }}
  ]
}}
"""


    # Try at most twice for temporary errors
    for retry in range(2):

        try:

            response = requests.post(

                f"{GEMINI_URL}/{MODEL}:generateContent",

                params={
                    "key": api_key
                },

                headers={
                    "Content-Type": "application/json"
                },

                json={

                    "contents": [
                        {
                            "parts": [
                                {
                                    "text": prompt
                                }
                            ]
                        }
                    ],

                    "generationConfig": {
                        "responseMimeType":
                        "application/json"
                    }

                },

                timeout=180
            )


            # --------------------------------
            # Quota exceeded
            # --------------------------------

            if response.status_code == 429:

                st.session_state.quiz_quota_exceeded = True

                return []


            # --------------------------------
            # Gemini temporarily unavailable
            # --------------------------------

            if response.status_code == 503:

                if retry == 0:

                    time.sleep(10)

                    continue

                st.session_state.quiz_service_busy = True

                return []


            # --------------------------------
            # Model unavailable
            # --------------------------------

            if response.status_code == 404:

                st.session_state.quiz_generation_error = True

                st.error(
                    f"❌ Gemini model '{MODEL}' "
                    "is not available for this API."
                )

                return []


            # --------------------------------
            # Other API errors
            # --------------------------------

            if response.status_code != 200:

                st.session_state.quiz_generation_error = True

                st.error(
                    f"❌ Gemini API Error "
                    f"({response.status_code})"
                )

                return []


            # --------------------------------
            # Read Gemini response
            # --------------------------------

            data = response.json()

            content = (
                data["candidates"][0]
                ["content"]["parts"][0]["text"]
            )


            result = json.loads(
                clean_json(content)
            )


            questions = result.get(
                "questions",
                []
            )


            if not isinstance(
                questions,
                list
            ):

                st.session_state.quiz_generation_error = True

                return []


            quiz = []


            # --------------------------------
            # Validate every question
            # --------------------------------

            for item in questions:

                if not isinstance(
                    item,
                    dict
                ):
                    continue


                if not all(
                    key in item
                    for key in [
                        "question",
                        "options",
                        "answer"
                    ]
                ):
                    continue


                question = str(
                    item["question"]
                ).strip()


                options = item["options"]


                answer = str(
                    item["answer"]
                ).strip()


                if not isinstance(
                    options,
                    list
                ):
                    continue


                if len(options) != 4:
                    continue


                options = [
                    str(option).strip()
                    for option in options
                ]


                # No duplicate options
                if len(
                    set(
                        option.lower()
                        for option in options
                    )
                ) != 4:
                    continue


                # Answer must match an option
                correct_answer = next(

                    (
                        option
                        for option in options

                        if option.lower()
                        == answer.lower()
                    ),

                    None
                )


                if correct_answer is None:
                    continue


                if not question:
                    continue


                # No duplicate questions
                if any(
                    question.lower()
                    == old["question"].lower()

                    for old in quiz
                ):
                    continue


                random.shuffle(options)


                quiz.append({

                    "question":
                    question,

                    "options":
                    options,

                    "answer":
                    correct_answer

                })


            # --------------------------------
            # Check result
            # --------------------------------

            if len(quiz) == count:

                return quiz


            # Gemini returned fewer valid questions
            if len(quiz) > 0:

                st.session_state.quiz_generation_error = True

                return []


            st.session_state.quiz_generation_error = True

            return []


        # --------------------------------
        # Timeout
        # --------------------------------

        except requests.exceptions.Timeout:

            if retry == 0:

                time.sleep(10)

                continue

            st.session_state.quiz_generation_error = True

            return []


        # --------------------------------
        # Connection error
        # --------------------------------

        except requests.exceptions.ConnectionError:

            if retry == 0:

                time.sleep(10)

                continue

            st.session_state.quiz_generation_error = True

            return []


        # --------------------------------
        # Invalid JSON
        # --------------------------------

        except json.JSONDecodeError:

            st.session_state.quiz_generation_error = True

            return []


        # --------------------------------
        # Unexpected response
        # --------------------------------

        except (KeyError, IndexError):

            st.session_state.quiz_generation_error = True

            return []


        # --------------------------------
        # Other errors
        # --------------------------------

        except Exception as e:

            st.session_state.quiz_generation_error = True

            st.error(
                f"❌ Quiz generation error: {e}"
            )

            return []


    return []