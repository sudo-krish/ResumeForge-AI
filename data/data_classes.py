"""
Data Classes for Resume Generation
Defines the canonical structure for resume data (generic, reusable)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import date


@dataclass
class ContactInfo:
    """Contact information"""
    name: str
    email: str
    phone: str
    location: str  # City, State format
    linkedin: Optional[str] = None
    github: Optional[str] = None
    website: Optional[str] = None
    portfolio: Optional[str] = None


@dataclass
class ProfessionalSummary:
    """Professional summary/headline"""
    title: str  # Job title (e.g., "Senior Data Engineer")
    years_of_experience: int
    specializations: List[str]  # Top 3-4 specializations
    key_achievement: str  # One quantified achievement


@dataclass
class SkillCategory:
    """Categorized skills"""
    category_name: str  # e.g., "Cloud & AWS", "Programming Languages"
    skills: List[str]  # List of skills in this category
    priority: int = 0  # Higher = more important


@dataclass
class WorkExperience:
    """Work experience entry"""
    position: str
    company: str
    location: str
    start_date: str  # e.g., "Jan 2024"
    end_date: str  # e.g., "Present" or "Dec 2024"
    achievements: List[str]  # 3-6 bullet points with metrics
    technologies: List[str]  # Technologies used
    is_current: bool = False


@dataclass
class Project:
    """Project entry"""
    name: str
    description: str  # One-line description with impact
    technologies: List[str]  # Tech stack
    metrics: Dict[str, str] = field(default_factory=dict)  # Quantified metrics
    url: Optional[str] = None
    is_featured: bool = False


@dataclass
class Education:
    """Education entry"""
    degree: str  # Full degree name
    field: str  # Field of study
    institution: str
    location: str
    graduation_year: str
    gpa: Optional[str] = None
    relevant_coursework: List[str] = field(default_factory=list)


@dataclass
class Certification:
    """Certification entry"""
    name: str  # Full certification name
    issuer: str  # Issuing organization
    date_issued: str
    credential_id: Optional[str] = None
    url: Optional[str] = None


@dataclass
class Publication:
    """Research publication or blog post"""
    title: str
    publication_venue: str  # Journal, conference, or blog
    date_published: str
    authors: List[str] = field(default_factory=list)
    url: Optional[str] = None


@dataclass
class Achievement:
    """Additional achievement or award"""
    description: str  # Brief description with metrics
    category: str = "general"  # e.g., "award", "leadership", "contribution"


@dataclass
class ResumeData:
    """
    Complete resume data structure
    This is the canonical format the resume generator expects
    """
    contact: ContactInfo
    summary: ProfessionalSummary
    skills: List[SkillCategory]
    experience: List[WorkExperience]
    projects: List[Project]
    education: List[Education]
    certifications: List[Certification] = field(default_factory=list)
    publications: List[Publication] = field(default_factory=list)
    achievements: List[Achievement] = field(default_factory=list)

    def __post_init__(self):
        """Validate data after initialization"""
        # Ensure experience is in reverse chronological order
        # You can add more validations here
        pass


# Utility functions for data classes

def create_contact_info(name: str, email: str, phone: str, location: str, **kwargs) -> ContactInfo:
    """Factory function for ContactInfo with validation"""
    return ContactInfo(
        name=name,
        email=email,
        phone=phone,
        location=location,
        **kwargs
    )


def create_skill_categories(skills_dict: Dict[str, List[str]]) -> List[SkillCategory]:
    """
    Convert skills dictionary to SkillCategory list

    Args:
        skills_dict: Dict with category names as keys, skill lists as values

    Returns:
        List of SkillCategory objects
    """
    categories = []
    priority_order = {
        'cloud': 5,
        'data_engineering': 4,
        'programming': 3,
        'databases': 2,
        'devops': 1
    }

    for idx, (category_key, skills_list) in enumerate(skills_dict.items()):
        # Convert category_key to display name
        display_name = category_key.replace('_', ' & ').title()
        priority = priority_order.get(category_key, 0)

        categories.append(SkillCategory(
            category_name=display_name,
            skills=skills_list,
            priority=priority
        ))

    # Sort by priority (descending)
    categories.sort(key=lambda x: x.priority, reverse=True)
    return categories
