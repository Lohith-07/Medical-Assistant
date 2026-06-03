import os
from typing import List
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from backend.embeddings import get_embedding_model

DB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "db"))

def create_vector_store(
    chunks: List[Document], 
    embeddings, 
    persist_directory: str = DB_DIR
) -> Chroma:
    """
    Creates a new Chroma vector store from text chunks, generates their embeddings,
    and persists them to the local disk.
    
    Args:
        chunks (List[Document]): The list of chunked Document objects.
        embeddings: The embedding model to encode the texts.
        persist_directory (str): Local folder to store the ChromaDB files.
        
    Returns:
        Chroma: The initialized LangChain Chroma vector store.
    """
    try:
        print(f"[Vector Store] Creating vector store in '{persist_directory}'...")
        
        # Initialize and save the database
        # Chroma.from_documents automatically calculates embeddings and writes to disk
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=persist_directory
        )
        
        print(f"[Vector Store] Successfully indexed and saved {len(chunks)} chunks.")
        return vector_store
        
    except Exception as e:
        print(f"[Vector Store Error] Failed to create vector store: {e}")
        raise e

def load_vector_store(
    embeddings, 
    persist_directory: str = DB_DIR
) -> Chroma:
    """
    Loads an already persisted Chroma vector store from local disk.
    
    Args:
        embeddings: The embedding model used for indexing the texts.
        persist_directory (str): Local folder where ChromaDB files are saved.
        
    Returns:
        Chroma: The loaded LangChain Chroma vector store.
    """
    if not os.path.exists(persist_directory):
        raise FileNotFoundError(f"No database directory found at: {persist_directory}")
        
    try:
        print(f"[Vector Store] Loading vector store from '{persist_directory}'...")
        vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings
        )
        return vector_store
    except Exception as e:
        print(f"[Vector Store Error] Failed to load vector store: {e}")
        raise e

if __name__ == "__main__":
    # Self-test block to verify database creation and persistence
    from backend.chunking import split_documents
    
    print("Starting vector store self-test...")
    
    # 1. Create a dummy medical text
    text_data = (
        "Appendicitis is an inflammation of the appendix. "
        "Symptoms commonly include right lower abdominal pain, nausea, vomiting, and decreased appetite. "
        "The standard treatment is surgical removal of the appendix, known as an appendectomy. "
        "Diagnosis is largely based on clinical symptoms, with imaging like ultrasound or CT scan."
    )
    
    doc = Document(
        page_content=text_data,
        metadata={"source": "appendicitis_info.pdf", "page": 2}
    )
    
    # 2. Get embeddings and chunk text
    embeds = get_embedding_model()
    chunks = split_documents([doc], chunk_size=150, chunk_overlap=20)
    
    # 3. Create vector store in db/test_db
    test_db_dir = os.path.join(DB_DIR, "test_db")
    
    try:
        # Create and persist
        db = create_vector_store(chunks, embeds, persist_directory=test_db_dir)
        
        # 4. Load database from disk to verify persistence
        loaded_db = load_vector_store(embeds, persist_directory=test_db_dir)
        
        # 5. Query the loaded database
        query = "What is the surgical removal of the appendix called?"
        results = loaded_db.similarity_search(query, k=1)
        
        print("\n--- Query Results ---")
        print(f"Query: '{query}'")
        if results:
            print(f"Best match page: {results[0].metadata.get('page')}")
            print(f"Best match source: {results[0].metadata.get('source')}")
            print(f"Best match content: '{results[0].page_content}'")
            print("\nTest Successful: ChromaDB successfully persisted and queried!")
        else:
            print("\nTest Failed: No match found.")
            
    except Exception as err:
        print(f"Test failed with error: {err}")
