from step3a_imports import AnalysisState
from step3b_models import semantic_model
from step3c_utils import clean_text_for_similarity
from sentence_transformers import util

def semantic_analysis_node(state: AnalysisState) -> AnalysisState:
    """Calculate semantic similarity between resume and job description"""
    resume_text = state["resume_text"]
    job_desc = state["job_description"]

    resume_clean = clean_text_for_similarity(resume_text)
    job_clean = clean_text_for_similarity(job_desc)

    if len(resume_clean) < 10 or len(job_clean) < 10:
        return {"semantic_similarity": 0.5}

    resume_embedding = semantic_model.encode(resume_clean, convert_to_tensor=True)
    job_embedding = semantic_model.encode(job_clean, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(resume_embedding, job_embedding).item()

    return {"semantic_similarity": max(0.1, min(1.0, similarity))}