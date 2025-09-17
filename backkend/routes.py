# FastAPI Routes
from fastapi import APIRouter, HTTPException, Depends
from models import (
    InitDBRequest, InitDBResponse,
    AddPDFRequest, AddPDFResponse, 
    AskRequest, AskResponse, SourceDocument
)
from service import RAGService

router = APIRouter(prefix="/api/rag", tags=["RAG"])

def get_rag_service() -> RAGService:
    return RAGService()

@router.post("/init-db", response_model=InitDBResponse, status_code=201)
async def init_db(request: InitDBRequest, rag_service: RAGService = Depends(get_rag_service)):
    """
    POST /init-db
    Input: 1+ PDFs
    Action: Create ChromaDB if it doesn't exist, Add PDFs into it
    Output: confirmation
    """
    try:
        # Process PDFs and create documents
        documents = rag_service.process_pdfs(request.pdf_paths)
        if not documents:
            raise HTTPException(
                status_code=400,
                detail="No valid content found in provided PDFs"
            )
        
        # Create vector store
        rag_service.create_vectorstore(documents)
        
        return InitDBResponse(
            status="success",
            message="ChromaDB initialized successfully with PDFs",
            documents_processed=len(request.pdf_paths),
            chunks_created=len(documents)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initializing database: {str(e)}")

@router.post("/add-pdf", response_model=AddPDFResponse)
async def add_pdf(request: AddPDFRequest, rag_service: RAGService = Depends(get_rag_service)):
    """
    POST /add-pdf
    Input: 1+ PDFs
    Action: Load persisted Chroma, Add new PDFs, Persist again
    Output: confirmation
    """
    try:
        # Load existing vector store if not already loaded
        if not rag_service.vectorstore:
            loaded = rag_service.load_vectorstore()
            if not loaded:
                raise HTTPException(
                    status_code=400,
                    detail="No existing ChromaDB found. Use /init-db first."
                )
        
        # Get current document count
        current_count = rag_service.get_document_count()
        
        # Process new PDFs
        new_documents = rag_service.process_pdfs(request.pdf_paths)
        if not new_documents:
            raise HTTPException(
                status_code=400,
                detail="No valid content found in provided PDFs"
            )
        
        # Add to existing vector store
        rag_service.add_to_vectorstore(new_documents)
        
        return AddPDFResponse(
            status="success",
            message="PDFs added to existing ChromaDB successfully",
            new_documents_added=len(new_documents),
            total_documents=rag_service.get_document_count()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding PDFs: {str(e)}")

@router.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest, rag_service: RAGService = Depends(get_rag_service)):
    """
    POST /ask
    Input: question text
    Action: Load persisted Chroma, Query with RAG chain
    Output: answer + sources
    """
    try:
        # Load existing vector store if not already loaded
        if not rag_service.vectorstore:
            loaded = rag_service.load_vectorstore()
            if not loaded:
                raise HTTPException(
                    status_code=400,
                    detail="No ChromaDB found. Use /init-db first to create knowledge base."
                )
        
        # Validate question
        if not request.question.strip():
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty"
            )
        
        # Get answer from RAG
        result = rag_service.ask_question(request.question)
        
        # Convert sources to response model
        sources = [
            SourceDocument(
                source=src["source"],
                chunk_id=src["chunk_id"],
                content_preview=src["content_preview"]
            )
            for src in result["sources"]
        ]
        
        return AskResponse(
            answer=result["answer"],
            sources=sources,
            conversation_length=result["conversation_length"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")
