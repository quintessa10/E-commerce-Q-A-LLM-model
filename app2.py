from fastapi import FastAPI
from pydantic import BaseModel
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders.csv_loader import CSVLoader
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

# ✅ Load the dataset (real test queries)
csv_file_path = 'tilak_large.csv'
data = pd.read_csv(csv_file_path, encoding="ISO-8859-1")

# ✅ Ensure correct columns exist
if "prompt" not in data.columns or "response" not in data.columns:
    raise ValueError("Dataset must contain 'prompt' and 'response' columns.")

# ✅ Convert dataset into test queries
test_queries = [{"query": row["prompt"], "expected_answer": row["response"]} for _, row in data.iterrows()]

# ✅ Load FAISS Model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-mpnet-base-dot-v1")
loader = CSVLoader(file_path=csv_file_path, source_column="response")
data = loader.load()
vectordb = FAISS.from_documents(documents=data, embedding=embedding_model)
retriever = vectordb.as_retriever(score_threshold=0.75)

# ✅ Function to calculate similarity using embeddings
def calculate_semantic_similarity(predicted_answer, expected_answer):
    predicted_embedding = embedding_model.embed_query(predicted_answer)  # Use embed_query() for single queries
    expected_embedding = embedding_model.embed_query(expected_answer)
    
    # Compute Cosine Similarity
    similarity = cosine_similarity([predicted_embedding], [expected_embedding])[0][0]
    return similarity

# ✅ Function to evaluate model accuracy
def evaluate_accuracy(test_queries):
    correct_predictions = 0
    total_queries = len(test_queries)
    threshold = 0.8  # Consider answers correct if similarity > 80%

    for query in test_queries:
        docs = retriever.get_relevant_documents(query["query"])  # ✅ FIXED: Use get_relevant_documents()
        
        if docs:
            predicted_answer = docs[0].page_content.strip()
        else:
            predicted_answer = "No relevant documents found."

        similarity = calculate_semantic_similarity(predicted_answer.lower(), query["expected_answer"].lower())

        # ✅ Count correct answers
        if similarity > threshold:
            correct_predictions += 1

        # ✅ Debugging Output
        print(f"Query: {query['query']}")
        print(f"Expected: {query['expected_answer']}")
        print(f"Predicted: {predicted_answer}")
        print(f"Similarity Score: {similarity:.2f}")
        print("-" * 50)

    # ✅ Calculate Accuracy
    accuracy = (correct_predictions / total_queries) * 100
    return accuracy

# ✅ Run evaluation and print results
accuracy = evaluate_accuracy(test_queries)
print(f"📊 Model Accuracy: {accuracy:.2f}%")

