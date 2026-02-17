# FlashSpace AI Bot 🚀

A FastAPI-powered AI chatbot that uses vector search and retrieval-augmented generation (RAG) to provide intelligent responses about FlashSpace services.

## Features

- **Vector Search**: Uses Voyage AI embeddings for semantic search across knowledge base
- **Reranking**: Implements two-stage retrieval with reranking for improved relevance
- **Chat Memory**: Maintains conversation history in MongoDB
- **MongoDB Integration**: Stores knowledge base and conversation logs

## Tech Stack

- **Framework**: FastAPI with Uvicorn
- **Embeddings**: Voyage AI (voyage-3-large model)
- **Reranking**: Voyage AI Rerank-2 model
- **Database**: MongoDB Atlas
- **Language**: Python 3.x

## Setup

### Prerequisites

- Python 3.8+
- MongoDB Atlas account
- Voyage AI API key

### Installation

1. Clone the repository:
```bash
git clone <repo-url>
cd Space_patner_bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables in `.env`:
```env
VOYAGE_API_KEY=<your-voyage-ai-key>
MONGODB_URI=<your-mongodb-uri>
MONGODB_DB=flashspace
KNOWLEDGE_COLLECTION=knowledge_base
MEMORY_COLLECTION=chat_memory
LEAD_COLLECTION=leads
VECTOR_INDEX_NAME=vector_index
EMBED_MODEL=voyage-3-large
RERANK_MODEL=rerank-2
```

## Running the Application

### Local Development

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Production (Heroku)

```bash
heroku login
git push heroku main
```

## API Endpoints

### Health Check
- **GET** `/`
- Returns: `{"status": "FlashSpace AI 2026 Running 🚀"}`

### Chat
- **POST** `/chat`
- Request body:
```json
{
  "userId": "user123",
  "message": "Your question here"
}
```
- Response:
```json
{
  "reply": "AI generated response with relevant information"
}
```

## System Architecture

1. **Vector Search**: Query is embedded using Voyage AI and matched against MongoDB vector index
2. **Reranking**: Top 200 candidates are reranked to find top 3 most relevant documents
3. **Response Generation**: Context from top 3 documents is formatted into a helpful response
4. **Memory Storage**: Both user messages and assistant responses are saved to chat memory

## Project Structure

- `main.py` - FastAPI application and endpoints
- `config.py` - Configuration management
- `db.py` - MongoDB connection and collection initialization
- `embeddings.py` - Voyage AI embedding generation
- `search.py` - Vector search implementation
- `rerank.py` - Document reranking logic
- `response_builder.py` - Response formatting
- `memory.py` - Chat history storage
- `requirements.txt` - Python dependencies
- `Procfile` - Heroku deployment configuration

## Environment Variables

| Variable | Description |
|----------|-------------|
| `VOYAGE_API_KEY` | API key for Voyage AI services |
| `MONGODB_URI` | MongoDB connection string |
| `MONGODB_DB` | Database name in MongoDB |
| `KNOWLEDGE_COLLECTION` | Collection storing knowledge base |
| `MEMORY_COLLECTION` | Collection storing chat history |
| `LEAD_COLLECTION` | Collection for lead information |
| `VECTOR_INDEX_NAME` | MongoDB vector search index name |
| `EMBED_MODEL` | Embedding model (voyage-3-large) |
| `RERANK_MODEL` | Reranking model (rerank-2) |

## Deployment

The application is configured for Heroku deployment. The `Procfile` specifies the command to run the FastAPI server.

## License

Proprietary - FlashSpace 2026
