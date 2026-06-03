import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.prompts import get_medical_prompt

# Load environment variables from .env file
load_dotenv()

def get_llm() -> ChatGoogleGenerativeAI:
    """
    Initializes and returns the Google Gemini LLM.
    It reads the API key from the environment variables.
    
    Returns:
        ChatGoogleGenerativeAI: The initialized LLM instance.
    """
    # Fetch either GEMINI_API_KEY or GOOGLE_API_KEY
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    
    if not api_key or api_key == "your_gemini_api_key_here":
        raise ValueError(
            "Gemini API Key is missing. Please set GEMINI_API_KEY or GOOGLE_API_KEY "
            "in your .env file."
        )
        
    try:
        # We set temperature low (e.g. 0.1) to minimize creativity/hallucinations for medical QA
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.1
        )
        print("[LLM] Google Gemini 2.5 Flash initialized successfully.")
        return llm
    except Exception as e:
        print(f"[LLM Error] Failed to initialize Gemini model: {e}")
        raise e

def run_rag_pipeline(query: str, retriever, llm) -> dict:
    """
    Runs the complete Retrieval-Augmented Generation pipeline.
    1. Retrieves relevant text chunks using the retriever.
    2. Formats the text chunks as context.
    3. Prompts the LLM with the context and user query.
    4. Returns both the answer and the source document objects.
    
    Args:
        query (str): The user's question.
        retriever: The LangChain retriever object.
        llm: The Gemini LLM object.
        
    Returns:
        dict: A dictionary containing:
              - 'answer': str (the generated answer)
              - 'source_documents': List[Document] (retrieved context chunks)
    """
    try:
        # Step 1: Retrieve context chunks
        print(f"[RAG Chain] Retrieving relevant chunks for query: '{query}'...")
        source_docs = retriever.invoke(query)
        
        # Step 2: Format the text content from chunks
        context_text = "\n\n".join([
            f"Source Page {doc.metadata.get('page', 'unknown')} ({doc.metadata.get('source', 'unknown')}):\n{doc.page_content}"
            for doc in source_docs
        ])
        
        # Step 3: Get prompt and format it
        prompt_template = get_medical_prompt()
        prompt_messages = prompt_template.format_messages(
            context=context_text,
            question=query
        )
        
        # Step 4: Run Gemini LLM inference
        print("[RAG Chain] Invoking Gemini LLM for grounded answer...")
        response = llm.invoke(prompt_messages)
        
        # Step 5: Return result dictionary
        return {
            "answer": response.content,
            "source_documents": source_docs
        }
        
    except Exception as e:
        print(f"[RAG Chain Error] Failed to run pipeline: {e}")
        raise e

if __name__ == "__main__":
    # Self-test block to run RAG pipeline end-to-end
    from backend.embeddings import get_embedding_model
    from backend.vector_store import load_vector_store
    from backend.retriever import get_retriever
    
    print("Starting RAG chain self-test...")
    
    # 1. Setup paths
    DB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "db"))
    test_db_dir = os.path.join(DB_DIR, "test_db")
    
    if not os.path.exists(test_db_dir):
        print("Please run vector_store.py test first to build the database.")
    else:
        # Try running end-to-end (requires a valid GEMINI_API_KEY in .env)
        try:
            embeds = get_embedding_model()
            db = load_vector_store(embeds, persist_directory=test_db_dir)
            retriever = get_retriever(db, k=2)
            
            # This will raise an error if GEMINI_API_KEY is not set yet, which is expected!
            llm = get_llm()
            
            test_query = "What standard imaging diagnosis is used for appendicitis?"
            result = run_rag_pipeline(test_query, retriever, llm)
            
            print("\n--- RAG Chain Response ---")
            print(f"Answer: {result['answer']}")
            print("\n--- Sources Used ---")
            for doc in result['source_documents']:
                print(f"- Page {doc.metadata.get('page')}: {doc.page_content[:100]}...")
                
            print("\nTest Successful: RAG Pipeline executed completely!")
            
        except ValueError as val_err:
            print(f"\n[Environment Alert] {val_err}")
            print("Note: The test cannot complete without a real Gemini API Key. This is normal and expected.")
        except Exception as err:
            print(f"Test failed with unexpected error: {err}")
