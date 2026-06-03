from langchain_core.prompts import ChatPromptTemplate

def get_medical_prompt() -> ChatPromptTemplate:
    """
    Creates and returns a system prompt template designed for grounded QA.
    It instructs the LLM to only answer using the retrieved text chunks
    and avoid hallucinating.
    
    Returns:
        ChatPromptTemplate: The prompt template.
    """
    system_instruction = (
        "You are an expert Medical AI Assistant designed to answer questions accurately "
        "using only the provided context. Follow these rules strictly:\n"
        "1. Answer the question using ONLY the provided clinical context. Do not use outside medical knowledge.\n"
        "2. Be concise, professional, and clear.\n"
        "3. If the retrieved context does not contain enough information to answer the question, "
        "clearly state: 'I cannot answer this based on the provided document.'\n"
        "4. Never hallucinate, speculate, or make up facts. Your response must be grounded strictly in the source text.\n\n"
        "--- Context ---\n"
        "{context}\n"
        "----------------"
    )
    
    # Define a clean chat-based template with system instructions and user input
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_instruction),
        ("human", "{question}")
    ])
    
    return prompt
