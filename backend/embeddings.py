import numpy as np
from langchain_community.embeddings import HuggingFaceEmbeddings

def get_embedding_model() -> HuggingFaceEmbeddings:
    """
    Initializes and returns the HuggingFaceEmbeddings model using the 
    sentence-transformers/all-MiniLM-L6-v2 pre-trained model.
    This model runs locally and encodes text into 384-dimensional dense vectors.
    
    Returns:
        HuggingFaceEmbeddings: The initialized LangChain embedding model.
    """
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    
    # We configure HuggingFaceEmbeddings to run on CPU by default.
    # If the user has a GPU (cuda), PyTorch will automatically use it if available,
    # but for compatibility, we let sentence-transformers manage device detection.
    encode_kwargs = {'normalize_embeddings': True}  # Normalizing simplifies similarity matching to dot product
    
    try:
        print(f"[Embeddings] Loading embedding model '{model_name}' (this might take a minute on first run)...")
        embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            encode_kwargs=encode_kwargs
        )
        print("[Embeddings] Model loaded successfully.")
        return embeddings
    except Exception as e:
        print(f"[Embeddings Error] Failed to load embedding model: {e}")
        raise e

def cosine_similarity(v1: list, v2: list) -> float:
    """Helper to calculate similarity between two vectors."""
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    return float(dot_product / (norm_v1 * norm_v2))

if __name__ == "__main__":
    # Self-test to verify embeddings model loads and encodes sentences correctly.
    print("Starting embeddings self-test...")
    
    try:
        model = get_embedding_model()
        
        # Test terms:
        # "Hyperglycemia" means high blood sugar, so they should be very similar.
        # "Bone fracture" is unrelated, so it should be less similar.
        term1 = "The patient is experiencing high blood sugar."
        term2 = "The patient has acute hyperglycemia."
        term3 = "The patient broke their left leg bone."
        
        print("\nEncoding sentences...")
        vec1 = model.embed_query(term1)
        vec2 = model.embed_query(term2)
        vec3 = model.embed_query(term3)
        
        print(f"Vector dimension: {len(vec1)} (Expected: 384)")
        
        sim12 = cosine_similarity(vec1, vec2)
        sim13 = cosine_similarity(vec1, vec3)
        
        print("\n--- Cosine Similarity Results ---")
        print(f"Similarity ('high blood sugar' vs 'hyperglycemia'): {sim12:.4f}")
        print(f"Similarity ('high blood sugar' vs 'bone fracture'): {sim13:.4f}")
        
        if sim12 > sim13:
            print("\nTest Successful: Semantic similarity is working correctly!")
        else:
            print("\nTest Failed: Semantic similarity logic is unexpected.")
            
    except Exception as err:
        print(f"Test failed with error: {err}")
