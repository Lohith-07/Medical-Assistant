from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(
    documents: List[Document], 
    chunk_size: int = 700, 
    chunk_overlap: int = 100
) -> List[Document]:
    """
    Splits a list of LangChain Document objects into smaller chunks.
    This is necessary to fit documents within LLM context windows and to 
    allow precise retrieval of relevant information.
    
    Args:
        documents (List[Document]): The list of raw pages loaded from the PDF.
        chunk_size (int): The maximum size of each text chunk (in characters).
        chunk_overlap (int): The character overlap between consecutive chunks 
                            to maintain context at boundaries.
                            
    Returns:
        List[Document]: A list of chunked Document objects.
    """
    try:
        # Initialize the splitter with standard medical RAG parameters
        # It attempts to split by paragraph (\n\n), then sentence (\n), then words (space).
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            add_start_index=True  # Keeps track of where the chunk started in the original page
        )
        
        # Split the documents
        chunks = splitter.split_documents(documents)
        print(f"[Chunking] Successfully split {len(documents)} pages into {len(chunks)} text chunks.")
        return chunks
        
    except Exception as e:
        print(f"[Chunking Error] Failed to split documents: {e}")
        raise e

if __name__ == "__main__":
    # Self-test block to verify chunking independently
    # We will simulate a fake document and chunk it
    fake_doc_text = (
        "Diabetes mellitus is a chronic medical condition. "
        "It is characterized by high levels of blood glucose. "
        "Symptoms include frequent urination, increased thirst, and increased hunger. "
        "If left untreated, diabetes can cause many medical complications. "
        "Acute complications can include diabetic ketoacidosis, hyperosmolar hyperglycemic state, or death. "
        "Serious long-term complications include cardiovascular disease, stroke, chronic kidney disease, "
        "foot ulcers, cognitive impairment, and damage to the eyes."
    )
    
    # Create a mock LangChain Document
    test_doc = Document(
        page_content=fake_doc_text,
        metadata={"source": "test_diabetes_info.txt", "page": 0}
    )
    
    print("Starting chunking self-test...")
    # Chunk using small chunk_size to see the splitting in action
    test_chunks = split_documents([test_doc], chunk_size=150, chunk_overlap=30)
    
    print("\n--- Test Results ---")
    for idx, chunk in enumerate(test_chunks):
        print(f"\nChunk {idx+1} (Length: {len(chunk.page_content)}):")
        print(f"Content: '{chunk.page_content}'")
        print(f"Metadata: {chunk.metadata}")
