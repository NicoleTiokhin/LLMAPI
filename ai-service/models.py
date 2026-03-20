from pydantic import BaseModel
from typing import List


class EvaluationRequest(BaseModel):
    user_id: str
    question_id: str
    answer: str


class EvaluationResponse(BaseModel):
    indicator: str
    feedback: str
    gaps: List[str]