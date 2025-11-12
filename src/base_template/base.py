"""
Base Template Abstract Class
All resume templates must inherit from this
"""

from abc import ABC, abstractmethod
from typing import List


class BaseTemplate(ABC):
    """
    Abstract base class for resume templates

    All templates must implement these methods to ensure
    consistent interface across different template styles
    """

    @abstractmethod
    def format_resume(self, resume_data) -> str:
        """
        Format complete resume from ResumeData

        Args:
            resume_data: Complete ResumeData object

        Returns:
            Complete LaTeX document string
        """
        pass

    @abstractmethod
    def format_header(self, contact) -> str:
        """Format header section"""
        pass

    @abstractmethod
    def format_summary(self, summary) -> str:
        """Format professional summary"""
        pass

    @abstractmethod
    def format_skills(self, skills: List) -> str:
        """Format skills section"""
        pass

    @abstractmethod
    def format_experience(self, experiences: List) -> str:
        """Format work experience"""
        pass

    @abstractmethod
    def format_projects(self, projects: List) -> str:
        """Format projects section"""
        pass

    @abstractmethod
    def format_education(self, education: List) -> str:
        """Format education section"""
        pass

    @abstractmethod
    def format_certifications(self, certs: List, pubs: List) -> str:
        """Format certifications and publications"""
        pass
