# FastAPI Main Application
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router

app = FastAPI(
    title="Study Assistant RAG API",
    description="RAG-based study assistant for software engineering students",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)

@app.get("/")
async def root():
    return {
        "message": "Study Assistant RAG API",
        "endpoints": [
            "POST /api/rag/init-db - Initialize ChromaDB with PDFs",
            "POST /api/rag/add-pdf - Add PDFs to existing ChromaDB", 
            "POST /api/rag/ask - Ask questions using RAG"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
