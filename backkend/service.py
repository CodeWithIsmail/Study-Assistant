# RAG Service - Core RAG functionality
import fitz  # PyMuPDF
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.schema import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

# Load environment variables
load_dotenv()

class RAGService:
    def __init__(self):
        self.persist_directory = "./chroma_db"
        # Use a smaller, faster embedding model
        self.embedding_model = SentenceTransformerEmbeddings(
            model_name="all-MiniLM-L6-v2",
            cache_folder="./models_cache"  # Cache models locally
        )
        self.vectorstore = None
        self.retriever = None
        self.llm = None
        self.rag_chain = None
        self.memory = None
        
        # Initialize LLM and memory
        self._initialize_llm()
        self._initialize_memory()
    
    def _initialize_llm(self):
        """Initialize Gemini LLM"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key,
            temperature=0.7,
            max_output_tokens=1200  # Reduced for faster responses
        )
    
    def _initialize_memory(self):
        """Initialize conversation memory"""
        self.memory = ConversationBufferWindowMemory(
            k=3,  # Reduced conversation history for faster processing
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF using PyMuPDF"""
        if not os.path.exists(pdf_path):
            return ""
        
        doc = fitz.open(pdf_path)
        text = ""
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            page_text = page.get_text()
            
            if page_text.strip():
                text += f"\n\n--- Lecture Page {page_num + 1} ---\n\n"
                text += page_text
        
        doc.close()
        return text
    
    def create_overlapping_chunks(self, text: str, chunk_size: int = 800, chunk_overlap: int = 100) -> List[Document]:
        """Split text into overlapping chunks (smaller chunks for faster processing)"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        chunks = text_splitter.split_text(text)
        
        documents = []
        for i, chunk in enumerate(chunks):
            doc = Document(
                page_content=chunk,
                metadata={
                    "chunk_id": i,
                    "source": "Unknown",
                    "chunk_size": len(chunk),
                    "content_type": "lecture_notes"
                }
            )
            documents.append(doc)
        
        return documents
    
    def process_pdfs(self, pdf_paths: List[str]) -> List[Document]:
        """Process multiple PDF files and create document chunks"""
        extracted_texts = {}
        
        for pdf_path in pdf_paths:
            if os.path.exists(pdf_path):
                text = self.extract_text_from_pdf(pdf_path)
                extracted_texts[os.path.basename(pdf_path)] = text
        
        documents = []
        for source, text in extracted_texts.items():
            docs = self.create_overlapping_chunks(text)
            for doc in docs:
                doc.metadata["source"] = source
            documents.extend(docs)
        
        return documents
    
    def create_vectorstore(self, documents: List[Document]):
        """Create ChromaDB vector store"""
        if not documents:
            return
        
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embedding_model,
            persist_directory=self.persist_directory,
            collection_name="software_engineering_knowledge_base"
        )
        
        self.vectorstore.persist()
        self._setup_retriever_and_chain()
    
    def load_vectorstore(self) -> bool:
        """Load existing vector store from disk"""
        if os.path.exists(self.persist_directory):
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embedding_model,
                collection_name="software_engineering_knowledge_base"
            )
            self._setup_retriever_and_chain()
            return True
        return False
    
    def add_to_vectorstore(self, documents: List[Document]):
        """Add documents to existing vector store"""
        if not self.vectorstore:
            raise ValueError("Vector store not initialized")
        
        self.vectorstore.add_documents(documents)
        self.vectorstore.persist()
    
    def _setup_retriever_and_chain(self):
        """Setup retriever and RAG chain"""
        if not self.vectorstore:
            return
        
        # Create retriever
        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity",  # Faster than similarity_score_threshold
            search_kwargs={
                "k": 5  # Reduced from 5 for faster retrieval
            }
        )
        
        # Create RAG chain
        qa_prompt_template = """You are an expert assistant for software engineering courses such as Distributed Systems, Software Metrics, and related subjects.

You will be given a QUESTION and some CONTEXT extracted from course materials (lecture notes, slides, PDFs, textbooks).

Instructions:
- Always use the CONTEXT as the starting point of your answer.  
- If the CONTEXT provides only names, terms, or short points, then expand each one in detail using your own knowledge (definitions, purpose, examples, pros/cons).  
- If the CONTEXT provides some explanation but not enough detail, merge the given explanation with your own knowledge to produce a richer, more complete answer.  
- If the CONTEXT is completely empty or irrelevant, say:  
  "Dont say you dont have in context.  
- Always explain thoroughly, not in one line. Use structured formats:
  - Definitions (if applicable)  
  - Key points or steps  
  - Additional elaboration/examples from your knowledge  
- Make sure the answer is clear, detailed, and student-friendly for exam preparation.

---

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
zna-jeny-ihn"""

        qa_prompt = PromptTemplate(
            template=qa_prompt_template,
            input_variables=["context", "question"]
        )
        
        self.rag_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            memory=self.memory,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": qa_prompt},
            verbose=False
        )
    
    def ask_question(self, question: str) -> Dict:
        """Ask a question to the RAG chatbot"""
        if not self.rag_chain:
            raise ValueError("RAG chain not initialized")
        
        result = self.rag_chain({"question": question})
        
        sources = []
        source_documents = result.get('source_documents', [])
        
        # If no source documents in result, manually retrieve them
        if not source_documents and self.retriever:
            print("No sources in chain result, manually retrieving...")
            source_documents = self.retriever.get_relevant_documents(question)
        
        print(f"Found {len(source_documents)} source documents")
        
        for i, doc in enumerate(source_documents):
            print(f"Document {i}: {doc.metadata}")
            sources.append({
                "source": doc.metadata.get('source', 'Unknown'),
                "chunk_id": str(doc.metadata.get('chunk_id', i)),
                "content_preview": doc.page_content[:100] + "..." if len(doc.page_content) > 100 else doc.page_content
            })
        
        # If still no sources found, add a message
        if not sources:
            sources.append({
                "source": "No sources found",
                "chunk_id": "N/A",
                "content_preview": "No relevant documents were found in the knowledge base for this question."
            })
        
        return {
            "answer": result['answer'],
            "sources": sources,
            "conversation_length": len(self.memory.chat_memory.messages) // 2 if self.memory else 0
        }
    
    def get_document_count(self) -> int:
        """Get total number of documents in vector store"""
        if not self.vectorstore:
            return 0
        try:
            collection = self.vectorstore._collection
            return collection.count()
        except:
            return 0
