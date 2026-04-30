from sentence_transformers import SentenceTransformer

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def create_embeddings(standards):
    texts = [s["text"] for s in standards]
    embeddings = model.encode(texts)
    return embeddings