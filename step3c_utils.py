import re
import io
from PyPDF2 import PdfReader
from docx import Document

def extract_text_from_file(file_content, filename):
    """Extract text from PDF, DOCX, or TXT files"""
    if filename.endswith('.pdf'):
        reader = PdfReader(io.BytesIO(file_content))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    elif filename.endswith('.docx'):
        doc = Document(io.BytesIO(file_content))
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    else:
        return file_content.decode('utf-8')

def extract_candidate_name(text):
    """Extract candidate name using improved logic without spaCy"""
    # Look for name patterns in first few non-empty lines
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    for i, line in enumerate(lines[:15]):  # Check first 15 non-empty lines
        words = line.split()
        if 2 <= len(words) <= 4:
            # Check if line looks like a name (contains at least one capital letter, no digits, reasonable length)
            if (all(len(word) >= 2 for word in words) and
                not any(char.isdigit() for char in line) and
                len(line) < 50 and
                any(word[0].isupper() for word in words) and
                not any(keyword in line.lower() for keyword in
                       ['resume', 'cv', 'curriculum', 'vitae', 'linkedin', 'email', 'phone', 'mobile', '@',
                        'objective', 'summary', 'experience', 'education', 'skills', 'certification'])):
                return line
    
    # Fallback: Look for common name patterns in the first 1000 characters
    first_part = text[:1000]
    # Pattern for typical names (Title Case words)
    name_patterns = [
        r'^[A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?(?:\s+[A-Z][a-z]+)?$',  # At beginning of line
        r'\n([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?(?:\s+[A-Z][a-z]+)?)\n'  # Between newlines
    ]
    
    for pattern in name_patterns:
        matches = re.findall(pattern, first_part, re.MULTILINE)
        if matches:
            for match in matches:
                if len(match.split()) >= 2 and len(match) < 50:
                    return match
    
    return "Candidate Name Not Found"

def extract_years_of_experience(text):
    """Extract years of experience from text with improved accuracy"""
    text_lower = text.lower()
    
    # Pattern 1: Direct years of experience
    patterns = [
        r'(\d+)\s*\+?\s*years?[\s\w]*experience',
        r'experience[\s\w]*of[\s\w]*(\d+)\s*\+?\s*years?',
        r'(\d+)\s*-\s*(\d+)\s*years?[\s\w]*experience',
        r'(\d+)\s*\+?\s*years?',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text_lower)
        if matches:
            if isinstance(matches[0], tuple):  # Range like "5-7 years"
                # Get all numbers from tuples and find max
                numbers = []
                for match_tuple in matches:
                    for item in match_tuple:
                        if item.isdigit():
                            numbers.append(int(item))
                if numbers:
                    return max(numbers)
            else:
                # Single number matches
                numbers = [int(match) for match in matches if match.isdigit()]
                if numbers:
                    return max(numbers)
    
    # Pattern 2: Date range calculation
    year_matches = re.findall(r'(19|20)\d{2}', text)
    if year_matches:
        years = sorted([int(year) for year in year_matches if 1900 <= int(year) <= 2030])
        if len(years) >= 2:
            experience = years[-1] - years[0]
            return max(0, min(experience, 40))  # Cap at 40 years
    
    return 0

def extract_current_position(text):
    """Extract current/last position and organization with improved accuracy"""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    position_keywords = [
        'manager', 'engineer', 'developer', 'analyst', 'specialist', 'consultant',
        'director', 'head', 'lead', 'architect', 'officer', 'executive',
        'president', 'ceo', 'cto', 'cfo', 'vp', 'assistant', 'coordinator'
    ]
    
    company_indicators = [
        'ltd', 'limited', 'inc', 'corporation', 'corp', 'company', 'group',
        'technologies', 'solutions', 'systems', 'international', 'global'
    ]
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        
        # Check if line contains position keywords
        if any(keyword in line_lower for keyword in position_keywords):
            position_line = line
            
            # Look for company in current, previous or next lines
            company_candidates = []
            
            # Check current line for company
            if any(indicator in line_lower for indicator in company_indicators):
                company_candidates.append(line)
            
            # Check surrounding lines
            for j in range(max(0, i-2), min(len(lines), i+3)):
                if j == i:
                    continue
                candidate_line = lines[j]
                candidate_lower = candidate_line.lower()
                if (any(indicator in candidate_lower for indicator in company_indicators) and
                    len(candidate_line) > 3 and
                    not any(keyword in candidate_lower for keyword in position_keywords + ['email', 'phone'])):
                    company_candidates.append(candidate_line)
            
            if company_candidates:
                # Use the closest company candidate
                company = company_candidates[0]
                return f"{position_line} | {company}"
            else:
                return position_line
    
    return "Position Not Specified"

def extract_education(text):
    """Extract educational information with improved accuracy"""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    education_keywords = [
        'bachelor', 'bsc', 'bs', 'b.tech', 'btech', 'be',
        'master', 'msc', 'ms', 'm.tech', 'mtech', 'me', 'mba',
        'phd', 'ph.d', 'doctorate',
        'university', 'college', 'institute', 'school',
        'degree', 'graduated', 'education'
    ]
    
    degree_patterns = [
        r'\b(bachelor|bsc|bs|b\.?tech|be)\b',
        r'\b(master|msc|ms|m\.?tech|me|mba)\b',
        r'\b(phd|ph\.d|doctorate)\b'
    ]
    
    education_info = []
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        
        # Check for education keywords
        if any(keyword in line_lower for keyword in education_keywords):
            education_line = line
            
            # Try to find university in current or next line
            university_found = False
            for j in range(i, min(i+3, len(lines))):
                uni_line = lines[j]
                if any(word in uni_line.lower() for word in ['university', 'college', 'institute', 'school']):
                    if uni_line != education_line:
                        education_line += " | " + uni_line
                    university_found = True
                    break
            
            # If no university found, check if current line has degree pattern
            if not university_found:
                for pattern in degree_patterns:
                    if re.search(pattern, line_lower):
                        education_info.append(education_line)
                        break
            else:
                education_info.append(education_line)
    
    return education_info[:2] if education_info else ["Education Not Specified"]

def clean_text_for_similarity(text):
    """Clean and prepare text for semantic analysis"""
    return ' '.join(text.split()[:500])

def generate_general_feedback(match_percentage, missing_skills, total_experience, job_years):
    """Generate concise general feedback"""
    if match_percentage >= 80:
        return "🎯 Strong Match - Highly recommended for immediate interview"
    elif match_percentage >= 65:
        return "✅ Good Fit - Consider for next round with skill validation"
    elif match_percentage >= 50:
        return "⚠️ Moderate Fit - May require additional training"
    elif match_percentage >= 35:
        return "📉 Limited Match - Consider only for junior roles"
    else:
        return "❌ Poor Match - Not recommended for this position"
