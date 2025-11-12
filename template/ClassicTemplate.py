"""
Classic Professional Template
Clean, minimalist design for all industries
"""

from typing import List
from data.data_classes import ResumeData, ContactInfo, ProfessionalSummary, SkillCategory, WorkExperience, Project, \
    Education, Certification, Publication
from src.base_template.base import BaseTemplate


class ClassicTemplate(BaseTemplate):
    """
    Classic Professional Template

    Features:
    - Clean, minimalist design
    - High readability
    - Traditional but modern
    - Color-coded sections (customizable)
    - Works for all industries
    """

    def format_resume(self, resume_data: ResumeData) -> str:
        """
        Format complete resume from ResumeData

        Args:
            resume_data: Complete resume data object

        Returns:
            Complete LaTeX document
        """
        # Format all sections
        header = self.format_header(resume_data.contact)
        summary = self.format_summary(resume_data.summary)
        skills = self.format_skills(resume_data.skills)
        experience = self.format_experience(resume_data.experience)
        projects = self.format_projects(resume_data.projects)
        education = self.format_education(resume_data.education)
        certifications = self.format_certifications(resume_data.certifications, resume_data.publications)

        # Build complete document
        return f"""\\documentclass[11pt,letterpaper]{{article}}

% Packages
\\usepackage[left=0.5in,top=0.5in,right=0.5in,bottom=0.5in]{{geometry}}
\\usepackage{{enumitem}}
\\usepackage{{hyperref}}
\\usepackage{{titlesec}}
\\usepackage{{xcolor}}

% Define colors
\\definecolor{{primarycolor}}{{RGB}}{{0,102,204}}
\\definecolor{{textcolor}}{{RGB}}{{51,51,51}}

% Formatting
\\titleformat{{\\section}}{{\\large\\bfseries\\color{{primarycolor}}}}{{}}{{0em}}{{}}[{{\\titlerule[0.8pt]}}]
\\titlespacing*{{\\section}}{{0pt}}{{12pt}}{{6pt}}
\\pagestyle{{empty}}
\\hypersetup{{colorlinks=true,linkcolor=primarycolor,urlcolor=primarycolor,pdfborder={{0 0 0}}}}
\\setlist[itemize]{{leftmargin=*, itemsep=3pt, parsep=0pt}}

\\begin{{document}}

%======================================================================
% HEADER
%======================================================================
{header}

%======================================================================
% PROFESSIONAL SUMMARY
%======================================================================
\\section{{Professional Summary}}
\\vspace{{-4pt}}
\\small
{summary}
\\normalsize

%======================================================================
% TECHNICAL SKILLS
%======================================================================
\\section{{Technical Skills}}
\\vspace{{-4pt}}
{skills}

%======================================================================
% PROFESSIONAL EXPERIENCE
%======================================================================
\\section{{Professional Experience}}
\\vspace{{-4pt}}
{experience}

%======================================================================
% PROJECTS
%======================================================================
\\section{{Key Projects}}
\\vspace{{-6pt}}
{projects}

%======================================================================
% EDUCATION
%======================================================================
\\section{{Education}}
\\vspace{{-4pt}}
{education}

%======================================================================
% CERTIFICATIONS
%======================================================================
\\section{{Certifications \\& Achievements}}
\\vspace{{-6pt}}
{certifications}

\\end{{document}}"""

    # =========================================================================
    # SECTION FORMATTING METHODS
    # =========================================================================

    def format_header(self, contact: ContactInfo) -> str:
        """Format header section"""
        name = self._escape(contact.name)
        phone = self._escape(contact.phone)
        email = self._escape(contact.email)
        location = self._escape(contact.location)

        # Build links
        links = []
        if contact.linkedin:
            display = contact.linkedin.replace('https://', '').replace('www.', '')
            links.append(f"\\href{{{contact.linkedin}}}{{{self._escape(display)}}}")

        if contact.github:
            display = contact.github.replace('https://', '').replace('www.', '')
            links.append(f"\\href{{{contact.github}}}{{{self._escape(display)}}}")

        if contact.website:
            display = contact.website.replace('https://', '').replace('www.', '')
            links.append(f"\\href{{{contact.website}}}{{{self._escape(display)}}}")

        links_line = " | ".join(links) if links else ""

        return f"""\\begin{{center}}
    {{\\LARGE\\textbf{{\\color{{primarycolor}}{name}}}}} \\\\
    \\vspace{{5pt}}
    \\small\\color{{textcolor}} {phone} | {email} | {location} \\\\
    \\vspace{{2pt}}
    {links_line}
\\end{{center}}
\\vspace{{-8pt}}"""

    def format_summary(self, summary: ProfessionalSummary) -> str:
        """Format professional summary"""
        if not summary:
            return "Professional with extensive experience in the field."

        specializations = ', '.join(summary.specializations) if summary.specializations else "various technologies"

        text = (
            f"{self._escape(summary.title)} with {summary.years_of_experience}+ years of experience "
            f"specializing in {self._escape(specializations)}. {self._escape(summary.key_achievement)}"
        )

        return text

    def format_skills(self, skills: List[SkillCategory]) -> str:
        """Format skills in table format"""
        if not skills:
            return "\\small\nSkills to be added.\n\\normalsize"

        rows = []
        for cat in skills[:6]:  # Top 6 categories
            category_name = self._escape(cat.category_name)
            skills_str = ', '.join([self._escape(s) for s in cat.skills[:10]])
            rows.append(f"\\textbf{{{category_name}}} & {skills_str} \\\\")

        return f"""\\small
\\begin{{tabular}}{{@{{}}p{{0.24\\textwidth}}p{{0.73\\textwidth}}@{{}}}}
{chr(10).join(rows)}
\\end{{tabular}}
\\normalsize"""

    def format_experience(self, experiences: List[WorkExperience]) -> str:
        """Format work experience"""
        if not experiences:
            return "\\small\nWork experience to be added.\n\\normalsize"

        entries = []

        for exp in experiences[:3]:  # Top 3 roles
            company = self._escape(exp.company)
            position = self._escape(exp.position)
            location = self._escape(exp.location)
            dates = f"{self._escape(exp.start_date)} -- {self._escape(exp.end_date)}"

            # Format achievements as bullet points
            bullets = []
            for ach in exp.achievements[:6]:  # Max 6 bullets
                bullets.append(f"    \\item {self._escape(ach)}")

            bullets_text = "\n".join(bullets) if bullets else "    \\item Key achievements"

            entry = f"""\\vspace{{4pt}}
\\textbf{{{position}}} \\hfill {dates} \\\\
\\textit{{{company}}} \\hfill \\textit{{{location}}}
\\begin{{itemize}}
{bullets_text}
\\end{{itemize}}"""

            entries.append(entry)

        return "\n\n".join(entries)

    def format_projects(self, projects: List[Project]) -> str:
        """Format projects"""
        featured = [p for p in projects if p.is_featured][:3]

        if not featured:
            return "\\begin{itemize}\n    \\item Key projects to be added\n\\end{itemize}"

        items = []
        for proj in featured:
            name = self._escape(proj.name)
            description = self._escape(proj.description)
            tech = ', '.join([self._escape(t) for t in proj.technologies[:5]]) if proj.technologies else "Technologies"

            items.append(f"    \\item \\textbf{{{name}}} ({tech}): {description}")

        return f"""\\begin{{itemize}}
{chr(10).join(items)}
\\end{{itemize}}"""

    def format_education(self, education: List[Education]) -> str:
        """Format education"""
        if not education:
            return "\\small\nEducation to be added.\n\\normalsize"

        entries = []

        for edu in education:
            degree = self._escape(f"{edu.degree} in {edu.field}")
            institution = self._escape(edu.institution)
            location = self._escape(edu.location)
            year = self._escape(edu.graduation_year)

            entry = f"""\\vspace{{4pt}}
\\textbf{{{degree}}} \\hfill {year} \\\\
\\textit{{{institution}}} \\hfill \\textit{{{location}}}"""

            if edu.gpa:
                entry += f" \\\\\nGPA: {self._escape(edu.gpa)}"

            entries.append(entry)

        return "\n\n".join(entries)

    def format_certifications(self, certs: List[Certification], pubs: List[Publication]) -> str:
        """Format certifications and publications"""
        items = []

        # Add certifications
        for cert in certs[:5]:  # Top 5
            name = self._escape(cert.name)
            issuer = self._escape(cert.issuer)
            date = self._escape(cert.date_issued)
            items.append(f"    \\item \\textbf{{{name}}} - {issuer} ({date})")

        # Add publications if available
        for pub in pubs[:3]:  # Top 3
            title = self._escape(pub.title)
            venue = self._escape(pub.publication_venue)
            date = self._escape(str(pub.date_published))
            items.append(f"    \\item \\textbf{{{title}}} - {venue} ({date})")

        if not items:
            items.append("    \\item Certifications to be added")

        return f"""\\begin{{itemize}}
{chr(10).join(items)}
\\end{{itemize}}"""

    # =========================================================================
    # HELPER METHODS
    # =========================================================================

    def _escape(self, text: str) -> str:
        """
        Escape LaTeX special characters

        Args:
            text: Raw text to escape

        Returns:
            LaTeX-safe text
        """
        if not text:
            return ""

        text = str(text)

        # LaTeX special characters
        replacements = [
            ('\\', r'\textbackslash{}'),
            ('&', r'\&'),
            ('%', r'\%'),
            ('$', r'\$'),
            ('#', r'\#'),
            ('_', r'\_'),
            ('{', r'\{'),
            ('}', r'\}'),
            ('~', r'\textasciitilde{}'),
            ('^', r'\textasciicircum{}'),
        ]

        for old, new in replacements:
            text = text.replace(old, new)

        return text.strip()
