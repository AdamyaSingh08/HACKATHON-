# BIS RAG Hackathon Project

## 🚀 Overview

This project implements a **Retrieval-Augmented Generation (RAG) system** to help users find relevant **BIS (Bureau of Indian Standards) standards** for a given product query.

The system processes user queries, retrieves the most relevant standard documents from the dataset, and returns the **top 3–5 matching standards** with low latency and high accuracy.

---

## 🎯 Problem Statement

Small and Medium Enterprises (MSEs) often struggle to identify the correct BIS standards applicable to their products. Manual search is time-consuming and inefficient.

---

## 💡 Solution

We built an end-to-end RAG pipeline that:

1. Converts BIS documents into searchable embeddings
2. Retrieves the most relevant chunks using vector similarity
3. Outputs the top standards ranked by relevance

---

## 🧠 System Architecture

```
User Query
   ↓
Embedding Model (Sentence Transformers)
   ↓
Vector Database (FAISS)
   ↓
Top-K Retrieval
   ↓
(Optional LLM Processing)
   ↓
Top 3–5 BIS Standards
```

---

## 🔍 Chunking & Retrieval Strategy

* Chunk Size: 300–500 words
* Overlap: 50–100 words
* Embedding Model: `all-MiniLM-L6-v2`
* Vector Store: FAISS (for fast similarity search)

This ensures better semantic matching and improves retrieval accuracy.

---

## ⚙️ Installation

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

```bash
python inference.py --input sample_input.json --output output.json
```

---

## 📂 Project Structure

```
HACKATHON-/
│
├── src/                 # Core RAG pipeline code
├── data/                # Dataset and outputs
├── inference.py         # Entry point for evaluation (MANDATORY)
├── eval_script.py       # Provided evaluation script
├── requirements.txt     # Dependencies
├── presentation.pdf     # Final PPT
├── README.md            # Project documentation
```

---

## 📊 Evaluation Metrics

The system is evaluated using:

* **Hit Rate @3** → Target: >80%
* **MRR @5** → Target: >0.7
* **Average Latency** → Target: <5 seconds

---

## ⚡ Performance Optimization

* Precomputed embeddings for faster retrieval
* FAISS indexing for efficient search
* Minimal runtime processing to reduce latency

---

## 🚫 Constraints Followed

* Only the provided dataset is used
* No external or fabricated standards
* All dependencies documented
* Fully reproducible on standard hardware

---

## 🧪 Output Format

The system generates output in the required JSON format:

```json
[
  {
    "id": "1",
    "retrieved_standards": ["IS 123", "IS 456", "IS 789"],
    "latency_seconds": 1.25
  }
]
```

---

## 👥 Team

* Member 1 Adamya Singh
* Member 2 Adarsh Singh
* Member 3 Bhavya Kapoor
* Member 4 Gaurav Shukla

---

## 🙏 Acknowledgements

* BIS Hackathon Organizers
* Dataset: BIS SP 21 Standards

---

## 📌 Notes

* Ensure `inference.py` runs correctly before submission
* Do not modify the output JSON format
* Keep latency under required limits

---
