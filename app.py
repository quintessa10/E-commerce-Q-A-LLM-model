from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders.csv_loader import CSVLoader

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load CSV file with the "response" column
csv_file_path = 'tilak_large.csv'
loader = CSVLoader(file_path=csv_file_path, source_column="response")  # Explicitly load only the "response" column
data = loader.load()

# Create embedding model and vector database using a more powerful model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-mpnet-base-dot-v1")
vectordb = FAISS.from_documents(documents=data, embedding=embedding_model)
retriever = vectordb.as_retriever(score_threshold=0.75)

# Define input and output models for the API
class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str

@app.post("/query", response_model=QueryResponse)
def query_model(request: QueryRequest):
    # Retrieve relevant documents
    docs = retriever.get_relevant_documents(request.query)

    # Extract only the "response" content
    if docs:
        answer = docs[0].page_content.strip()  # page_content corresponds to the "response" column
        return QueryResponse(answer=answer)
    else:
        raise HTTPException(status_code=404, detail="No relevant documents found.")