import os
import json
from llm_client import call_llm

RAW_PATH = "knowledge_base/raw"
CACHE_PATH = "knowledge_base/cache/principles.json"


# -----------------------------
# Load raw course files
# -----------------------------
def load_raw_files():
    texts = []

    for filename in os.listdir(RAW_PATH):
        if filename.endswith(".txt"):
            with open(os.path.join(RAW_PATH, filename), "r", encoding="utf-8") as f:
                texts.append(f.read())

    return texts


# -----------------------------
# Generate principles via LLM
# -----------------------------
def generate_principles():
    texts = load_raw_files()

    if not texts:
        print("⚠️ No raw files found.")
        return []

    combined = "\n\n".join(texts)

    # 🚨 LIMIT SIZE (VERY IMPORTANT)
    combined = combined[:6000]

    print(f"\n📏 Prompt size: {len(combined)} characters")

    prompt = f"""
You are an expert in Lean Startup methodology.

Extract the key principles from the following text.

Return ONLY valid JSON (no explanation, no markdown):

[
  {{
    "name": "Principle name",
    "keywords": ["keyword1", "keyword2"],
    "description": "Short explanation"
  }}
]

Text:
{combined}
"""

    try:
        response = call_llm(prompt)

        print("\n🧠 RAW LLM RESPONSE:")
        print(response)

        principles = json.loads(response)

        # ✅ Validate structure
        if not isinstance(principles, list):
            raise ValueError("Invalid format: not a list")

        return principles

    except Exception as e:
        print("❌ Extraction failed:", str(e))
        return []


# -----------------------------
# Cache handling
# -----------------------------
def get_principles():
    os.makedirs("knowledge_base/cache", exist_ok=True)

    if os.path.exists(CACHE_PATH):
        print("📦 Loading cached principles...")
        with open(CACHE_PATH, "r") as f:
            return json.load(f)

    print("⚙️ Generating new principles...")
    principles = generate_principles()

    with open(CACHE_PATH, "w") as f:
        json.dump(principles, f, indent=2)

    return principles


# -----------------------------
# Run manually
# -----------------------------
if __name__ == "__main__":
    print("🔄 Starting extraction...")

    principles = generate_principles()

    print(f"\n✅ Extracted {len(principles)} principles")

    os.makedirs("knowledge_base/processed", exist_ok=True)

    with open("knowledge_base/processed/concepts.json", "w") as f:
        json.dump({
            "documents": [
                {
                    "title": "Lean Startup",
                    "concepts": principles
                }
            ]
        }, f, indent=2)

    print("💾 Saved to knowledge_base/processed/concepts.json")