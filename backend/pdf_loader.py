from typing import List
import os
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader

def load_pdf(file_path: str) -> List[Document]:
    """
    Loads a PDF file and extracts its content as a list of LangChain Document objects.
    Each page in the PDF becomes a single Document object containing the page text 
    and metadata (like the page number and source file path).
    
    Args:
        file_path (str): The path to the PDF file.
        
    Returns:
        List[Document]: A list of LangChain Document objects.
    """
    # Validation: Ensure the file exists before attempting to load it
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found at: {file_path}")
    
    try:
        # Initialize PyPDFLoader with the file path
        loader = PyPDFLoader(file_path)
        
        # Load the document pages
        documents = loader.load()
        
        print(f"[PDF Loader] Successfully loaded {len(documents)} pages from '{file_path}'.")
        return documents
    except Exception as e:
        print(f"[PDF Loader Error] Failed to load PDF file '{file_path}': {e}")
        raise e

if __name__ == "__main__":
    # A simple self-test block to verify the loader works independently
    import sys
    
    # We can test this by running: python backend/pdf_loader.py <path_to_pdf>
    if len(sys.argv) > 1:
        test_pdf = sys.argv[1]
        try:
            pages = load_pdf(test_pdf)
            if pages:
                print("\n--- Test Successful ---")
                print(f"Loaded page count: {len(pages)}")
                print(f"First page preview (first 200 chars):\n{pages[0].page_content[:200]}")
                print(f"Metadata of first page: {pages[0].metadata}")
        except Exception as err:
            print(f"Test failed with error: {err}")
    else:
        print("To test the loader, run: python backend/pdf_loader.py <path_to_some_pdf>")
