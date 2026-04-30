print("SCRIPT STARTED")
import json
import time

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


def main(input_path, output_path):
    with open(input_path, "r") as f:
        data = json.load(f)

    results = []

    for item in data:
        start_time = time.time()

        query = item["query"]

        retrieved = retrieve(query, k=10)
        answers = generate_answer(query, retrieved)

        latency = time.time() - start_time

        results.append({
            "id": item["id"],
            "retrieved_standards": answers,
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
