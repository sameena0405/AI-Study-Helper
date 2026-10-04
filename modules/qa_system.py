import os
import requests
import streamlit as st

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-20b"


def get_api_key():
    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        return os.environ.get("GROQ_API_KEY")


def answer_question(question, topic="General", difficulty="Medium", history=None):

    api_key = get_api_key()

    if not api_key:
        return "❌ GROQ_API_KEY is not configured."

    system_prompt = f"""
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
- Understand follow-up questions using conversation history.
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    if history:
        messages.extend(history)

    messages.append({
        "role": "user",
        "content": question
    })

    try:
        response = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 2048
            },
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]

    except requests.exceptions.Timeout:
        return "⏳ AI is taking too long to respond. Please try again."

    except requests.exceptions.RequestException as e:
        return f"❌ Groq API Error: {str(e)}"

    except Exception as e:
        return f"❌ Error: {str(e)}"