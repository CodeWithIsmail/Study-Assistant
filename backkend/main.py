# FastAPI Main Application
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routes import router
from user_routes import router as user_router
from database import connect_to_mongo, close_mongo_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()

app = FastAPI(
    title="Study Assistant RAG API",
    description="RAG-based study assistant with user authentication",
    version="1.0.0",
    lifespan=lifespan
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
app.include_router(user_router)

@app.get("/")
async def root():
    return {
        "message": "Study Assistant RAG API with Authentication",
        "endpoints": [
            "POST /api/auth/signup - User registration",
            "POST /api/auth/login - User login",
            "GET /api/auth/me - Get current user info",
            "POST /api/rag/init-db - Initialize ChromaDB with PDFs",
            "POST /api/rag/add-pdf - Add PDFs to existing ChromaDB", 
            "POST /api/rag/ask - Ask questions using RAG"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
