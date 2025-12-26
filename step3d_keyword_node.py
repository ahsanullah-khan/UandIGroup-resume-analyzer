from step3a_imports import AnalysisState
from step3c_utils import extract_years_of_experience, extract_candidate_name, extract_current_position, extract_education
import re

def keyword_extraction_node(state: AnalysisState) -> AnalysisState:
    """Extract keywords and skills from resume and job description"""
    resume_text = state["resume_text"].lower()
    job_desc = state["job_description"].lower()

    # Comprehensive skills database
    technical_skills = [
        # Programming Languages
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'rust', 'kotlin', 'swift',
        'php', 'ruby', 'scala', 'r', 'matlab', 'perl', 'haskell', 'dart', 'elixir',

        # Web Development
        'html', 'css', 'sass', 'less', 'bootstrap', 'tailwind', 'react', 'angular', 'vue', 'svelte',
        'node.js', 'express', 'django', 'flask', 'fastapi', 'spring', 'laravel', 'ruby on rails',
        'asp.net', 'jquery', 'ember', 'backbone', 'meteor',

        # Mobile Development
        'react native', 'flutter', 'ionic', 'xamarin', 'android', 'ios', 'swiftui', 'kotlin multiplatform',

        # Databases
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'cassandra', 'oracle', 'sql server', 'sqlite',
        'dynamodb', 'cosmos db', 'firebase', 'elasticsearch', 'snowflake', 'bigquery',

        # Cloud & DevOps
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'github', 'gitlab', 'bitbucket',
        'terraform', 'ansible', 'puppet', 'chef', 'circleci', 'travis ci', 'github actions',
        'aws ec2', 'aws s3', 'aws lambda', 'aws rds', 'aws dynamodb', 'azure functions', 'google cloud functions',

        # AI/ML
        'machine learning', 'deep learning', 'artificial intelligence', 'neural networks', 'nlp', 'computer vision',
        'tensorflow', 'pytorch', 'scikit-learn', 'keras', 'opencv', 'nltk', 'spacy', 'hugging face',
        'pandas', 'numpy', 'matplotlib', 'seaborn', 'plotly', 'jupyter', 'colab',

        # Data Science
        'data analysis', 'data visualization', 'statistics', 'big data', 'hadoop', 'spark', 'kafka',
        'tableau', 'power bi', 'looker', 'qlik', 'excel', 'airflow', 'databricks',

        # Backend & APIs
        'rest', 'graphql', 'soap', 'grpc', 'microservices', 'api development', 'serverless',
        'message queue', 'rabbitmq', 'kafka', 'redis', 'nginx', 'apache',

        # Testing
        'unit testing', 'integration testing', 'selenium', 'cypress', 'jest', 'mocha', 'junit', 'pytest',
        'test driven development', 'quality assurance', 'automated testing',

        # Security
        'cybersecurity', 'penetration testing', 'ethical hacking', 'owasp', 'encryption', 'ssl/tls',
        'firewalls', 'vpn', 'identity management', 'oauth', 'jwt',

        # Tools & Platforms
        'linux', 'unix', 'windows server', 'macos', 'vmware', 'virtualbox', 'vagrant',
        'postman', 'swagger', 'insomnia', 'jira', 'confluence', 'slack', 'teams',

        # Methodologies
        'agile', 'scrum', 'kanban', 'waterfall', 'devops', 'ci/cd', 'tdd', 'bdd'
    ]

    hr_skills = [
        # Recruitment & Talent
        'recruitment', 'hiring', 'talent acquisition', 'sourcing', 'headhunting', 'staffing',
        'interviewing', 'candidate screening', 'onboarding', 'background checks',

        # HR Management
        'employee relations', 'hr', 'human resources', 'performance management', 'succession planning',
        'workforce planning', 'employee engagement', 'labor relations', 'hr policies', 'talent management',

        # Compensation & Benefits
        'compensation', 'employee benefits', 'payroll', 'salary benchmarking', 'incentive plans', 'health insurance',
        'retirement plans', 'employee benefits',

        # Training & Development
        'training', 'development', 'learning management', 'career development', 'leadership development',
        'skills assessment', 'performance reviews', 'employee training',

        # HR Analytics
        'hr analytics', 'workforce analytics', 'employee retention', 'turnover analysis', 'hr metrics',
        'diversity and inclusion', 'hr reporting',

        # Compliance & Legal
        'employment law', 'hr compliance', 'labor law', 'workplace safety', 'osha', 'eeoc compliance',

        # HR Systems
        'workday', 'sap successfactors', 'oracle hcm', 'adp', 'bamboo hr', 'gusto', 'paychex',
        'hr information systems', 'ats systems'
    ]

    business_skills = [
        # Project Management
        'project management', 'pm', 'project planning', 'risk management', 'budget management',
        'stakeholder management', 'resource allocation', 'project lifecycle',

        # Product Management
        'product management', 'product strategy', 'roadmapping', 'user stories', 'backlog grooming',
        'agile methodology', 'scrum master', 'product owner',

        # Business Analysis
        'business analysis', 'requirements gathering', 'process improvement', 'business process modeling',
        'use cases', 'user acceptance testing', 'gap analysis',

        # Sales & Marketing
        'sales', 'business development', 'account management', 'client relations', 'customer success',
        'digital marketing', 'seo', 'sem', 'social media marketing', 'content marketing', 'email marketing',
        'marketing automation', 'google analytics', 'crm', 'salesforce', 'hubspot',

        # Finance & Accounting
        'financial analysis', 'accounting', 'bookkeeping', 'financial reporting', 'budgeting', 'forecasting',
        'quickbooks', 'xero', 'sap fico', 'financial modeling',

        # Operations
        'operations management', 'supply chain', 'logistics', 'inventory management', 'quality control',
        'six sigma', 'lean manufacturing', 'process optimization'
    ]

    soft_skills = [
        'leadership', 'team management', 'communication', 'presentation', 'public speaking',
        'problem solving', 'critical thinking', 'analytical skills', 'time management',
        'collaboration', 'teamwork', 'adaptability', 'creativity', 'innovation',
        'emotional intelligence', 'conflict resolution', 'negotiation', 'decision making'
    ]

    # Combine all skills
    all_skills = technical_skills + hr_skills + business_skills + soft_skills

    resume_skills = [skill for skill in all_skills if re.search(r'\b' + re.escape(skill) + r'\b', resume_text)]
    required_skills = [skill for skill in all_skills if re.search(r'\b' + re.escape(skill) + r'\b', job_desc)]
    missing_skills = [skill for skill in required_skills if skill not in resume_skills]

    resume_years = extract_years_of_experience(state["resume_text"])
    job_years = extract_years_of_experience(job_desc)

    # Extract candidate information
    candidate_name = extract_candidate_name(state["resume_text"])
    current_position = extract_current_position(state["resume_text"])
    education = extract_education(state["resume_text"])

    return {
        "keyword_matches": {
            "resume_skills": resume_skills,
            "required_skills": required_skills,
            "missing_skills": missing_skills,
            "resume_years": resume_years,
            "job_years": job_years
        },
        "candidate_name": candidate_name,
        "total_experience": resume_years,
        "current_position": current_position,
        "education": education
    }