import streamlit as st
import pandas as pd
from resume_analyzer import resume_analyzer_app, extract_text_from_file
import plotly.graph_objects as go
import time
import io
from datetime import datetime

st.set_page_config(
    page_title="U&I Garments - Bulk Resume Analyzer",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium CSS Styling
st.markdown("""
<style>
    /* Main Theme Colors */
    :root {
        --primary: #8B4513;
        --secondary: #D2691E;
        --accent: #F4A460;
        --dark: #2F4F4F;
        --light: #FFF8DC;
    }

    .main-header {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(139, 69, 19, 0.3);
    }

    .main-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        font-family: 'Georgia', serif;
    }

    .main-subtitle {
        font-size: 1.4rem;
        opacity: 0.95;
        font-weight: 300;
    }

    .brand-section {
        background: linear-gradient(135deg, var(--dark) 0%, #708090 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }

    .brand-tag {
        background: rgba(255,255,255,0.2);
        color: white;
        padding: 0.5rem 1.2rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 500;
        margin: 0.3rem;
        display: inline-block;
        border: 1px solid rgba(255,255,255,0.3);
    }

    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(139, 69, 19, 0.1);
        border: 1px solid #eaeaea;
        margin-bottom: 2rem;
        text-align: center;
        height: 100%;
        transition: all 0.3s ease;
        border-left: 4px solid var(--primary);
    }

    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(139, 69, 19, 0.15);
    }

    .section-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(139, 69, 19, 0.08);
        border: 1px solid #eaeaea;
        margin-bottom: 2rem;
        border-left: 4px solid var(--secondary);
    }

    .metric-card {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(139, 69, 19, 0.2);
    }

    .metric-value {
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
        font-family: 'Georgia', serif;
    }

    .metric-label {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0;
        font-weight: 300;
    }

    .analyze-btn {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
        border: none;
        padding: 1rem 2.5rem;
        border-radius: 30px;
        font-weight: 600;
        font-size: 1.2rem;
        transition: all 0.3s ease;
        display: inline-block;
        text-decoration: none;
        box-shadow: 0 4px 15px rgba(139, 69, 19, 0.3);
        width: 100%;
    }

    .analyze-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(139, 69, 19, 0.4);
        color: white;
    }

    .skill-tag {
        background: var(--primary);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
        display: inline-block;
        margin: 0.2rem;
    }

    .skill-tag.missing {
        background: #DC143C;
    }

    .skill-tag.present {
        background: #228B22;
    }

    .high-match { background-color: #d4edda !important; }
    .low-match { background-color: #f8d7da !important; }

    .stButton button {
        width: 100%;
    }

    /* File uploader styling */
    .stFileUploader {
        border: 2px dashed #8B4513;
        border-radius: 10px;
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Premium Header Section
    st.markdown("""
    <div class='main-header'>
        <div class='main-title'>U&I GARMENTS</div>
        <div class='main-subtitle'>AI-Powered Bulk Resume Analyzer</div>
        <p style='font-size: 1.1rem; margin-top: 1rem; opacity: 0.9;'>
            Premium Talent Assessment for Pakistan's Leading Fashion Retail Group
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Brands Showcase
    st.markdown("""
    <div class='brand-section'>
        <h3 style='color: white; margin-bottom: 1.5rem;'>OUR PRESTIGIOUS BRANDS PORTFOLIO</h3>
        <div>
            <span class='brand-tag'>Junaid Jamshed</span>
            <span class='brand-tag'>Almirah</span>
            <span class='brand-tag'>Cast & Crew</span>
            <span class='brand-tag'>Panjnad</span>
            <span class='brand-tag'>Al-Tayyab Beauty</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Features Section
    st.markdown("## 🎯 HR Excellence Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='feature-card'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem; color: #8B4513;'>📊</div>
            <div style='font-size: 1.3rem; font-weight: 600; color: #2F4F4F; margin-bottom: 1rem;'>Bulk Processing</div>
            <p>Analyze multiple resumes simultaneously against job requirements with AI-powered matching</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='feature-card'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem; color: #8B4513;'>👔</div>
            <div style='font-size: 1.3rem; font-weight: 600; color: #2F4F4F; margin-bottom: 1rem;'>Smart Extraction</div>
            <p>Automatically extract candidate names, experience, education, and current positions</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='feature-card'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem; color: #8B4513;'>⚡</div>
            <div style='font-size: 1.3rem; font-weight: 600; color: #2F4F4F; margin-bottom: 1rem;'>Instant Results</div>
            <p>Get comprehensive candidate comparison tables with match scores and skill gaps</p>
        </div>
        """, unsafe_allow_html=True)

    # Initialize session state
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = []
    if 'job_description' not in st.session_state:
        st.session_state.job_description = ""
    if 'processed_files' not in st.session_state:
        st.session_state.processed_files = set()

    # Main Input Section - CORRECTED LOGIC
    st.markdown("---")
    st.markdown("## 📋 Job & Resume Input")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🎯 Job Description")

        # SINGLE file upload for JD
        jd_file = st.file_uploader(
            "Upload Job Description File",
            type=['pdf', 'docx', 'txt'],
            key="jd_upload",
            help="Upload a single PDF, DOCX, or TXT file containing the job description"
        )

        if jd_file:
            job_description = extract_text_from_file(jd_file.getvalue(), jd_file.name)
            st.session_state.job_description = job_description
            st.success(f"✅ Job Description loaded from file ({len(job_description)} characters)")
        else:
            # Text area for manual JD input
            job_description = st.text_area(
                "Or paste Job Description here:",
                height=200,
                value=st.session_state.job_description,
                placeholder="Paste the complete job description here...\n\nInclude:\n• Required skills\n• Experience level\n• Qualifications\n• Responsibilities",
                help="Paste the job description text directly or upload a file above"
            )
            st.session_state.job_description = job_description

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("📄 Candidate Resumes")

        # MULTIPLE file upload for resumes - CORRECTED
        uploaded_resumes = st.file_uploader(
            "Upload Multiple Resume Files",
            type=['pdf', 'docx', 'txt'],
            accept_multiple_files=True,
            key="resume_upload",
            help="Select multiple PDF, DOCX, or TXT files containing candidate resumes"
        )

        if uploaded_resumes:
            st.success(f"✅ {len(uploaded_resumes)} resume(s) selected for analysis")

            # Show uploaded resume files
            st.markdown("**Selected Resume Files:**")
            for i, file in enumerate(uploaded_resumes):
                st.write(f"{i+1}. {file.name}")

        st.markdown('</div>', unsafe_allow_html=True)

    # Analysis Controls
    st.markdown("---")
    st.markdown("## 🔍 Analysis Control Center")

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.info("""
        **Ready to analyze?**
        - Ensure job description is entered/uploaded
        - Select multiple resume files
        - Click 'Analyze All Resumes' to start bulk processing
        """)

    with col2:
        analyze_all = st.button("🚀 Analyze All Resumes", use_container_width=True, type="primary")

    with col3:
        if st.button("🔄 Clear Results", use_container_width=True):
            st.session_state.analysis_results = []
            st.session_state.processed_files = set()
            st.rerun()

    # Process Analysis - CORRECTED LOGIC
    if analyze_all and uploaded_resumes and st.session_state.job_description:
        progress_bar = st.progress(0)
        status_text = st.empty()

        results = []
        total_files = len(uploaded_resumes)

        for i, resume_file in enumerate(uploaded_resumes):
            # Skip if already processed
            if resume_file.name in st.session_state.processed_files:
                continue

            status_text.text(f"🔍 Analyzing {i+1}/{total_files}: {resume_file.name}")
            progress_bar.progress((i) / total_files)

            try:
                # Extract text from RESUME (not JD) - CORRECTED
                resume_text = extract_text_from_file(resume_file.getvalue(), resume_file.name)

                if not resume_text or len(resume_text.strip()) < 50:
                    st.warning(f"⚠️ Skipping {resume_file.name} - insufficient text content")
                    continue

                # Analyze resume against JD - CORRECTED
                analysis_result = resume_analyzer_app.invoke({
                    "resume_text": resume_text,  # This is the candidate's resume
                    "job_description": st.session_state.job_description  # This is the JD
                })

                # Add file information - CORRECTED (resume file name)
                analysis_result['resume_filename'] = resume_file.name  # Store resume filename
                analysis_result['processed_date'] = datetime.now().strftime("%Y-%m-%d %H:%M")

                results.append(analysis_result)
                st.session_state.processed_files.add(resume_file.name)

            except Exception as e:
                st.error(f"❌ Error processing {resume_file.name}: {str(e)}")

        # Update session state
        st.session_state.analysis_results.extend(results)

        progress_bar.progress(100)
        status_text.text(f"✅ Analysis complete! Processed {len(results)} resumes")
        time.sleep(1)
        st.rerun()

    # Display Results - UPDATED: Only 4 columns
    if st.session_state.analysis_results:
        st.markdown("---")
        st.markdown("## 📊 Candidate Analysis Results")

        # Create results dataframe - UPDATED: Only 4 columns as requested
        results_data = []
        for result in st.session_state.analysis_results:
            results_data.append({
                'Resume File': result.get('resume_filename', 'Unknown'),
                'Overall Fit Score': f"{result['match_percentage']}%",
                'Experience Relevance': f"{int(result['semantic_similarity'] * 100)}%",
                'Missing Skills': ', '.join(result.get('missing_skills', []))[:80] + ('...' if len(', '.join(result.get('missing_skills', []))) > 80 else '') if result.get('missing_skills') else 'None'
            })

        df = pd.DataFrame(results_data)

        # Sort by match percentage
        df['SortScore'] = df['Overall Fit Score'].str.replace('%', '').astype(float)
        df = df.sort_values('SortScore', ascending=False).drop('SortScore', axis=1)

        # Display metrics - FIXED: Correct calculation for weak matches
        st.markdown("### 📈 Summary Metrics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            avg_match = df['Overall Fit Score'].str.replace('%', '').astype(float).mean()
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{avg_match:.1f}%</div>
                <div class='metric-label'>Average Match</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            total_candidates = len(df)
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{total_candidates}</div>
                <div class='metric-label'>Total Candidates</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            strong_matches = len(df[df['Overall Fit Score'].str.replace('%', '').astype(float) >= 70])
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{strong_matches}</div>
                <div class='metric-label'>Strong Matches</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            # FIXED: Changed to calculate weak matches correctly (<70%)
            weak_matches = len(df[df['Overall Fit Score'].str.replace('%', '').astype(float) < 70])
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{weak_matches}</div>
                <div class='metric-label'>Weak Matches</div>
            </div>
            """, unsafe_allow_html=True)

        # Display results table - UPDATED: Only 4 columns
        st.markdown("### 👥 Candidate Comparison Table")

        # Add styling to table based on match score
        def color_rows(row):
            score = float(row['Overall Fit Score'].replace('%', ''))
            if score >= 70:
                return ['background-color: #d4edda'] * len(row)
            else:
                return ['background-color: #f8d7da'] * len(row)

        styled_df = df.style.apply(color_rows, axis=1)
        st.dataframe(styled_df, use_container_width=True, height=400)

        # Download results - UPDATED: Only Excel export
        st.markdown("### 📥 Export Results")

        # Create Excel file with formatting
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Resume Analysis', index=False)

            # Get workbook and worksheet
            workbook = writer.book
            worksheet = writer.sheets['Resume Analysis']

            # Add formats
            high_match_format = workbook.add_format({'bg_color': '#d4edda'})
            low_match_format = workbook.add_format({'bg_color': '#f8d7da'})

            # Apply formatting based on match score
            for row_num in range(1, len(df) + 1):
                score = float(df.iloc[row_num-1]['Overall Fit Score'].replace('%', ''))
                if score >= 70:
                    worksheet.set_row(row_num, None, high_match_format)
                else:
                    worksheet.set_row(row_num, None, low_match_format)

            # Auto-adjust column widths
            for i, col in enumerate(df.columns):
                max_len = max(df[col].astype(str).str.len().max(), len(col)) + 2
                worksheet.set_column(i, i, min(max_len, 50))

        excel_data = output.getvalue()
        st.download_button(
            label="📊 Download Excel Report",
            data=excel_data,
            file_name=f"resume_analysis_results_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mime="application/vnd.ms-excel",
            use_container_width=True
        )

    else:
        # Show instructions when no results
        st.markdown("---")
        st.markdown("## 📝 How to Use the Bulk Resume Analyzer")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div class='section-card'>
                <h4>🚀 Quick Start Guide</h4>
                <p>1. <strong>Enter Job Description</strong> - Paste or upload the job requirements</p>
                <p>2. <strong>Upload Multiple Resumes</strong> - Select multiple PDF/DOCX files</p>
                <p>3. <strong>Analyze All</strong> - Click the analyze button to process all resumes</p>
                <p>4. <strong>Review Results</strong> - See sorted candidate table with match scores</p>
                <p>5. <strong>Export Data</strong> - Download results for further analysis</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class='section-card'>
                <h4>🎯 What We Extract</h4>
                <p>• <strong>Resume Files</strong> - Original file names for easy identification</p>
                <p>• <strong>Overall Fit Score</strong> - Comprehensive matching percentage</p>
                <p>• <strong>Experience Relevance</strong> - Semantic match to job requirements</p>
                <p>• <strong>Missing Skills</strong> - Critical skills gap analysis</p>
            </div>
            """, unsafe_allow_html=True)

    # Premium Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem; background: #f8f9fa; border-radius: 10px; margin-top: 2rem;'>
        <h4 style='color: #8B4513; margin-bottom: 1rem;'>U&I GARMENTS PVT. LTD.</h4>
        <p style='margin: 0.5rem 0;'>Elevating Fashion Retail Through Intelligent Talent Acquisition</p>
        <div style='margin-top: 1rem; font-size: 0.9rem; color: #888;'>
            <strong>Our Brands:</strong> Junaid Jamshed • Almirah • Cast & Crew • Panjnad • Al-Tayyab Beauty
        </div>
        <p style='margin-top: 1rem; font-size: 0.8rem; color: #999;'>
            AI-Powered HR Tool • Confidential • For Internal Use Only
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()