from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from sentence_transformers import SentenceTransformer, util
import re

class AnalysisState(TypedDict):
    resume_text: str
    job_description: str
    match_percentage: float
    missing_skills: List[str]
    suggested_changes: List[str]
    keyword_matches: Dict
    semantic_similarity: float
    candidate_name: str
    total_experience: int
    current_position: str
    education: List[str]
    general_feedback: str