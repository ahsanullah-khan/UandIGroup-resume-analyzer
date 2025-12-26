from step3a_imports import AnalysisState, ChatGroq, SentenceTransformer

# Initialize AI Models
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

semantic_model = SentenceTransformer('all-MiniLM-L6-v2')