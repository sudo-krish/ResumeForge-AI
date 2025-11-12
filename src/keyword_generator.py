"""
AI-Powered Keyword Generator
Analyzes job role and generates optimal keywords for resume optimization
"""

from typing import List, Dict, Set, Tuple
from dataclasses import dataclass
from collections import defaultdict

from src.ai_integration import AIResumeAssistant


@dataclass
class KeywordProfile:
    """Generated keyword profile for a job role"""
    role: str
    primary_keywords: List[str]  # Must appear 2-3x
    secondary_keywords: List[str]  # Should appear 1-2x
    technical_skills: List[str]  # Technical competencies
    power_verbs: Dict[str, List[str]]  # Categorized power verbs
    industry_buzzwords: List[str]  # 2025 trending terms
    synonyms: Dict[str, List[str]]  # Keyword variations to avoid repetition


class AIKeywordGenerator:
    """
    Intelligent keyword generator for any job role

    Analyzes:
    - Job role requirements
    - Industry trends (2025)
    - User's actual experience
    - ATS optimization needs
    """

    # Industry-specific keyword databases
    INDUSTRY_KEYWORDS = {
        'data_engineer': {
            'hot_2025': ['AI', 'ML', 'LLM', 'GenAI', 'RAG', 'Vector Database',
                         'Real-time', 'Streaming', 'Event-driven', 'Cloud-native'],
            'core_tech': ['Spark', 'Kafka', 'Airflow', 'dbt', 'Redshift', 'Snowflake'],
            'cloud': ['AWS', 'Azure', 'GCP', 'Kubernetes', 'Docker', 'Terraform'],
        },
        'software_engineer': {
            'hot_2025': ['AI', 'ML', 'Microservices', 'Cloud-native', 'DevOps', 'CI/CD'],
            'core_tech': ['Python', 'Java', 'React', 'Node.js', 'GraphQL', 'REST APIs'],
            'cloud': ['AWS', 'Kubernetes', 'Docker', 'Serverless'],
        },
        'machine_learning_engineer': {
            'hot_2025': ['LLM', 'GenAI', 'Transformers', 'RAG', 'Fine-tuning', 'MLOps'],
            'core_tech': ['PyTorch', 'TensorFlow', 'Scikit-learn', 'MLflow', 'Kubeflow'],
            'cloud': ['AWS SageMaker', 'Azure ML', 'GCP Vertex AI'],
        },
        # Add more roles as needed
    }

    def __init__(self, ai_assistant: AIResumeAssistant):
        """Initialize with AI assistant"""
        self.ai = ai_assistant

    def generate_keywords(
            self,
            job_role: str,
            job_description: str = "",
            user_experience: Dict = None,
            target_company: str = "FAANG"
    ) -> KeywordProfile:
        """
        Generate optimized keyword profile for job role

        Args:
            job_role: Target job role (e.g., "Data Engineer", "ML Engineer")
            job_description: Optional job posting text
            user_experience: User's actual experience data
            target_company: Target company type (FAANG, startup, enterprise)

        Returns:
            KeywordProfile with all optimized keywords
        """
        print(f"\n🔍 Generating keywords for: {job_role}")

        # Normalize role
        role_key = self._normalize_role(job_role)

        # Step 1: Get base keywords from database
        base_keywords = self._get_base_keywords(role_key)

        # Step 2: Extract keywords from job description (if provided)
        jd_keywords = self._extract_jd_keywords(job_description) if job_description else []

        # Step 3: Analyze user's experience for authentic keywords
        experience_keywords = self._extract_experience_keywords(user_experience) if user_experience else []

        # Step 4: AI-powered keyword enrichment
        enriched_keywords = self._ai_enrich_keywords(
            job_role, base_keywords, jd_keywords, experience_keywords, target_company
        )

        # Step 5: Build final keyword profile
        profile = self._build_keyword_profile(
            job_role, enriched_keywords, experience_keywords
        )

        self._print_keyword_summary(profile)

        return profile

    def _normalize_role(self, job_role: str) -> str:
        """Normalize job role to database key"""
        role_lower = job_role.lower().replace(' ', '_')

        # Map variations
        if 'data' in role_lower and 'engineer' in role_lower:
            return 'data_engineer'
        elif 'machine' in role_lower or 'ml' in role_lower:
            return 'machine_learning_engineer'
        elif 'software' in role_lower or 'backend' in role_lower or 'fullstack' in role_lower:
            return 'software_engineer'
        else:
            return 'data_engineer'  # Default

    def _get_base_keywords(self, role_key: str) -> Dict:
        """Get base keywords from database"""
        return self.INDUSTRY_KEYWORDS.get(role_key, self.INDUSTRY_KEYWORDS['data_engineer'])

    def _extract_jd_keywords(self, job_description: str) -> List[str]:
        """Extract keywords from job description"""
        # Simple extraction (can be enhanced with NLP)
        keywords = []

        # Common technical terms
        tech_terms = [
            'Python', 'Java', 'SQL', 'AWS', 'Azure', 'GCP', 'Kubernetes', 'Docker',
            'Kafka', 'Spark', 'Airflow', 'dbt', 'Redshift', 'Snowflake', 'BigQuery',
            'Machine Learning', 'AI', 'ML', 'LLM', 'GenAI', 'RAG', 'Vector Database',
            'Real-time', 'Streaming', 'ETL', 'Data Pipeline', 'Data Warehouse'
        ]

        jd_lower = job_description.lower()
        for term in tech_terms:
            if term.lower() in jd_lower:
                keywords.append(term)

        return list(set(keywords))

    def _extract_experience_keywords(self, experience: Dict) -> List[str]:
        """Extract keywords from user's actual experience"""
        keywords = set()

        if not experience:
            return []

        # Extract from skills
        if 'skills' in experience:
            for skill in experience['skills']:
                if isinstance(skill, str):
                    keywords.add(skill)

        # Extract from technologies
        if 'technologies' in experience:
            keywords.update(experience['technologies'])

        # Extract from achievements
        if 'achievements' in experience:
            for achievement in experience['achievements']:
                # Extract tech terms from achievement text
                words = str(achievement).split()
                for word in words:
                    if word[0].isupper() and len(word) > 3:  # Likely a tech term
                        keywords.add(word)

        return list(keywords)

    def _ai_enrich_keywords(
            self,
            job_role: str,
            base_keywords: Dict,
            jd_keywords: List[str],
            experience_keywords: List[str],
            target_company: str
    ) -> Dict:
        """Use AI to enrich and prioritize keywords"""

        context = f"""
JOB ROLE: {job_role}
TARGET COMPANY: {target_company}
BASE KEYWORDS: {', '.join(base_keywords.get('hot_2025', []))}
JOB DESCRIPTION KEYWORDS: {', '.join(jd_keywords[:20])}
USER'S EXPERIENCE KEYWORDS: {', '.join(experience_keywords[:20])}
"""

        prompt = f"""You are an expert resume keyword optimizer for 2025.

{context}

Generate an optimized keyword list for this role that:
1. Balances trending 2025 keywords with foundational skills
2. Matches job description requirements (if provided)
3. Stays authentic to user's actual experience
4. Optimizes for ATS (Applicant Tracking Systems)
5. Includes industry-standard synonyms to avoid keyword stuffing

OUTPUT FORMAT (JSON):
{{
    "primary_keywords": ["keyword1", "keyword2", ...],  // Must appear 2-3x
    "secondary_keywords": ["keyword3", "keyword4", ...],  // Should appear 1-2x
    "technical_skills": ["skill1", "skill2", ...],
    "power_verbs": {{
        "Leadership": ["verb1", "verb2"],
        "Technical": ["verb3", "verb4"],
        "Optimization": ["verb5", "verb6"]
    }},
    "industry_buzzwords": ["buzzword1", "buzzword2", ...],
    "synonyms": {{
        "real-time": ["streaming", "low-latency", "instant"],
        "cloud": ["cloud-native", "serverless", "distributed"]
    }}
}}

Only output valid JSON, no markdown or explanation."""

        try:
            response = self.ai.generate_content("keyword_generation", prompt, "")

            # Parse JSON response
            import json
            import re

            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                keywords_dict = json.loads(json_match.group())
                return keywords_dict
            else:
                # Fallback to base keywords
                return self._fallback_keywords(base_keywords)

        except Exception as e:
            print(f"   ⚠️  AI enrichment failed: {e}, using base keywords")
            return self._fallback_keywords(base_keywords)

    def _fallback_keywords(self, base_keywords: Dict) -> Dict:
        """Fallback keyword structure"""
        return {
            'primary_keywords': base_keywords.get('hot_2025', [])[:8],
            'secondary_keywords': base_keywords.get('core_tech', [])[:10],
            'technical_skills': base_keywords.get('cloud', [])[:8],
            'power_verbs': {
                'Leadership': ['Led', 'Spearheaded', 'Drove'],
                'Technical': ['Architected', 'Engineered', 'Built', 'Designed'],
                'Optimization': ['Optimized', 'Enhanced', 'Streamlined']
            },
            'industry_buzzwords': ['AI', 'ML', 'Cloud-native', 'Real-time'],
            'synonyms': {
                'real-time': ['streaming', 'low-latency', 'instant'],
                'cloud': ['cloud-native', 'serverless', 'distributed']
            }
        }

    def _build_keyword_profile(
            self,
            job_role: str,
            enriched_keywords: Dict,
            experience_keywords: List[str]
    ) -> KeywordProfile:
        """Build final keyword profile"""

        return KeywordProfile(
            role=job_role,
            primary_keywords=enriched_keywords.get('primary_keywords', []),
            secondary_keywords=enriched_keywords.get('secondary_keywords', []),
            technical_skills=enriched_keywords.get('technical_skills', []),
            power_verbs=enriched_keywords.get('power_verbs', {}),
            industry_buzzwords=enriched_keywords.get('industry_buzzwords', []),
            synonyms=enriched_keywords.get('synonyms', {})
        )

    def _print_keyword_summary(self, profile: KeywordProfile):
        """Print keyword profile summary"""
        print(f"\n✅ Keyword Profile Generated:")
        print(f"   Primary Keywords (2-3x): {len(profile.primary_keywords)}")
        print(f"   Secondary Keywords (1-2x): {len(profile.secondary_keywords)}")
        print(f"   Technical Skills: {len(profile.technical_skills)}")
        print(f"   Power Verb Categories: {len(profile.power_verbs)}")
        print(f"   Synonyms: {len(profile.synonyms)} groups")

        print(f"\n   Top Keywords: {', '.join(profile.primary_keywords[:5])}")
