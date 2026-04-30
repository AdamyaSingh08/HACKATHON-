import sys
sys.path.insert(0, 'src')
from embedder import create_embeddings

# Test with sample data
standards = [{"text": "Hello world"}, {"text": "Test embeddings"}]
embeddings = create_embeddings(standards)
print(f"Embeddings shape: {embeddings.shape}")
print("Success!")
