import json
import re

from models import EvaluationRequest
from prompt_builder import build_prompt
from llm_client import call_llm

from knowledge_base.loader import (
    retrieve_relevant_concepts,
    format_concepts_for_prompt
)


def tokenize(text: str) -> set:
    return set(re.findall(r"[a-zA-Z]{3,}", text.lower()))


def analyze_answer(answer: str, concepts):
    answer_tokens = tokenize(answer)

    keyword_hits = 0
    phrase_hits = 0

    for c in concepts:
        concept_tokens = tokenize(c["concept"])
        def_tokens = tokenize(c["definition"])

        keyword_hits += len(answer_tokens & concept_tokens)
        keyword_hits += len(answer_tokens & def_tokens)

        if c["concept"].lower() in answer.lower():
            phrase_hits += 1

    return {
        "keyword_hits": keyword_hits,
        "phrase_hits": phrase_hits
    }


def evaluate_answer(request: EvaluationRequest):

    question_id = request.question_id
    question_text = request.question_text
    answer = request.answer.strip()

    # Question decides which course concepts are relevant
    search_query = question_text

    relevant_concepts = retrieve_relevant_concepts(
        search_query,
        top_k=5
    )

    knowledge_context = format_concepts_for_prompt(
        relevant_concepts
    )

    analysis = analyze_answer(
        answer,
        relevant_concepts
    )

    prompt = build_prompt(
        question_text=question_text,
        answer=answer,
        context=knowledge_context,
        analysis=analysis
    )

    raw_response = call_llm(prompt)

    try:
        result = json.loads(raw_response)

    except json.JSONDecodeError:
        result = {
            "indicator": "yellow",
            "general_feedback": "The AI returned an invalid format. Please review manually.",
            "concept_feedback": "Could not evaluate concept usage because the response format was invalid.",
            "gaps": ["response formatting issue"]
        }

    if "indicator" not in result:
        result["indicator"] = "yellow"

    if "general_feedback" not in result:
        result["general_feedback"] = "No general feedback returned."

    if "concept_feedback" not in result:
        result["concept_feedback"] = "No concept feedback returned."

    if "gaps" not in result or not isinstance(result["gaps"], list):
        result["gaps"] = ["no structured gap analysis"]

    return result