def build_prompt(answer: str, context: str) -> str:
    return f"""
You are an educational AI evaluator.

Your job is to evaluate the student's answer based only on the provided course content.

COURSE CONTENT:
{context}

STUDENT ANSWER:
{answer}

Evaluation criteria:
1. Does the answer use course concepts correctly?
2. Does the answer explain the reasoning clearly?
3. Does the answer connect concepts to the case or situation?
4. Which important concepts are missing?

Indicator rules:
- green = strong understanding
- yellow = partial understanding
- red = weak understanding

Important rules:
- Use only the provided course content
- Do not rely on outside knowledge
- Be fair and concise
- Return only valid JSON

Return this exact JSON structure:
{{
  "indicator": "green or yellow or red",
  "feedback": "short feedback for the student",
  "gaps": ["gap 1", "gap 2"]
}}
"""