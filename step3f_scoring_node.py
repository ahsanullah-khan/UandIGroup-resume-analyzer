from step3a_imports import AnalysisState
from step3c_utils import generate_general_feedback

def calculate_match_score_node(state: AnalysisState) -> AnalysisState:
    """Calculate overall match percentage using weighted scoring"""
    keyword_data = state["keyword_matches"]
    semantic_similarity = state["semantic_similarity"]

    required_skills = keyword_data["required_skills"]
    resume_skills = keyword_data["resume_skills"]
    resume_years = keyword_data["resume_years"]
    job_years = keyword_data["job_years"]

    keyword_match_score = len([skill for skill in required_skills if skill in resume_skills]) / len(required_skills) if required_skills else 0.3

    if job_years > 0 and resume_years >= job_years:
        experience_score = 1.0
    elif job_years > 0 and resume_years > 0:
        experience_score = resume_years / job_years
    else:
        experience_score = 0.5

    overall_match = (semantic_similarity * 0.4) + (keyword_match_score * 0.3) + (experience_score * 0.3)

    # Generate general feedback
    general_feedback = generate_general_feedback(
        overall_match * 100,
        keyword_data["missing_skills"],
        resume_years,
        job_years
    )

    return {
        "match_percentage": round(overall_match * 100, 2),
        "general_feedback": general_feedback
    }