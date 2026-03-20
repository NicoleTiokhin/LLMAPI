import json
from models import EvaluationRequest
from retriever import retrieve_relevant_content
from prompt_builder import build_prompt
from llm_client import call_llm


def evaluate_answer(request: EvaluationRequest):
    answer = request.answer

    context = retrieve_relevant_content(answer)
    prompt = build_prompt(answer, context)
    raw_response = call_llm(prompt)

    try:
        result = json.loads(raw_response)
    except json.JSONDecodeError:
        result = {
            "indicator": "yellow",
            "feedback": "The AI returned an invalid format. Please review the answer manually.",
            "gaps": ["response formatting issue"]
        }

    if "indicator" not in result:
        result["indicator"] = "yellow"

    if "feedback" not in result:
        result["feedback"] = "No feedback was returned."

    if "gaps" not in result or not isinstance(result["gaps"], list):
        result["gaps"] = ["no structured gap analysis returned"]

    return result