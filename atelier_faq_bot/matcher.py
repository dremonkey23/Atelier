import re
from collections import Counter
from difflib import SequenceMatcher
from typing import Iterable

from .faq import FAQ, FAQEntry

_WORD_RE = re.compile(r"[a-z0-9][a-z0-9+._-]*", re.I)
_STOPWORDS = {
    "a", "an", "and", "are", "can", "do", "does", "for", "how", "i", "is", "it", "of", "on", "or", "the", "to", "what", "with",
}


def normalize(text: str) -> list[str]:
    return [
        m.group(0).lower()
        for m in _WORD_RE.finditer(text or "")
        if m.group(0).lower() not in _STOPWORDS
    ]


def score_entry(query: str, entry: FAQEntry) -> float:
    q_words = normalize(query)
    if not q_words:
        return 0.0
    q_counter = Counter(q_words)
    keyword_text = " ".join(entry.keywords).lower()
    haystack = f"{entry.topic} {entry.question} {' '.join(entry.keywords)}".lower()

    score = 0.0
    for word, count in q_counter.items():
        if word in entry.keywords:
            score += 4.0 * count
        elif word in keyword_text:
            score += 2.5 * count
        elif word in haystack:
            score += 1.5 * count

    score += 2.0 * SequenceMatcher(None, query.lower(), entry.question.lower()).ratio()
    if entry.topic in q_counter:
        score += 3.0
    return score


def find_best_answer(query: str, entries: Iterable[FAQEntry] = FAQ) -> tuple[FAQEntry | None, float]:
    scored = [(entry, score_entry(query, entry)) for entry in entries]
    if not scored:
        return None, 0.0
    best, score = max(scored, key=lambda item: item[1])
    if score < 2.0:
        return None, score
    return best, score


def format_answer(query: str) -> str:
    entry, _score = find_best_answer(query)
    if not entry:
        return (
            "I do not have a confident answer for that yet. Try asking about: what Atelier is, registering an agent, "
            "services, orders, payments, bounties, the API, x402, Solana/Base, or safety.\n\n"
            "Official docs: https://atelierai.xyz/docs"
        )
    return f"{entry.question}\n\n{entry.answer}\n\nSource: atelierai.xyz / docs"
