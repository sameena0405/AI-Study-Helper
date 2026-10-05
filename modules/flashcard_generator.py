import os
import requests
import json
import re
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


def generate_flashcards(
    text,
    count=5,
    difficulty="Medium"
):

    api_key = get_api_key()

    if not api_key:

        st.error(
            "❌ GEMINI_API_KEY is not configured."
        )

        return []

    prompt = f"""
You are an AI study assistant.

Create {count} useful study flashcards
from the following study material.

Difficulty: {difficulty}

Study material:

{text}

Requirements:

- Create exactly {count} flashcards.
- Each flashcard must test an important concept.
- Questions must be clear and meaningful.
- Answers must be concise but complete.
- Do not simply copy the entire sentence from the notes.
- Use information from the study material only.
- Avoid duplicate questions.
- Focus on concepts useful for exam revision.

Return ONLY valid JSON in exactly this format:

{{
    "flashcards": [
        {{
            "question": "Question here",
            "answer": "Answer here"
        }}
    ]
}}
"""

    for retry in range(3):

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

                timeout=120
            )

            # Temporary overload
            if response.status_code == 503:

                if retry < 2:

                    st.warning(
                        f"⏳ Gemini is busy. "
                        f"Retrying... ({retry + 1}/3)"
                    )

                    time.sleep(5)

                    continue

                st.error(
                    "❌ Gemini is currently busy. "
                    "Please try again later."
                )

                return []

            # Quota exceeded
            if response.status_code == 429:

                st.error(
                    "❌ Gemini API quota exceeded. "
                    "Please wait until your quota resets."
                )

                return []

            # Model unavailable
            if response.status_code == 404:

                st.error(
                    f"❌ Gemini model '{MODEL}' "
                    "is not available for this API."
                )

                return []

            # Other errors
            if response.status_code != 200:

                st.error(
                    f"❌ Gemini API Error "
                    f"({response.status_code}): "
                    f"{response.text}"
                )

                return []

            data = response.json()

            content = (
                data["candidates"][0]
                ["content"]["parts"][0]["text"]
            )

            result = json.loads(
                clean_json(content)
            )

            cards = result.get(
                "flashcards",
                []
            )

            if not isinstance(cards, list):

                return []

            valid_cards = []

            for card in cards:

                if not isinstance(card, dict):

                    continue

                if (
                    "question" not in card
                    or "answer" not in card
                ):

                    continue

                question = str(
                    card["question"]
                ).strip()

                answer = str(
                    card["answer"]
                ).strip()

                if not question or not answer:

                    continue

                valid_cards.append({

                    "question": question,

                    "answer": answer

                })

            return valid_cards[:count]

        except requests.exceptions.ConnectionError:

            if retry < 2:

                time.sleep(5)

                continue

            st.error(
                "❌ Could not connect to Gemini."
            )

            return []

        except requests.exceptions.Timeout:

            if retry < 2:

                time.sleep(5)

                continue

            st.error(
                "⏳ Gemini request timed out."
            )

            return []

        except json.JSONDecodeError:

            st.error(
                "❌ Gemini returned invalid JSON."
            )

            return []

        except Exception as e:

            st.error(
                f"❌ Flashcard generation error: {e}"
            )

            return []

    return []