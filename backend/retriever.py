from langchain_core.vectorstores import VectorStoreRetriever
from langchain_community.vectorstores import Chroma

def get_retriever(vector_store: Chroma, k: int = 3) -> VectorStoreRetriever:
    """
    Converts a Chroma vector store into a LangChain Retriever object.
    
    Args:
        vector_store (Chroma): The initialized Chroma database.
        k (int): The number of relevant documents to retrieve for a query.
        
    Returns:
        VectorStoreRetriever: A retriever object that can be chained in LangChain.
    """
    try:
        # We use a standard similarity search.
        # search_kwargs={"k": k} tells the retriever to return the top k matches.
        retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        )
        print(f"[Retriever] Initialized similarity search retriever (k={k}).")
        return retriever
    except Exception as e:
        print(f"[Retriever Error] Failed to create retriever: {e}")
        raise e

if __name__ == "__main__":
    # Self-test using the test database from Phase 5
    import os
    from backend.embeddings import get_embedding_model
    from backend.vector_store import load_vector_store
    
    print("Starting retriever self-test...")
    
    DB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "db"))
    test_db_dir = os.path.join(DB_DIR, "test_db")
    
    if not os.path.exists(test_db_dir):
        print(f"Error: Test database does not exist at '{test_db_dir}'. Please run Phase 5 test first.")
    else:
        try:
            # 1. Load embeddings and vector store
            embeds = get_embedding_model()
            db = load_vector_store(embeds, persist_directory=test_db_dir)
            
            # 2. Get retriever
            retriever = get_retriever(db, k=2)
            
            # 3. Test retrieval
            query = "What standard imaging diagnosis is used for appendicitis?"
            print(f"\nQuerying: '{query}'...")
            
            # invoke() retrieves the top documents
            retrieved_docs = retriever.invoke(query)
            
            print("\n--- Retrieval Results ---")
            print(f"Retrieved {len(retrieved_docs)} chunks:")
            for idx, doc in enumerate(retrieved_docs):
                print(f"\nResult {idx+1}:")
                print(f"Content: '{doc.page_content}'")
                print(f"Metadata: {doc.metadata}")
                
            if len(retrieved_docs) > 0:
                print("\nTest Successful: Retriever retrieved relevant chunks correctly!")
            else:
                print("\nTest Failed: No chunks were retrieved.")
                
        except Exception as err:
            print(f"Test failed with error: {err}")
