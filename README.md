# doc-chat-agent-backend
This is the backend for a Document-Based Chatbot built using **FastAPI**. It enables users to upload documents and interact with them using natural language queries. The backend uses **LlamaIndex** for indexing/querying and **ChromaDB** for vector storage.

# Features
- Upload and process documents (PDF, TXT, etc.)
- Chat interface backed by LLM
- Uses LlamaIndex for building context-aware document indexes
- Uses ChromaDB as the vector store

# Tech Stack
- Python 3.10+
- FastAPI
- LlamaIndex
- ChromaDB
- Uvicorn

## Setup Instructions

# Clone the Repository

git clone [https://github.com/your-username/document-chat-backend.git](https://github.com/saandeep123456/doc-chat-agent-backend.git)
cd doc-chat-agent-backend

# Create a Virtual Environment
python3 -m venv venv
source venv/bin/activate (or) venv\Scripts\activate

# Install Requirements
pip install -r requirements.txt

# Run the Server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Test API
Visit: http://localhost:8000/docs to see interactive Swagger UI

# Environment Variables
You can configure OpenAI key or other credentials using .env file if needed:
OPENAI_API_KEY=your_key_here





