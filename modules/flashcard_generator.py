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


def generate_flashcards(
    text,
    count=5,
    difficulty="Medium"
):

    prompt = f"""
You are an AI study assistant.

Create {count} useful study flashcards from the following study material.

Difficulty: {difficulty}

Study material:
{text}

Requirements:

- Create exactly {count} flashcards.
- Each flashcard must test an important concept.
- Questions must be clear and meaningful.
- Answers must be concise but complete.
- Do not simply copy the entire sentence from the notes.
- Use the information from the study material only.
- Avoid duplicate questions.
- Focus on concepts useful for exam revision.

Return ONLY valid JSON in exactly this format:

[
    {{
        "question": "Question here",
        "answer": "Answer here"
    }}
]
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

        cards = json.loads(content)

        if isinstance(cards, dict):

            if "flashcards" in cards:
                cards = cards["flashcards"]

            elif "cards" in cards:
                cards = cards["cards"]

            else:
                cards = [cards]

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

        return []

    except requests.exceptions.Timeout:

        return []

    except Exception:

        return []