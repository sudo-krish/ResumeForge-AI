"""
Data Transformer
Converts portfolio data format to canonical resume data classes
"""

from typing import Dict, Any, List
from data.data_classes import (
    ResumeData, ContactInfo, ProfessionalSummary, SkillCategory,
    WorkExperience, Project, Education, Certification, Publication, Achievement
)


class PortfolioToResumeTransformer:
    """Transform portfolio data structure to resume data classes"""

    @staticmethod
    def transform(portfolio_data: Dict[str, Any]) -> ResumeData:
        """
        Main transformation function

        Args:
            portfolio_data: Portfolio data dictionary

        Returns:
            ResumeData object
        """
        print("🔄 Transforming portfolio data to resume format...")

        # Transform each section
        contact = PortfolioToResumeTransformer._transform_contact(
            portfolio_data.get('personal', {})
        )

        summary = PortfolioToResumeTransformer._transform_summary(
            portfolio_data.get('personal', {})
        )

        skills = PortfolioToResumeTransformer._transform_skills(
            portfolio_data.get('personal', {})
        )

        experience = PortfolioToResumeTransformer._transform_experience(
            portfolio_data.get('companies', [])
        )

        projects = PortfolioToResumeTransformer._transform_projects(
            portfolio_data.get('projects', [])
        )

        education = PortfolioToResumeTransformer._transform_education(
            portfolio_data.get('education', [])
        )

        certifications = PortfolioToResumeTransformer._transform_certifications(
            portfolio_data.get('certifications', [])
        )

        publications = PortfolioToResumeTransformer._transform_publications(
            portfolio_data.get('researchPapers', [])
        )

        achievements = PortfolioToResumeTransformer._transform_achievements(
            portfolio_data.get('personal', {})
        )

        print("✅ Transformation complete")

        return ResumeData(
            contact=contact,
            summary=summary,
            skills=skills,
            experience=experience,
            projects=projects,
            education=education,
            certifications=certifications,
            publications=publications,
            achievements=achievements
        )

    @staticmethod
    def _transform_contact(personal_data: Dict[str, Any]) -> ContactInfo:
        """Transform contact information"""
        address = personal_data.get('address', {})
        social_links = personal_data.get('socialLinks', {})

        location = f"{address.get('city', 'City')}, {address.get('state', 'State')}"

        return ContactInfo(
            name=personal_data.get('name', 'Your Name'),
            email=personal_data.get('email', 'email@example.com'),
            phone=personal_data.get('phone', '+91-XXXXXXXXXX'),
            location=location,
            linkedin=social_links.get('linkedin'),
            github=social_links.get('github'),
            website=personal_data.get('website'),
            portfolio=personal_data.get('website')
        )

    @staticmethod
    def _transform_summary(personal_data: Dict[str, Any]) -> ProfessionalSummary:
        """Transform professional summary"""
        # Extract job title (first part before |)
        job_title = personal_data.get('jobTitle', 'Professional')
        if '|' in job_title:
            job_title = job_title.split('|')[0].strip()

        # Get top specializations
        top_skills = personal_data.get('topSkills', [])[:4]

        # Get first achievement as key achievement
        achievements = personal_data.get('achievements', [])
        key_achievement = achievements[0] if achievements else "Delivered impactful solutions"

        return ProfessionalSummary(
            title=job_title,
            years_of_experience=personal_data.get('yearsOfExperience', 0),
            specializations=top_skills,
            key_achievement=key_achievement
        )

    @staticmethod
    def _transform_skills(personal_data: Dict[str, Any]) -> List[SkillCategory]:
        """Transform and categorize skills"""
        all_skills = personal_data.get('skills', [])
        top_skills = personal_data.get('topSkills', [])

        # Categorize skills
        categories = {
            'cloud_aws': [],
            'data_engineering': [],
            'programming': [],
            'databases': [],
            'devops': []
        }

        keywords = {
            'cloud_aws': ['AWS', 'Cloud', 'Lambda', 'Glue', 'EMR', 'Kinesis', 'Redshift', 'S3', 'RDS', 'DynamoDB'],
            'data_engineering': ['Kafka', 'Spark', 'Airflow', 'dbt', 'CDC', 'ETL', 'Debezium', 'Pipeline', 'Data Lake',
                                 'Informatica'],
            'programming': ['Python', 'Go', 'SQL', 'PySpark', 'Pandas', 'NumPy', 'Boto3', 'Shell'],
            'databases': ['PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Aurora', 'Parquet', 'Hive'],
            'devops': ['Docker', 'Kubernetes', 'Terraform', 'CI/CD', 'Git']
        }

        # Prioritize top skills
        priority_skills = set(top_skills)

        for skill in all_skills:
            for category, kws in keywords.items():
                if any(kw.lower() in skill.lower() for kw in kws):
                    if any(ts.lower() in skill.lower() for ts in priority_skills):
                        categories[category].insert(0, skill)
                    else:
                        categories[category].append(skill)
                    break

        # Convert to SkillCategory objects
        skill_categories = []
        priority_map = {'cloud_aws': 5, 'data_engineering': 4, 'programming': 3, 'databases': 2, 'devops': 1}
        display_names = {
            'cloud_aws': 'Cloud and AWS',
            'data_engineering': 'Data Engineering',
            'programming': 'Programming Languages',
            'databases': 'Databases',
            'devops': 'DevOps and CI/CD'
        }

        for category, skills_list in categories.items():
            if skills_list:
                skill_categories.append(SkillCategory(
                    category_name=display_names.get(category, category.replace('_', ' ').title()),
                    skills=skills_list[:10],  # Limit per category
                    priority=priority_map.get(category, 0)
                ))

        skill_categories.sort(key=lambda x: x.priority, reverse=True)
        return skill_categories

    @staticmethod
    def _transform_experience(companies_data: List[Dict[str, Any]]) -> List[WorkExperience]:
        """Transform work experience"""
        experiences = []

        for company in companies_data:
            # Extract location from description
            location = "Remote"
            if company.get('description'):
                parts = company.get('description', '').split(',')
                if parts:
                    location = parts[-1].strip()

            experiences.append(WorkExperience(
                position=company.get('position', 'Position'),
                company=company.get('name', 'Company'),
                location=location,
                start_date=company.get('duration', '').split('-')[0].strip() if '-' in company.get('duration',
                                                                                                   '') else '',
                end_date=company.get('duration', '').split('-')[-1].strip() if '-' in company.get('duration',
                                                                                                  '') else 'Present',
                achievements=company.get('responsibilities', [])[:6],  # Max 6 bullets
                technologies=company.get('technologies', []),
                is_current=company.get('current', False)
            ))

        return experiences

    @staticmethod
    def _transform_projects(projects_data: List[Dict[str, Any]]) -> List[Project]:
        """Transform projects"""
        projects = []

        for proj in projects_data:
            # Combine technologies and languages
            all_tech = proj.get('technologies', []) + proj.get('languages', [])

            projects.append(Project(
                name=proj.get('name', 'Project'),
                description=proj.get('description', ''),
                technologies=all_tech[:8],  # Limit tech stack
                metrics=proj.get('metrics', {}),
                url=proj.get('repository') or proj.get('url'),
                is_featured=proj.get('featured', False)
            ))

        return projects

    @staticmethod
    def _transform_education(education_data: List[Dict[str, Any]]) -> List[Education]:
        """Transform education"""
        education_list = []

        for edu in education_data:
            education_list.append(Education(
                degree=edu.get('degree', 'Bachelor of Technology'),
                field=edu.get('field', 'Computer Science'),
                institution=edu.get('university', 'University'),
                location=edu.get('location', ''),
                graduation_year=edu.get('graduationYear', ''),
                gpa=edu.get('gpa'),
                relevant_coursework=edu.get('coursework', [])
            ))

        return education_list

    @staticmethod
    def _transform_certifications(certifications_data: List[Dict[str, Any]]) -> List[Certification]:
        """Transform certifications"""
        certifications = []

        for cert in certifications_data:
            certifications.append(Certification(
                name=cert.get('name', ''),
                issuer=cert.get('issuer', ''),
                date_issued=cert.get('dateIssued', ''),
                credential_id=cert.get('credentialId'),
                url=cert.get('url')
            ))

        return certifications

    @staticmethod
    def _transform_publications(research_papers: List[Dict[str, Any]]) -> List[Publication]:
        """Transform research papers/publications"""
        publications = []

        for paper in research_papers:
            publications.append(Publication(
                title=paper.get('title', ''),
                publication_venue=paper.get('journal', ''),
                date_published=str(paper.get('datePublished', '')),
                authors=paper.get('authors', []),
                url=paper.get('url')
            ))

        return publications

    @staticmethod
    def _transform_achievements(personal_data: Dict[str, Any]) -> List[Achievement]:
        """Transform achievements"""
        achievements_list = []

        for achievement in personal_data.get('achievements', [])[1:]:  # Skip first (used in summary)
            achievements_list.append(Achievement(
                description=achievement,
                category="professional"
            ))

        return achievements_list
