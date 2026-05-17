from llm_client import call_llm

prompt = 'Return ONLY this JSON: {"test": "ok"}'

response = call_llm(prompt)

print("\n=== RAW RESPONSE ===")
print(response)