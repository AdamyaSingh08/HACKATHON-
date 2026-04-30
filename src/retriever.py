import faiss
import numpy as np
from src.embedder import model

index = None
standards_store = []

def build_index(standards, embeddings):
    global index, standards_store

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)

    # Convert to float32 for FAISS compatibility
    index.add(np.array(embeddings, dtype=np.float32))
    standards_store = standards


def retrieve(query, k=5):
    if index is None:
        raise ValueError("Index not built. Call build_index() first.")
    
    query_embedding = model.encode([query]).astype(np.float32)
    D, I = index.search(query_embedding, k)

    results = []
    for idx in I[0]:
        results.append(standards_store[idx])

    # Apply keyword scoring
    query_lower = query.lower()
    
    def keyword_score(item):
        text = item["text"].lower()
        score = 0

        if "cement" in query_lower and "cement" in text:
            score += 2
        if "steel" in query_lower and "steel" in text:
            score += 2
        if "aggregate" in query_lower and "aggregate" in text:
            score += 2
        if "concrete" in query_lower and "concrete" in text:
            score += 1

        return score

    results = sorted(results, key=keyword_score, reverse=True)
    return results