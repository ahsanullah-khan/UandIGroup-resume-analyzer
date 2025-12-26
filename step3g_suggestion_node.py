from step3a_imports import AnalysisState

def generate_suggestions_node(state: AnalysisState) -> AnalysisState:
    """Generate simplified missing skills list"""
    missing_skills = state["keyword_matches"]["missing_skills"]

    # Return only missing skills as suggestions
    return {
        "suggested_changes": missing_skills[:10],  # Limit to top 10 missing skills
        "missing_skills": missing_skills
    }