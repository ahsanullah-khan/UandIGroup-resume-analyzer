# Import all components
from step3a_imports import AnalysisState, StateGraph, END
from step3b_models import llm, semantic_model
from step3c_utils import extract_text_from_file, extract_years_of_experience, clean_text_for_similarity
from step3d_keyword_node import keyword_extraction_node
from step3e_semantic_node import semantic_analysis_node
from step3f_scoring_node import calculate_match_score_node
from step3g_suggestion_node import generate_suggestions_node

# Re-export key components for the main app
__all__ = [
    'AnalysisState',
    'resume_analyzer_app',
    'extract_text_from_file',
    'llm',
    'semantic_model'
]

# Create LangGraph Workflow
workflow = StateGraph(AnalysisState)

# Add nodes
workflow.add_node("keyword_extraction", keyword_extraction_node)
workflow.add_node("semantic_analysis", semantic_analysis_node)
workflow.add_node("score_calculation", calculate_match_score_node)
workflow.add_node("suggestion_generation", generate_suggestions_node)

# Build workflow
workflow.set_entry_point("keyword_extraction")
workflow.add_edge("keyword_extraction", "semantic_analysis")
workflow.add_edge("semantic_analysis", "score_calculation")
workflow.add_edge("score_calculation", "suggestion_generation")
workflow.add_edge("suggestion_generation", END)

# Compile the application
resume_analyzer_app = workflow.compile()

print("✅ Bulk Resume Analyzer built successfully!")