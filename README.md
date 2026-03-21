# LLMAPI

This repository contains the current backend prototype for our student project.

The broader idea behind the project is to support students in Moodle-based learning environments by adding an external AI service that can:

- evaluate student answers against course material
- return structured feedback and identified learning gaps
- provide more consistent support across learning centers
- reduce dependency on locally available subject experts

At the moment, this repository only contains the Python API service for the evaluation part.

## Project Direction

Based on the project proposal and implementation roadmap, the intended architecture is:

1. A student submits an answer in Moodle.
2. Moodle sends the answer to this AI service.
3. This service retrieves relevant course content.
4. The LLM evaluates the answer using that course context.
5. The service returns structured feedback to Moodle.

So this repository is best understood as an external AI service that Moodle can call, not as a complete end-user application.

## Current Scope

The current codebase is a small FastAPI backend in [ai-service](/Users/majajurkowska/Desktop/Programming/LLMAPI/ai-service).

It currently provides:

- `GET /` as a health check
- `POST /evaluate` to evaluate a student's answer
- local course content lookup from `ai-service/knowledge_base/`
- an OpenAI-backed evaluation step using `OPENAI_API_KEY`

## Current Architecture

The main files are:

- [main.py](/Users/majajurkowska/Desktop/Programming/LLMAPI/ai-service/main.py): FastAPI entrypoint
- [models.py](/Users/majajurkowska/Desktop/Programming/LLMAPI/ai-service/models.py): request and response schemas
- [evaluator.py](/Users/majajurkowska/Desktop/Programming/LLMAPI/ai-service/evaluator.py): orchestration logic
- [retriever.py](/Users/majajurkowska/Desktop/Programming/LLMAPI/ai-service/retriever.py): simple course content retrieval
- [prompt_builder.py](/Users/majajurkowska/Desktop/Programming/LLMAPI/ai-service/prompt_builder.py): evaluation prompt construction
- [llm_client.py](/Users/majajurkowska/Desktop/Programming/LLMAPI/ai-service/llm_client.py): OpenAI API call
- [knowledge_base/course_overview.txt](/Users/majajurkowska/Desktop/Programming/LLMAPI/ai-service/knowledge_base/course_overview.txt): sample course content

Request flow:

1. `POST /evaluate` receives `user_id`, `question_id`, and `answer`.
2. The evaluator retrieves relevant course content.
3. A prompt is built from the answer and the retrieved content.
4. The OpenAI client sends the prompt to the model.
5. The response is parsed into a structured result with `indicator`, `feedback`, and `gaps`.

## Requirements

- Python 3
- `pip`
- an OpenAI API key

Because dependency versions are not pinned, Python 3.10 to 3.12 is the safest choice.

## Setup

Run these commands from the repository root:

```bash
cd ai-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Then set your API key in `ai-service/.env`:

```env
OPENAI_API_KEY=your_key_here
```

## How To Run

Start the backend from inside [ai-service](/Users/majajurkowska/Desktop/Programming/LLMAPI/ai-service):

```bash
cd ai-service
source .venv/bin/activate
uvicorn main:app --reload
```

Running from `ai-service` matters because:

- the code uses local imports like `from models import ...`
- the retriever expects `knowledge_base/` relative to the current working directory

If the service starts correctly, you should see Uvicorn serving on `http://127.0.0.1:8000`.

Available endpoints:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/docs`

## How To Test

Keep the server running in one terminal.

In a second terminal, run the health check:

```bash
curl http://127.0.0.1:8000/
```

Expected response:

```json
{"message":"AI Evaluation Service is running"}
```

Example evaluation request:

```bash
curl -X POST http://127.0.0.1:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "123",
    "question_id": "q1",
    "answer": "Stakeholder analysis helps identify actors in a situation, understand their interests, and evaluate how much influence they have."
  }'
```

Expected response shape:

```json
{
  "indicator": "green",
  "feedback": "Short feedback text",
  "gaps": ["gap 1", "gap 2"]
}
```

## Current Limitations

- there is no Moodle connector in this repository yet
- there is no frontend in this repository
- retrieval is currently simple keyword matching
- the knowledge base is currently just local text files
- dependency versions are not pinned
- there is no automated test suite yet

## Notes

- `ai-service/.env.example` is useful as a template and should not contain a real key
- `ai-service/.env` should stay local and should not be committed
- Python `__pycache__` files are local artifacts and should generally not be committed
