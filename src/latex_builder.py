"""
Professional LaTeX Resume Builder
Delegates all formatting to templates - builder only orchestrates and validates
"""

from typing import Optional
from pathlib import Path

from data.data_classes import ResumeData
from src.resume_templates import ResumeTemplate, TemplateManager


class ProfessionalLaTeXBuilder:
    """
    Template-agnostic LaTeX builder

    Responsibilities:
    - Template selection and initialization
    - Orchestration (calls template methods)
    - LaTeX validation
    - NO formatting (templates do that)
    """

    def __init__(self, template: ResumeTemplate = ResumeTemplate.JAKE):
        """
        Initialize builder with template choice

        Args:
            template: Template to use (default: Jake's Resume)
        """
        self.template = TemplateManager.get_template(template)
        self.template_name = template

    def build_resume_from_data(self, resume_data: ResumeData) -> str:
        """
        Build complete LaTeX document from ResumeData
        Template handles ALL formatting

        Args:
            resume_data: Complete resume data object

        Returns:
            Complete LaTeX document string
        """
        print(f"\n📄 Building with {self.template_name.value.upper()} template...")

        # Template does all the work
        latex_content = self.template.format_resume(resume_data)

        # Validate structure
        if self._validate_structure(latex_content):
            print("   ✓ LaTeX document built successfully")
        else:
            print("   ⚠️  LaTeX validation warnings detected")

        return latex_content

    def _validate_structure(self, latex_content: str) -> bool:
        """
        Validate LaTeX document structure

        Checks:
        - Required LaTeX elements present
        - Balanced environments
        - Document integrity
        """
        if not latex_content or len(latex_content) < 100:
            print("   ⚠️  Document too short or empty")
            return False

        # Check required elements
        required_elements = [
            '\\documentclass',
            '\\begin{document}',
            '\\end{document}',
        ]

        for element in required_elements:
            if element not in latex_content:
                print(f"   ⚠️  Missing: {element}")
                return False

        # Check balanced environments
        environments = ['itemize', 'enumerate', 'tabular', 'center']
        for env in environments:
            begin_count = latex_content.count(f'\\begin{{{env}}}')
            end_count = latex_content.count(f'\\end{{{env}}}')

            if begin_count != end_count:
                print(f"   ⚠️  Unbalanced {env}: {begin_count} begin vs {end_count} end")
                return False

        return True

    def validate_latex(self, latex_content: str) -> bool:
        """
        Public validation method

        Args:
            latex_content: LaTeX document to validate

        Returns:
            True if valid, False otherwise
        """
        return self._validate_structure(latex_content)

    def save_to_file(self, latex_content: str, output_path: str) -> bool:
        """
        Save LaTeX content to file

        Args:
            latex_content: LaTeX document
            output_path: Output file path

        Returns:
            True if successful, False otherwise
        """
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(latex_content)

            print(f"   ✓ Saved: {output_path}")
            return True

        except Exception as e:
            print(f"   ❌ Error saving file: {e}")
            return False
