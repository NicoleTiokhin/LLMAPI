from fastapi import FastAPI
from models import EvaluationRequest, EvaluationResponse
from evaluator import evaluate_answer

app = FastAPI(title="AI Evaluation Service")


@app.get("/")
def root():
    return {"message": "AI Evaluation Service is running"}


@app.post("/evaluate", response_model=EvaluationResponse)
def evaluate(request: EvaluationRequest):
    return evaluate_answer(request)