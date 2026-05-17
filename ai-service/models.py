from pydantic import BaseModel
from typing import List


class EvaluationRequest(BaseModel):
    user_id: str
    question_id: str
    question_text: str
    answer: str


class EvaluationResponse(BaseModel):
    indicator: str
    general_feedback: str
    concept_feedback: str
    gaps: List[str]