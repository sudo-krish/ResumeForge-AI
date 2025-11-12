"""
Jake's Resume Template
Most popular single-column ATS-friendly template
"""

from typing import List
from data.data_classes import ResumeData, ContactInfo, ProfessionalSummary, SkillCategory, WorkExperience, Project, \
    Education, Certification, Publication
from src.base_template.base import BaseTemplate


class JakeTemplate(BaseTemplate):
    """
    Jake's Resume Template

    Features:
    - Single-column ATS-friendly layout
    - Clean, minimalist design
    - Highly readable
    - Maximum ATS compatibility
    - Popular among tech professionals
    """

    def format_resume(self, resume_data: ResumeData) -> str:
        """
        Format complete resume from ResumeData

        Args:
            resume_data: Complete resume data object

        Returns:
            Complete LaTeX document in Jake's format
        """
        # Format all sections
        header = self.format_header(resume_data.contact)
        summary = self.format_summary(resume_data.summary)
        skills = self.format_skills(resume_data.skills)
        experience = self.format_experience(resume_data.experience)
        projects = self.format_projects(resume_data.projects)
        education = self.format_education(resume_data.education)
        certifications = self.format_certifications(resume_data.certifications, resume_data.publications)

        # Build complete Jake document
        return f"""\\documentclass[letterpaper,11pt]{{article}}

\\usepackage{{latexsym}}
\\usepackage[empty]{{fullpage}}
\\usepackage{{titlesec}}
\\usepackage{{marvosym}}
\\usepackage[usenames,dvipsnames]{{color}}
\\usepackage{{verbatim}}
\\usepackage{{enumitem}}
\\usepackage[hidelinks]{{hyperref}}
\\usepackage{{fancyhdr}}
\\usepackage[english]{{babel}}
\\usepackage{{tabularx}}
\\input{{glyphtounicode}}

\\pagestyle{{fancy}}
\\fancyhf{{}}
\\fancyfoot{{}}
\\renewcommand{{\\headrulewidth}}{{0pt}}
\\renewcommand{{\\footrulewidth}}{{0pt}}

% Adjust margins
\\addtolength{{\\oddsidemargin}}{{-0.5in}}
\\addtolength{{\\evensidemargin}}{{-0.5in}}
\\addtolength{{\\textwidth}}{{1in}}
\\addtolength{{\\topmargin}}{{-.5in}}
\\addtolength{{\\textheight}}{{1.0in}}

\\urlstyle{{same}}
\\raggedbottom
\\raggedright
\\setlength{{\\tabcolsep}}{{0in}}

% Sections formatting
\\titleformat{{\\section}}{{\\vspace{{-4pt}}\\scshape\\raggedright\\large}}{{}}{{0em}}{{}}[\\color{{black}}\\titlerule \\vspace{{-5pt}}]

% Ensure that generate pdf is machine readable/ATS parsable
\\pdfgentounicode=1

%-------------------------
% Custom commands
\\newcommand{{\\resumeItem}}[1]{{\\item\\small{{{{#1 \\vspace{{-2pt}}}}}}}}

\\newcommand{{\\resumeSubheading}}[4]{{
  \\vspace{{-2pt}}\\item
    \\begin{{tabular*}}{{0.97\\textwidth}}[t]{{l@{{\\extracolsep{{\\fill}}}}r}}
      \\textbf{{#1}} & #2 \\\\
      \\textit{{\\small#3}} & \\textit{{\\small #4}} \\\\
    \\end{{tabular*}}\\vspace{{-7pt}}
}}

\\newcommand{{\\resumeProjectHeading}}[2]{{
    \\item
    \\begin{{tabular*}}{{0.97\\textwidth}}{{l@{{\\extracolsep{{\\fill}}}}r}}
      \\small#1 & #2 \\\\
    \\end{{tabular*}}\\vspace{{-7pt}}
}}

\\newcommand{{\\resumeSubItem}}[1]{{\\resumeItem{{#1}}\\vspace{{-4pt}}}}

\\renewcommand\\labelitemii{{$\\vcenter{{\\hbox{{\\tiny$\\bullet$}}}}$}}

\\newcommand{{\\resumeSubHeadingListStart}}{{\\begin{{itemize}}[leftmargin=0.15in, label={{}}]}}
\\newcommand{{\\resumeSubHeadingListEnd}}{{\\end{{itemize}}}}
\\newcommand{{\\resumeItemListStart}}{{\\begin{{itemize}}}}
\\newcommand{{\\resumeItemListEnd}}{{\\end{{itemize}}\\vspace{{-5pt}}}}

%-------------------------------------------
%%%%%%  RESUME STARTS HERE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\begin{{document}}

%----------HEADING----------
{header}

%-----------SUMMARY-----------
\\section{{Summary}}
{summary}

%-----------TECHNICAL SKILLS-----------
\\section{{Technical Skills}}
{skills}

%-----------EXPERIENCE-----------
\\section{{Experience}}
{experience}

%-----------PROJECTS-----------
\\section{{Projects}}
{projects}

%-----------EDUCATION-----------
\\section{{Education}}
{education}

%-----------CERTIFICATIONS-----------
\\section{{Certifications}}
{certifications}

\\end{{document}}"""

    # =========================================================================
    # SECTION FORMATTING METHODS
    # =========================================================================

    def format_header(self, contact: ContactInfo) -> str:
        """Format header in Jake's style"""
        name = self._escape(contact.name)
        phone = self._escape(contact.phone)
        email = self._escape(contact.email)
        location = self._escape(contact.location)

        # Build links
        links = []
        if contact.linkedin:
            display = contact.linkedin.replace('https://', '').replace('www.', '')
            links.append(f"\\href{{{contact.linkedin}}}{{\\underline{{{self._escape(display)}}}}}")

        if contact.github:
            display = contact.github.replace('https://', '').replace('www.', '')
            links.append(f"\\href{{{contact.github}}}{{\\underline{{{self._escape(display)}}}}}")

        if contact.website:
            display = contact.website.replace('https://', '').replace('www.', '')
            links.append(f"\\href{{{contact.website}}}{{\\underline{{{self._escape(display)}}}}}")

        links_line = " | ".join(links) if links else ""

        return f"""\\begin{{center}}
    \\textbf{{\\Huge \\scshape {name}}} \\\\ \\vspace{{1pt}}
    \\small {phone} | {email} | {location} \\\\ \\vspace{{1pt}}
    \\small {links_line}
\\end{{center}}"""

    def format_summary(self, summary: ProfessionalSummary) -> str:
        """Format professional summary"""
        if not summary:
            return ""

        specializations = ', '.join(summary.specializations) if summary.specializations else "various technologies"

        text = (
            f"{self._escape(summary.title)} with {summary.years_of_experience}+ years of experience "
            f"specializing in {self._escape(specializations)}. {self._escape(summary.key_achievement)}"
        )

        return text

    def format_skills(self, skills: List[SkillCategory]) -> str:
        """Format skills in Jake's itemize format"""
        if not skills:
            return " \\begin{itemize}[leftmargin=0.15in, label={}]\n    \\small{\\item{\n     \\textbf{Skills:} Add your skills here\n    }}\n \\end{itemize}"

        # Format each category as "Category: skill1, skill2, ..."
        rows = []
        for cat in skills[:6]:  # Top 6 categories
            category_name = self._escape(cat.category_name)
            skills_str = ', '.join([self._escape(s) for s in cat.skills[:10]])
            rows.append(f"     \\textbf{{{category_name}:}} {skills_str} \\\\")

        return f""" \\begin{{itemize}}[leftmargin=0.15in, label={{}}]
    \\small{{\\item{{
{chr(10).join(rows)}
    }}}}
 \\end{{itemize}}"""

    def format_experience(self, experiences: List[WorkExperience]) -> str:
        """Format experience in Jake's \\resumeSubheading format"""
        if not experiences:
            return """  \\resumeSubHeadingListStart
    \\resumeSubheading
      {{Company Name}}{{Jan 2023 -- Present}}
      {{Position Title}}{{Location}}
      \\resumeItemListStart
        \\resumeItem{{Add your achievements here}}
      \\resumeItemListEnd
  \\resumeSubHeadingListEnd"""

        entries = []

        for exp in experiences[:3]:  # Top 3 roles
            company = self._escape(exp.company)
            position = self._escape(exp.position)
            location = self._escape(exp.location)
            dates = f"{self._escape(exp.start_date)} -- {self._escape(exp.end_date)}"

            # Format achievements as \\resumeItem
            bullets = []
            for ach in exp.achievements[:7]:  # Max 7 bullets
                bullets.append(f"        \\resumeItem{{{self._escape(ach)}}}")

            bullets_text = "\n".join(bullets) if bullets else "        \\resumeItem{Add achievements here}"

            entry = f"""    \\resumeSubheading
      {{{company}}}{{{dates}}}
      {{{position}}}{{{location}}}
      \\resumeItemListStart
{bullets_text}
      \\resumeItemListEnd"""

            entries.append(entry)

        return f"""  \\resumeSubHeadingListStart
{chr(10).join(entries)}
  \\resumeSubHeadingListEnd"""

    def format_projects(self, projects: List[Project]) -> str:
        """Format projects in Jake's \\resumeProjectHeading format"""
        featured = [p for p in projects if p.is_featured][:3]

        if not featured:
            return """    \\resumeSubHeadingListStart
      \\resumeProjectHeading
          {{\\textbf{{Project Name}} $|$ \\emph{{Technologies}}}}{{2024}}
          \\resumeItemListStart
            \\resumeItem{{Project description}}
          \\resumeItemListEnd
    \\resumeSubHeadingListEnd"""

        entries = []

        for proj in featured:
            name = self._escape(proj.name)
            description = self._escape(proj.description)
            tech = ', '.join([self._escape(t) for t in proj.technologies[:5]]) if proj.technologies else "Technologies"

            entry = f"""      \\resumeProjectHeading
          {{\\textbf{{{name}}} $|$ \\emph{{{tech}}}}}{{2024}}
          \\resumeItemListStart
            \\resumeItem{{{description}}}
          \\resumeItemListEnd"""

            entries.append(entry)

        return f"""    \\resumeSubHeadingListStart
{chr(10).join(entries)}
    \\resumeSubHeadingListEnd"""

    def format_education(self, education: List[Education]) -> str:
        """Format education in Jake's format"""
        if not education:
            return """  \\resumeSubHeadingListStart
    \\resumeSubheading
      {{University Name}}{{City, State}}
      {{Degree in Field}}{{2024}}
  \\resumeSubHeadingListEnd"""

        entries = []

        for edu in education:
            institution = self._escape(edu.institution)
            location = self._escape(edu.location)
            degree = self._escape(f"{edu.degree} in {edu.field}")
            year = self._escape(edu.graduation_year)

            entry = f"""    \\resumeSubheading
      {{{institution}}}{{{location}}}
      {{{degree}}}{{{year}}}"""

            entries.append(entry)

        return f"""  \\resumeSubHeadingListStart
{chr(10).join(entries)}
  \\resumeSubHeadingListEnd"""

    def format_certifications(self, certs: List[Certification], pubs: List[Publication]) -> str:
        """Format certifications"""
        items = []

        # Add certifications
        for cert in certs[:5]:  # Top 5
            name = self._escape(cert.name)
            issuer = self._escape(cert.issuer)
            date = self._escape(cert.date_issued)
            items.append(f"    \\resumeItem{{\\textbf{{{name}}} - {issuer} ({date})}}")

        # Add publications if available
        for pub in pubs[:3]:  # Top 3
            title = self._escape(pub.title)
            venue = self._escape(pub.publication_venue)
            date = self._escape(str(pub.date_published))
            items.append(f"    \\resumeItem{{\\textbf{{{title}}} - {venue} ({date})}}")

        if not items:
            items.append("    \\resumeItem{Add certifications here}")

        return f""" \\resumeItemListStart
{chr(10).join(items)}
 \\resumeItemListEnd"""

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
