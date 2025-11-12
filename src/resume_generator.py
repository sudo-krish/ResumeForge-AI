"""
AI-Powered Resume Generator (Template-Agnostic)
Delegates formatting to templates - generator only orchestrates
"""

from typing import Dict, Tuple
from datetime import datetime
from pathlib import Path

from data.data_classes import ResumeData
from src.ai_integration import AIResumeAssistant
from src.keyword_generator import AIKeywordGenerator, KeywordProfile
from src.resume_optimizer import IntelligentResumeOptimizer, BatchOptimizer
from src.latex_builder import ProfessionalLaTeXBuilder
from src.resume_metrics import Comprehensive2025ResumeAnalyzer
from src.resume_templates import ResumeTemplate


class AIResumeGenerator:
    """
    Template-Agnostic Resume Generator

    Generator orchestrates workflow, templates handle formatting
    """

    def __init__(
        self,
        ai_assistant: AIResumeAssistant,
        auto_optimize: bool = True,
        template: ResumeTemplate = ResumeTemplate.JAKE,
    ):
        """Initialize generator"""
        self.ai = ai_assistant
        self.auto_optimize = auto_optimize
        self.template = template

        # Initialize components
        self.keyword_gen = AIKeywordGenerator(ai_assistant)
        self.optimizer = IntelligentResumeOptimizer(ai_assistant)
        self.batch_optimizer = BatchOptimizer(self.optimizer)
        self.latex_builder = ProfessionalLaTeXBuilder(template=template)
        self.metrics = Comprehensive2025ResumeAnalyzer()

        self._print_init_banner(template)

    def generate(
        self,
        resume_data: ResumeData,
        job_role: str,
        output_file: str = "output/resume.tex",
        job_description: str = "",
        target_company: str = "FAANG"
    ) -> Tuple[str, Dict]:
        """Generate optimized resume"""
        self._print_generation_header(job_role, target_company)

        # Phase 1: Keywords
        keyword_profile = self._phase1_keywords(job_role, job_description, resume_data, target_company)

        # Phase 2: AI Optimization (on raw data class content)
        optimized_data = self._phase2_optimization(resume_data, keyword_profile)

        # Phase 3: LaTeX Building (template does formatting)
        latex_content = self._phase3_latex(optimized_data)

        # Phase 4: Quality Analysis
        quality_report = self._phase4_analysis(optimized_data, latex_content)

        # Save and report
        self._save_file(output_file, latex_content)
        self._print_final_summary(output_file, quality_report)

        return latex_content, quality_report

    def _phase1_keywords(self, job_role, job_description, resume_data, target_company) -> KeywordProfile:
        """Generate keywords"""
        print("\n" + "="*80)
        print("PHASE 1: KEYWORD GENERATION")
        print("="*80)

        user_experience = {
            'skills': [],
            'technologies': [],
            'achievements': []
        }

        for skill_cat in resume_data.skills:
            user_experience['skills'].extend(skill_cat.skills)

        for exp in resume_data.experience:
            user_experience['technologies'].extend(exp.technologies)
            user_experience['achievements'].extend(exp.achievements)

        keyword_profile = self.keyword_gen.generate_keywords(
            job_role=job_role,
            job_description=job_description,
            user_experience=user_experience,
            target_company=target_company
        )

        print(f"   ✓ Generated {len(keyword_profile.primary_keywords)} primary keywords")
        return keyword_profile

    def _phase2_optimization(self, resume_data: ResumeData, keyword_profile: KeywordProfile) -> ResumeData:
        """AI Optimization - Single method call"""
        if not self.auto_optimize:
            print("\n⏭️  PHASE 2: Skipped")
            return resume_data

        print("\n" + "=" * 80)
        print("PHASE 2: AI-POWERED OPTIMIZATION")
        print("=" * 80)

        try:
            optimized_data, stats = self.optimizer.optimize_resume_data(
                resume_data=resume_data,
                keyword_profile=keyword_profile
            )
            return optimized_data
        except Exception as e:
            print(f"\n   ❌ ERROR: {str(e)}")
            return resume_data

    def _phase3_latex(self, resume_data: ResumeData) -> str:
        """Build LaTeX - delegates formatting to template"""
        print("\n" + "="*80)
        print("PHASE 3: LATEX DOCUMENT GENERATION")
        print("="*80)

        # LaTeX builder calls template's format methods
        latex_content = self.latex_builder.build_resume_from_data(resume_data)

        if self.latex_builder.validate_latex(latex_content):
            print("   ✓ LaTeX validation passed")
        else:
            print("   ⚠️  LaTeX validation issues detected")

        return latex_content

    def _phase4_analysis(self, resume_data: ResumeData, latex_content: str) -> Dict:
        """
        Quality analysis on RAW LaTeX content
        FIXED: Pass latex_content directly to analyzer (it handles parsing internally)
        """
        print("\n" + "=" * 80)
        print("PHASE 4: COMPREHENSIVE QUALITY ANALYSIS")
        print("=" * 80)

        # FIXED: Pass raw LaTeX directly - analyzer handles parsing
        report = self.metrics.analyze_comprehensive(
            content=latex_content,  # Pass raw LaTeX as content
            latex_content=latex_content  # Also pass as latex_content (for ATS check)
        )

        return report

    def _extract_text_from_latex(self, latex_content: str) -> str:
        """
        Extract plain text from LaTeX for analysis
        Removes LaTeX commands but preserves content
        """
        import re

        # Remove everything before \begin{document}
        if '\\begin{document}' in latex_content:
            latex_content = latex_content.split('\\begin{document}')[1]

        # Remove everything after \end{document}
        if '\\end{document}' in latex_content:
            latex_content = latex_content.split('\\end{document}')[0]

        # Remove comments
        latex_content = re.sub(r'%.*?\n', '\n', latex_content)

        # Remove LaTeX commands but keep their content
        # \textbf{content} -> content
        latex_content = re.sub(r'\\textbf\{([^}]+)\}', r'\1', latex_content)
        latex_content = re.sub(r'\\textit\{([^}]+)\}', r'\1', latex_content)
        latex_content = re.sub(r'\\emph\{([^}]+)\}', r'\1', latex_content)
        latex_content = re.sub(r'\\underline\{([^}]+)\}', r'\1', latex_content)
        latex_content = re.sub(r'\\scshape\s+', '', latex_content)
        latex_content = re.sub(r'\\small\s+', '', latex_content)
        latex_content = re.sub(r'\\large\s+', '', latex_content)
        latex_content = re.sub(r'\\Huge\s+', '', latex_content)

        # \href{url}{text} -> text
        latex_content = re.sub(r'\\href\{[^}]+\}\{([^}]+)\}', r'\1', latex_content)

        # \section{Title} -> Title (keep section headers)
        latex_content = re.sub(r'\\section\{([^}]+)\}', r'\n\n\1\n', latex_content)

        # Remove environment commands
        latex_content = re.sub(r'\\(begin|end)\{[^}]+\}', '', latex_content)

        # Remove \item commands
        latex_content = re.sub(r'\\item\s*', '', latex_content)

        # Remove \resumeItem, \resumeSubheading, etc.
        latex_content = re.sub(r'\\resume[A-Za-z]+', '', latex_content)

        # Remove remaining backslash commands
        latex_content = re.sub(r'\\[a-zA-Z]+(\[[^\]]*\])?(\{[^}]*\})?', '', latex_content)

        # Remove special characters used in LaTeX
        latex_content = latex_content.replace('\\\\', '\n')
        latex_content = latex_content.replace('&', '')
        latex_content = latex_content.replace('$', '')
        latex_content = latex_content.replace('~', ' ')
        latex_content = latex_content.replace('|', '')

        # Clean up whitespace
        latex_content = re.sub(r'\n\s*\n\s*\n', '\n\n', latex_content)
        latex_content = re.sub(r' +', ' ', latex_content)
        latex_content = re.sub(r'\n ', '\n', latex_content)

        return latex_content.strip()

    def _extract_text_from_data(self, data: ResumeData) -> str:
        """
        Extract all text from data classes for analysis
        DEPRECATED: Use _extract_text_from_latex instead
        Kept for backward compatibility
        """
        text_parts = []

        # Contact
        text_parts.append(f"{data.contact.name} {data.contact.email}")

        # Summary
        if data.summary:
            text_parts.append(
                f"{data.summary.title} {' '.join(data.summary.specializations)} {data.summary.key_achievement}")

        # Skills
        for cat in data.skills:
            text_parts.append(' '.join(cat.skills))

        # Experience
        for exp in data.experience:
            text_parts.append(f"{exp.company} {exp.position}")
            text_parts.extend(exp.achievements)

        # Projects
        for proj in data.projects:
            text_parts.append(f"{proj.name} {proj.description}")

        return "\n\n".join(text_parts)

    def _save_file(self, output_file: str, latex_content: str):
        """Save file"""
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        print(f"\n💾 Saved: {output_file}")

    def _print_init_banner(self, template):
        """Print banner"""
        print("="*80)
        print("🤖 AI-POWERED RESUME GENERATOR (2025 EDITION)")
        print("="*80)
        print(f"✅ Template: {template.value.upper()}")
        print(f"✅ Optimizer: {'Enabled' if self.auto_optimize else 'Disabled'}")
        print("="*80)

    def _print_generation_header(self, job_role, target):
        """Print header"""
        print(f"\n🎯 TARGET ROLE: {job_role}")
        print(f"🏢 TARGET: {target}")
        print(f"📅 DATE: {datetime.now().strftime('%B %d, %Y')}")

    def _print_final_summary(self, output_file, report):
        """Print summary"""
        print("\n" + "="*80)
        print("✅ RESUME GENERATION COMPLETE")
        print("="*80)
        score = report['score']
        print(f"\n📄 File: {output_file}")
        print(f"🎯 SCORE: {score.overall}/100 (Grade: {score.grade})")
        print("="*80 + "\n")


# Backward compatibility
class ATSResumeGenerator(AIResumeGenerator):
    """Alias for legacy code"""

    def generate_resume(
            self,
            data: ResumeData,
            output: str = "output/resume.tex",
            job_role: str = "Data Engineer"
    ) -> str:
        """Legacy method"""
        content, _ = self.generate(data, job_role, output)
        return content