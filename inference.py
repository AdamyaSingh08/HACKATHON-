print("SCRIPT STARTED")
import json
import time
import re

from src.parser import extract_text, split_standards
from src.embedder import create_embeddings
from src.retriever import build_index, retrieve
from src.rag import generate_answer

# Load once (IMPORTANT for latency)
print("Loading BIS data...")

text = extract_text("data/bis.pdf")
standards = split_standards(text)

print(f"Total standards found: {len(standards)}")

embeddings = create_embeddings(standards)
build_index(standards, embeddings)

print("Index built successfully!")


# ✅ keyword scoring (keep yours)
def keyword_score(query, standard_id):
    return sum(1 for word in query.lower().split() if word in standard_id.lower())


# 🔥 NEW: extract FULL standard ID with year
def extract_full_id(ans):
    text = ans.get("reason", "")

    match = re.search(
        r"(IS\s*\d{1,5}(?:\s*\(Part\s*\d+\))?\s*:\s*\d{4})",
        text
    )

    if match:
        return re.sub(r"\s+", " ", match.group()).strip()

    # fallback if reason fails
    return ans.get("standard_id", "")


def main(input_path, output_path):
    with open(input_path, "r") as f:
        data = json.load(f)

    results = []

    for item in data:
        start_time = time.time()

        query = item["query"]

        retrieved = retrieve(query, k=10)
        answers = generate_answer(query, retrieved)

        # 🔥 FIXED: use full ID extraction
        retrieved_standards = [extract_full_id(ans) for ans in answers if ans]

        # remove duplicates
        retrieved_standards = list(dict.fromkeys(retrieved_standards))

        # re-rank
        retrieved_standards = sorted(
            retrieved_standards,
            key=lambda x: keyword_score(query, x),
            reverse=True
        )

        # limit to top 5
        retrieved_standards = retrieved_standards[:5]

        latency = time.time() - start_time

        results.append({
            "id": item["id"],
            "retrieved_standards": retrieved_standards,
            "latency_seconds": round(latency, 3)
        })

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print("Output saved to:", output_path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)

    args = parser.parse_args()

    main(args.input, args.output)