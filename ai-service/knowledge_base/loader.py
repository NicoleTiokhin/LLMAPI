import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROCESSED_DIR = BASE_DIR / "processed"

CONCEPTS_PATH = PROCESSED_DIR / "concepts.json"


def tokenize(text: str) -> set:
    return set(re.findall(r"[a-zA-Z]{3,}", text.lower()))


def load_concepts():
    if not CONCEPTS_PATH.exists():
        return []

    data = json.loads(CONCEPTS_PATH.read_text(encoding="utf-8"))

    concepts = []
    for doc in data.get("documents", []):
        for c in doc.get("concepts", []):
            concepts.append({
                "concept": c.get("concept", "").lower(),
                "definition": c.get("definition", "").lower(),
                "examples": c.get("examples", []),
                "topic": doc.get("title", "")
            })

    return concepts


def concept_score(answer, concept):
    answer_tokens = tokenize(answer)

    concept_tokens = tokenize(concept["concept"])
    def_tokens = tokenize(concept["definition"])

    score = 0
    score += len(answer_tokens & concept_tokens) * 5
    score += len(answer_tokens & def_tokens) * 2

    if concept["concept"] in answer.lower():
        score += 10

    return score


def retrieve_relevant_concepts(answer: str, top_k=5):
    concepts = load_concepts()

    scored = []
    for c in concepts:
        s = concept_score(answer, c)
        if s > 0:
            scored.append((s, c))

    scored.sort(reverse=True, key=lambda x: x[0])

    results = []
    seen = set()

    for score, c in scored:
        if c["concept"] in seen:
            continue

        seen.add(c["concept"])
        c["score"] = score
        results.append(c)

        if len(results) >= top_k:
            break

    return results


def format_concepts_for_prompt(concepts):
    if not concepts:
        return "No relevant course concepts found."

    lines = []

    for c in concepts:
        lines.append(f"Concept: {c['concept']}")
        lines.append(f"Definition: {c['definition']}")

        if c["examples"]:
            lines.append("Examples:")
            for ex in c["examples"]:
                lines.append(f"- {ex}")

        lines.append("")

    return "\n".join(lines)