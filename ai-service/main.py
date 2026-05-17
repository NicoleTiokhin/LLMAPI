from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from models import EvaluationRequest, EvaluationResponse
from evaluator import evaluate_answer

app = FastAPI(title="AI Evaluation Service")


@app.get("/")
def root():
    return {
        "message": "AI Evaluation Service is running"
    }


@app.post("/evaluate", response_model=EvaluationResponse)
def evaluate(request: EvaluationRequest):
    return evaluate_answer(request)


@app.post("/tool", response_class=HTMLResponse)
async def tool_ui(request: Request):

    form = await request.form()

    # -----------------------------
    # Moodle / LTI user data
    # -----------------------------
    user_id = form.get(
        "user_id",
        "unknown_user"
    )

    full_name = form.get(
        "lis_person_name_full",
        "Unknown User"
    )

    email = form.get(
        "lis_person_contact_email_primary",
        "unknown@email.com"
    )

    # -----------------------------
    # Dynamic Moodle question
    # -----------------------------
    question_id = form.get(
        "question_id",
        "default_question"
    )

    question_text = form.get(
        "custom_question",
        "Explain Lean Startup principles."
    )

    # -----------------------------
    # HTML UI
    # -----------------------------
    return f"""
<!doctype html>
<html>
<head>
    <title>AI Feedback Tool</title>

    <style>

        body {{
            font-family: Arial;
            margin: 2rem;
            max-width: 900px;
        }}

        textarea {{
            width: 100%;
            height: 180px;
            margin-top: 10px;
            padding: 10px;
        }}

        button {{
            margin-top: 15px;
            padding: 10px 20px;
            cursor: pointer;
        }}

        .result {{
            margin-top: 30px;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 8px;
        }}

        .green {{
            background-color: #d4edda;
        }}

        .yellow {{
            background-color: #fff3cd;
        }}

        .red {{
            background-color: #f8d7da;
        }}

        ul {{
            margin-top: 10px;
        }}

        .feedback-section {{
            margin-top: 20px;
        }}

    </style>
</head>

<body>

<h2>AI Feedback Tool</h2>

<p>
<b>User:</b> {full_name}
</p>

<p>
<b>Email:</b> {email}
</p>

<p>
<b>Question:</b>
</p>

<p>
{question_text}
</p>

<textarea
    id="answer"
    placeholder="Enter your answer here..."
></textarea>

<br>

<button onclick="submitAnswer()">
    Submit Answer
</button>

<div id="result" class="result" style="display:none;"></div>

<script>

const USER_ID = "{user_id}";
const QUESTION_ID = "{question_id}";
const QUESTION_TEXT = `{question_text}`;

async function submitAnswer() {{

    const answer = document.getElementById("answer").value;

    if (!answer) {{
        alert("Please enter an answer.");
        return;
    }}

    const response = await fetch("/evaluate", {{

        method: "POST",

        headers: {{
            "Content-Type": "application/json"
        }},

        body: JSON.stringify({{
            user_id: USER_ID,
            question_id: QUESTION_ID,
            question_text: QUESTION_TEXT,
            answer: answer
        }})
    }});

    const data = await response.json();

    const resultDiv = document.getElementById("result");

    resultDiv.style.display = "block";

    resultDiv.className = "result " + data.indicator;

    let gapsHtml = "";

    if (data.gaps && data.gaps.length > 0) {{

        gapsHtml = `
            <div class="feedback-section">

                <h4>Missing / Weak Concepts</h4>

                <ul>
                    ${{data.gaps.map(g => `<li>${{g}}</li>`).join("")}}
                </ul>

            </div>
        `;
    }}

    resultDiv.innerHTML = `

        <h3>
            Indicator: ${{data.indicator.toUpperCase()}}
        </h3>

        <div class="feedback-section">

            <h4>General Feedback</h4>

            <p>
                ${{data.general_feedback}}
            </p>

        </div>

        <div class="feedback-section">

            <h4>Course Concept Feedback</h4>

            <p>
                ${{data.concept_feedback}}
            </p>

        </div>

        ${{gapsHtml}}
    `;
}}

</script>

</body>
</html>
"""


@app.get("/tool-test", response_class=HTMLResponse)
async def tool_test():

    class FakeRequest:

        async def form(self):
            return {
                "user_id": "student_1",
                "lis_person_name_full": "Nicole",
                "lis_person_contact_email_primary": "test@example.com",
                "question_id": "lean_q1",
                "custom_question": "Explain validated learning in Lean Startup."
            }

    return await tool_ui(FakeRequest())