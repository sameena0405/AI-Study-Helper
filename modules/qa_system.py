import os
import requests
import time
import random
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


def answer_question(
    question,
    topic="General",
    difficulty="Medium",
    history=None
):

    api_key = get_api_key()

    if not api_key:

        return (
            "❌ GEMINI_API_KEY is not configured."
        )

    prompt = f"""
You are an intelligent AI Study Assistant.

Subject: {topic}

Difficulty: {difficulty}

Instructions:

- Answer the student's question directly.
- Explain concepts clearly and accurately.
- Use simple language when appropriate.
- Give step-by-step explanations for difficult topics.
- Give examples when useful.
- For programming questions, provide correct code and explanation.
- For comparisons, use a table when useful.
- For exam preparation, highlight important points.
- Do not repeat the same answer unnecessarily.

Conversation history:

{history if history else "No previous conversation."}

Student question:

{question}
"""

    # Maximum 3 attempts
    for attempt in range(3):

        try:

            response = requests.post(
                f"{GEMINI_URL}/{MODEL}:generateContent",
                params={"key": api_key},
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
                    ]
                },
                timeout=120
            )


            # -----------------------------
            # Gemini temporarily overloaded
            # -----------------------------

            if response.status_code == 503:

                if attempt < 2:

                    delay = (
                        10 * (2 ** attempt)
                        + random.uniform(0, 3)
                    )

                    st.warning(
                        f"⏳ Gemini is temporarily busy. "
                        f"Retrying in {delay:.0f} seconds..."
                    )

                    time.sleep(delay)

                    continue

                return (
                    "❌ Gemini is temporarily busy right now. "
                    "Please wait a little and try again."
                )


            # -----------------------------
            # Quota exceeded
            # -----------------------------

            if response.status_code == 429:

                return (
                    "❌ Gemini API quota exceeded. "
                    "Please wait until your quota resets."
                )


            # -----------------------------
            # Model unavailable
            # -----------------------------

            if response.status_code == 404:

                return (
                    f"❌ Gemini model '{MODEL}' "
                    "is not available for this API."
                )


            # -----------------------------
            # Other API errors
            # -----------------------------

            if response.status_code != 200:

                return (
                    f"❌ Gemini API Error "
                    f"({response.status_code}): "
                    f"{response.text}"
                )


            # -----------------------------
            # Successful response
            # -----------------------------

            data = response.json()

            if "candidates" not in data:

                return (
                    "❌ Gemini did not return a response."
                )

            return (
                data["candidates"][0]
                ["content"]["parts"][0]["text"]
            )


        except requests.exceptions.Timeout:

            if attempt < 2:

                delay = (
                    10 * (2 ** attempt)
                )

                st.warning(
                    f"⏳ Request timed out. "
                    f"Retrying in {delay} seconds..."
                )

                time.sleep(delay)

                continue

            return (
                "⏳ Gemini request timed out. "
                "Please try again later."
            )


        except requests.exceptions.ConnectionError:

            if attempt < 2:

                delay = (
                    10 * (2 ** attempt)
                )

                st.warning(
                    f"🌐 Connection problem. "
                    f"Retrying in {delay} seconds..."
                )

                time.sleep(delay)

                continue

            return (
                "❌ Could not connect to Gemini. "
                "Please check your internet connection."
            )


        except requests.exceptions.RequestException as e:

            return (
                f"❌ Gemini connection error: {e}"
            )


        except (KeyError, IndexError):

            return (
                "❌ Unexpected response received "
                "from Gemini."
            )


        except Exception as e:

            return f"❌ Error: {str(e)}"


    return (
        "❌ Unable to get a response from Gemini."
    )