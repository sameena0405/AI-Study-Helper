import re
from collections import Counter


def summarize_text(text, sentences_count=3):

    if not text or not text.strip():
        return ""

    # Split text into sentences
    sentences = re.split(
        r'(?<=[.!?])\s+',
        text.strip()
    )

    sentences = [
        sentence.strip()
        for sentence in sentences
        if len(sentence.strip().split()) >= 5
    ]

    if len(sentences) <= sentences_count:
        return " ".join(sentences)

    # Remove common words
    stop_words = {
        "the", "is", "are", "was", "were",
        "a", "an", "and", "or", "but",
        "of", "to", "in", "on", "for",
        "with", "as", "by", "from", "at",
        "this", "that", "these", "those",
        "it", "its", "be", "been", "has",
        "have", "had", "can", "will", "which",
        "about", "into", "than", "their",
        "they", "them", "we", "you", "your"
    }

    words = re.findall(
        r'\b[a-zA-Z]{3,}\b',
        text.lower()
    )

    word_frequency = Counter(
        word
        for word in words
        if word not in stop_words
    )

    # Score sentences
    scores = []

    for index, sentence in enumerate(sentences):

        sentence_words = re.findall(
            r'\b[a-zA-Z]{3,}\b',
            sentence.lower()
        )

        score = sum(
            word_frequency[word]
            for word in sentence_words
            if word not in stop_words
        )

        scores.append(
            (score, index, sentence)
        )

    # Select important sentences
    best_sentences = sorted(
        scores,
        reverse=True
    )[:sentences_count]

    # Keep original order
    best_sentences.sort(
        key=lambda x: x[1]
    )

    return " ".join(
        sentence
        for _, _, sentence in best_sentences
    )