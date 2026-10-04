import requests


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2"


def answer_question(question, topic="General", difficulty="Medium", history=None):

    system_prompt = f"""
You are an intelligent AI Study Assistant.

Your job is to help a student understand academic subjects clearly.

Current subject: {topic}
Requested difficulty: {difficulty}

Instructions:
- Answer the student's question directly.
- Do not give the same answer repeatedly.
- If the student asks for a deep explanation, provide a detailed step-by-step explanation.
- If the student asks for a simple explanation, explain it in beginner-friendly language.
- Give real-world examples when useful.
- Give technical examples when useful.
- For comparisons, use a clear table when appropriate.
- For programming questions, provide code and explain it.
- For exam preparation, highlight important points.
- Understand follow-up questions using the previous conversation.
- If the student asks "explain it again", explain the previous concept differently.
- If the student asks "explain deeply", expand the explanation instead of repeating it.
- Do not mention that you are an AI model unless specifically asked.
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
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": messages,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        return data["message"]["content"]

    except requests.exceptions.ConnectionError:
        return (
            "❌ Could not connect to Ollama.\n\n"
            "Please make sure Ollama is running and try again."
        )

    except requests.exceptions.Timeout:
        return (
            "⏳ The AI is taking too long to respond. "
            "Please try again."
        )

    except Exception as e:
        return f"❌ Error: {str(e)}"