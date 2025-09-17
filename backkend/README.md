# 🎓 Study Assistant - RAG-based AI Chatbot

A powerful **Retrieval-Augmented Generation (RAG)** chatbot designed to help software engineering students learn from their course materials. Upload PDFs, ask questions, and get intelligent responses with source citations.

## 🚀 Features

- **📄 PDF Processing**: Extract and process content from lecture notes, textbooks, and study materials
- **🔍 Intelligent Search**: Vector-based similarity search through your documents
- **💬 Conversational Memory**: Maintains context across multiple questions
- **📚 Source Citations**: Shows which documents were used to generate answers
- **⚡ Fast API**: Optimized for quick responses
- **🔄 Incremental Updates**: Add new PDFs without rebuilding the entire knowledge base

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI       │    │   RAG Service   │    │   ChromaDB      │
│   Routes        │◄──►│   (Business     │◄──►│   Vector Store  │
│   (HTTP Layer)  │    │    Logic)       │    │   (Embeddings)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       ▼                       │
         │              ┌─────────────────┐              │
         │              │   Gemini LLM    │              │
         └──────────────►│   (Google AI)   │◄─────────────┘
                        └─────────────────┘
```

## 📦 Installation

### Prerequisites
- Python 3.12+
- Google AI API Key (Gemini)

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd Study-Assistant

# Create virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### Get Google AI API Key
1. Go to [Google AI Studio](https://makersuite.google.com/)
2. Create a new API key
3. Add it to your `.env` file:
```bash
GEMINI_API_KEY=your_actual_api_key_here
```

## 🎯 Quick Start

### 1. Start the Server
```bash
source env/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server will start at: `http://localhost:8000`

### 2. Initialize Knowledge Base
**First time only** - Upload your PDFs to create the knowledge base:

```bash
curl -X POST "http://localhost:8000/api/rag/init-db" \
  -H "Content-Type: application/json" \
  -d '{
    "pdf_paths": [
      "assets/Sample.pdf",
      "assets/GreedyAlgorithms.pdf"
    ]
  }'
```

### 3. Ask Questions
```bash
curl -X POST "http://localhost:8000/api/rag/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is a greedy algorithm and how does it work?"
  }'
```

### 4. Add More PDFs (Optional)
```bash
curl -X POST "http://localhost:8000/api/rag/add-pdf" \
  -H "Content-Type: application/json" \
  -d '{
    "pdf_paths": [
      "assets/Lecture#7.pdf",
      "assets/metrics3.pdf"
    ]
  }'
```

## 🔌 API Endpoints

### POST `/api/rag/init-db`
Initialize the knowledge base with PDFs (first time only).

**Request:**
```json
{
  "pdf_paths": ["path/to/file1.pdf", "path/to/file2.pdf"]
}
```

**Response:**
```json
{
  "status": "success",
  "message": "ChromaDB initialized successfully with PDFs",
  "documents_processed": 2,
  "chunks_created": 157
}
```

### POST `/api/rag/add-pdf`
Add more PDFs to existing knowledge base.

**Request:**
```json
{
  "pdf_paths": ["path/to/new_file.pdf"]
}
```

**Response:**
```json
{
  "status": "success",
  "message": "PDFs added to existing ChromaDB successfully",
  "new_documents_added": 45,
  "total_documents": 202
}
```

### POST `/api/rag/ask`
Ask questions using the RAG system.

**Request:**
```json
{
  "question": "Explain the time complexity of binary search"
}
```

**Response:**
```json
{
  "answer": "Binary search has O(log n) time complexity because...",
  "sources": [
    {
      "source": "Algorithms.pdf",
      "chunk_id": "23",
      "content_preview": "Binary search is a divide and conquer algorithm..."
    }
  ],
  "conversation_length": 3
}
```

## 📁 Project Structure

```
Study-Assistant/
├── main.py              # FastAPI application setup
├── routes.py             # API route handlers
├── service.py            # RAG business logic
├── models.py             # Pydantic request/response models
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (API keys)
├── .gitignore           # Git ignore rules
├── assets/              # PDF files for knowledge base
│   ├── Sample.pdf
│   ├── GreedyAlgorithms.pdf
│   └── ...
├── chroma_db/           # Persistent vector database
└── models_cache/        # Cached embedding models
```

## ⚙️ Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Google AI API key (required)

### Performance Tuning
Current optimizations for fast responses:
- Chunk size: 800 tokens (vs 1000)
- Retrieval: Top 3 documents (vs 5)  
- Memory: 3 conversation turns (vs 5)
- Output: 512 tokens max (vs 1024)

## 🔄 Workflow

### First Time Setup:
1. Start server
2. Call `/init-db` with your PDFs
3. Ask questions with `/ask`

### Subsequent Sessions:
1. Start server (auto-loads existing database)
2. Ask questions immediately with `/ask`
3. Add more PDFs anytime with `/add-pdf`

## 🧠 How It Works

1. **PDF Processing**: Extracts text from PDFs using PyMuPDF
2. **Chunking**: Splits documents into overlapping 800-token chunks
3. **Embedding**: Converts chunks to vectors using SentenceTransformers
4. **Storage**: Stores embeddings in ChromaDB for fast retrieval
5. **Retrieval**: Finds relevant chunks using similarity search
6. **Generation**: Uses Gemini LLM to generate answers from context
7. **Memory**: Maintains conversation history for follow-up questions

## 🛠️ Dependencies

### Core Libraries:
- **FastAPI**: Web framework for the API
- **LangChain**: RAG pipeline orchestration
- **ChromaDB**: Vector database for embeddings
- **PyMuPDF**: PDF text extraction
- **SentenceTransformers**: Text embeddings
- **Google Generative AI**: LLM for answer generation

### Development:
```bash
pip install -r requirements.txt
```

## 📊 Performance

- **Initialization**: ~30 seconds for 4 PDFs (first time only)
- **Query Response**: ~2-5 seconds per question
- **Memory Usage**: ~200MB for typical knowledge base
- **Storage**: ~50MB ChromaDB for 4 lecture PDFs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Troubleshooting

### Common Issues:

**"GEMINI_API_KEY not found"**
- Make sure your `.env` file exists and contains the API key

**"No existing ChromaDB found"**
- Run `/init-db` first to create the knowledge base

**"Rate limit exceeded"**
- Wait a few minutes between requests (Gemini API limits)

**Slow responses**
- First query is slower due to model loading
- Subsequent queries should be faster

### Getting Help:
- Check the terminal output for detailed error messages
- Ensure all PDFs exist in the specified paths
- Verify your API key is valid

---

**Happy studying! 🎓✨**