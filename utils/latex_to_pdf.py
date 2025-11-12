"""
LaTeX to PDF Converter (2025 - Resume Optimized)
Professional-grade LaTeX compilation with advanced error handling and resume validation
"""

import subprocess
import os
import shutil
import re
from pathlib import Path
from typing import Tuple, Optional, List


class LaTeXToPDFConverter:
    """
    Production-ready LaTeX to PDF converter optimized for resumes

    Features:
    - Multi-compiler support (pdflatex, xelatex, lualatex)
    - Detailed error parsing and reporting
    - Resume-specific validation
    - Automatic package installation detection
    - Clean auxiliary file management
    - PDF metadata optimization
    """

    def __init__(self, compiler: str = 'auto'):
        """
        Initialize converter

        Args:
            compiler: 'auto', 'pdflatex', 'xelatex', or 'lualatex'
        """
        if compiler == 'auto':
            self.compiler = self._find_latex_compiler()
        else:
            if shutil.which(compiler):
                self.compiler = compiler
            else:
                self.compiler = self._find_latex_compiler()

        if self.compiler:
            print(f"📦 Using LaTeX compiler: {self.compiler}")
        else:
            print("⚠️  No LaTeX compiler found")

    def _find_latex_compiler(self) -> Optional[str]:
        """
        Find available LaTeX compiler
        Priority: pdflatex > xelatex > lualatex
        """
        compilers = ['pdflatex', 'xelatex', 'lualatex']

        for compiler in compilers:
            if shutil.which(compiler):
                return compiler

        return None

    def is_latex_installed(self) -> bool:
        """Check if LaTeX is installed"""
        return self.compiler is not None

    def get_compiler_version(self) -> Optional[str]:
        """Get LaTeX compiler version"""
        if not self.compiler:
            return None

        try:
            result = subprocess.run(
                [self.compiler, '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            # Extract first line (version info)
            return result.stdout.split('\n')[0]
        except:
            return None

    def validate_resume_latex(self, tex_file: Path) -> Tuple[bool, List[str]]:
        """
        Validate LaTeX file for common resume issues

        Returns:
            (is_valid, warnings)
        """
        warnings = []

        try:
            with open(tex_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for documentclass
            if not re.search(r'\\documentclass', content):
                warnings.append("Missing \\documentclass declaration")

            # Check for begin/end document
            if not re.search(r'\\begin{document}', content):
                warnings.append("Missing \\begin{document}")
            if not re.search(r'\\end{document}', content):
                warnings.append("Missing \\end{document}")

            # Check for common resume issues
            if '\\includegraphics' in content or '\\includepdf' in content:
                warnings.append("⚠️  Graphics detected - may not be ATS-friendly")

            if '\\usepackage{tikz}' in content or '\\usetikzlibrary' in content:
                warnings.append("⚠️  TikZ graphics detected - may not be ATS-friendly")

            # Check for fancy fonts that might cause issues
            if '\\usepackage{fontspec}' in content and self.compiler == 'pdflatex':
                warnings.append("fontspec requires xelatex or lualatex (not pdflatex)")

            # Check for undefined control sequences (common typos)
            if content.count('\\') - content.count('\\\\') > 100:
                # Many backslashes, check for common typos
                typos = [
                    (r'\\textb{', r'\\textbf{'),
                    (r'\\emph\s', r'\\emph{'),
                ]
                for wrong, right in typos:
                    if re.search(wrong, content):
                        warnings.append(f"Possible typo: {wrong} → use {right}")

            is_valid = len(warnings) == 0
            return is_valid, warnings

        except Exception as e:
            warnings.append(f"Could not validate file: {e}")
            return False, warnings

    def parse_latex_errors(self, log_content: str) -> List[str]:
        """
        Parse LaTeX log file for meaningful errors

        Returns:
            List of error messages
        """
        errors = []

        # Common LaTeX error patterns
        error_patterns = [
            (r'! LaTeX Error: (.+)', 'LaTeX Error'),
            (r'! Undefined control sequence\.\n(.+)', 'Undefined command'),
            (r'! Missing (.+?) inserted', 'Missing character'),
            (r'! Package (\w+) Error: (.+)', 'Package error'),
            (r'! File `(.+?)\' not found', 'Missing file'),
            (r'! Emergency stop', 'Critical error'),
        ]

        for pattern, error_type in error_patterns:
            matches = re.finditer(pattern, log_content, re.MULTILINE)
            for match in matches:
                if match.groups():
                    errors.append(f"{error_type}: {match.group(1)}")
                else:
                    errors.append(error_type)

        # Check for missing packages
        if 'LaTeX Error: File' in log_content and '.sty\' not found' in log_content:
            missing_packages = re.findall(r'File `(.+?)\.sty\' not found', log_content)
            if missing_packages:
                errors.append(f"Missing packages: {', '.join(set(missing_packages))}")
                errors.append("Install with: sudo apt install texlive-latex-extra")

        return errors

    def convert(
        self,
        tex_file: str,
        output_dir: Optional[str] = None,
        cleanup: bool = True,
        validate: bool = True,
        compile_twice: bool = True
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Convert LaTeX file to PDF

        Args:
            tex_file: Path to .tex file
            output_dir: Output directory (optional)
            cleanup: Remove auxiliary files (default: True)
            validate: Run pre-compilation validation (default: True)
            compile_twice: Run twice for references (default: True)

        Returns:
            tuple: (success: bool, pdf_path: str, error: str)
        """
        if not self.compiler:
            return False, None, "❌ No LaTeX compiler installed. Run with --help for installation instructions."

        tex_path = Path(tex_file)

        if not tex_path.exists():
            return False, None, f"❌ File not found: {tex_file}"

        # Validate LaTeX file
        if validate:
            print("🔍 Validating LaTeX file...")
            is_valid, warnings = self.validate_resume_latex(tex_path)
            if warnings:
                print("⚠️  Validation warnings:")
                for warning in warnings:
                    print(f"   - {warning}")
            if not is_valid and len(warnings) > 0:
                print("   (Continuing anyway...)")

        # Set working directory
        work_dir = Path(output_dir) if output_dir else tex_path.parent
        work_dir = work_dir.absolute()
        work_dir.mkdir(parents=True, exist_ok=True)

        print(f"🔄 Converting {tex_path.name} to PDF...")
        print(f"   Compiler: {self.compiler}")
        print(f"   Output: {work_dir}")

        # Compilation runs
        runs = 2 if compile_twice else 1

        try:
            for run in range(runs):
                if runs > 1:
                    print(f"   Run {run + 1}/{runs}...")

                cmd = [
                    self.compiler,
                    '-interaction=nonstopmode',  # Don't stop on errors
                    '-halt-on-error',            # But do halt on critical errors
                    '-file-line-error',          # Better error messages
                    f'-output-directory={work_dir}',
                    str(tex_path.absolute())
                ]

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=120,  # Increased timeout for complex resumes
                    cwd=str(work_dir)
                )

                # On last run, check for errors
                if run == runs - 1 and result.returncode != 0:
                    # Parse log file for errors
                    log_file = work_dir / f"{tex_path.stem}.log"
                    if log_file.exists():
                        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                            log_content = f.read()

                        errors = self.parse_latex_errors(log_content)
                        if errors:
                            error_msg = "LaTeX compilation errors:\n" + "\n".join(f"  • {e}" for e in errors[:5])
                            return False, None, error_msg

                    # Generic error if can't parse
                    return False, None, "❌ PDF compilation failed. Check LaTeX syntax.\nRun with verbose output for details."

            # Check for PDF
            pdf_path = work_dir / f"{tex_path.stem}.pdf"

            if pdf_path.exists():
                pdf_size = pdf_path.stat().st_size
                print(f"   ✓ PDF created ({pdf_size / 1024:.1f} KB)")

                # Cleanup auxiliary files
                if cleanup:
                    cleaned = self._cleanup_aux_files(work_dir, tex_path.stem)
                    if cleaned:
                        print(f"   ✓ Cleaned {cleaned} auxiliary files")

                return True, str(pdf_path), None
            else:
                return False, None, "❌ PDF was not generated (unknown error)"

        except subprocess.TimeoutExpired:
            return False, None, "❌ LaTeX compilation timed out (120s). File may be too complex."
        except FileNotFoundError:
            return False, None, f"❌ Compiler not found: {self.compiler}"
        except Exception as e:
            return False, None, f"❌ Unexpected error: {str(e)}"

    def _cleanup_aux_files(self, directory: Path, basename: str) -> int:
        """
        Remove auxiliary LaTeX files

        Returns:
            Number of files removed
        """
        aux_extensions = [
            '.aux', '.log', '.out', '.toc', '.lof', '.lot',
            '.fls', '.fdb_latexmk', '.synctex.gz', '.bbl', '.blg',
            '.nav', '.snm', '.vrb', '.idx', '.ind', '.ilg',
            '.bcf', '.run.xml', '.dvi', '.ps'
        ]

        cleaned_count = 0
        for ext in aux_extensions:
            aux_file = Path(directory) / f"{basename}{ext}"
            try:
                if aux_file.exists():
                    aux_file.unlink()
                    cleaned_count += 1
            except Exception as e:
                # Silent fail on cleanup errors
                pass

        return cleaned_count

    def optimize_pdf_metadata(self, pdf_path: str, metadata: dict = None):
        """
        Optimize PDF metadata for resumes (requires PyPDF2)

        Args:
            pdf_path: Path to PDF file
            metadata: Dict with keys: title, author, subject, keywords
        """
        try:
            from PyPDF2 import PdfReader, PdfWriter

            reader = PdfReader(pdf_path)
            writer = PdfWriter()

            # Copy pages
            for page in reader.pages:
                writer.add_page(page)

            # Set metadata
            if metadata:
                writer.add_metadata({
                    '/Title': metadata.get('title', 'Resume'),
                    '/Author': metadata.get('author', 'Unknown'),
                    '/Subject': metadata.get('subject', 'Professional Resume'),
                    '/Keywords': metadata.get('keywords', 'resume, CV, data engineer')
                })

            # Write optimized PDF
            with open(pdf_path, 'wb') as f:
                writer.write(f)

            print("   ✓ PDF metadata optimized")

        except ImportError:
            print("   ℹ️  Install PyPDF2 for metadata optimization: pip install PyPDF2")
        except Exception as e:
            print(f"   ⚠️  Could not optimize metadata: {e}")


def install_latex_instructions():
    """Print comprehensive LaTeX installation instructions"""
    print("\n" + "="*70)
    print("📚 LaTeX Installation Instructions (2025)")
    print("="*70)

    print("\n🐧 UBUNTU/DEBIAN (Recommended for Resumes):")
    print("   # Basic installation (sufficient for most resumes)")
    print("   sudo apt update")
    print("   sudo apt install texlive-latex-base texlive-fonts-recommended")
    print()
    print("   # Full installation (all packages)")
    print("   sudo apt install texlive-full")

    print("\n🎩 FEDORA/RHEL/CENTOS:")
    print("   sudo dnf install texlive-scheme-basic")
    print("   # Or full: sudo dnf install texlive-scheme-full")

    print("\n🍎 macOS:")
    print("   # Using Homebrew (lightweight)")
    print("   brew install --cask basictex")
    print()
    print("   # Full installation")
    print("   brew install --cask mactex")

    print("\n🪟 WINDOWS:")
    print("   Download MiKTeX: https://miktex.org/download")
    print("   Or TeX Live: https://www.tug.org/texlive/windows.html")

    print("\n🐳 DOCKER (Cross-platform):")
    print("   docker pull texlive/texlive:latest")
    print("   docker run -v $(pwd):/data texlive/texlive pdflatex resume.tex")

    print("\n✅ VERIFY INSTALLATION:")
    print("   pdflatex --version")
    print("   # Should output: pdfTeX 3.x...")

    print("\n📦 REQUIRED PACKAGES FOR RESUMES:")
    print("   - texlive-latex-base (core LaTeX)")
    print("   - texlive-fonts-recommended (standard fonts)")
    print("   - texlive-latex-extra (additional packages: hyperref, geometry, etc.)")

    print("\n💡 TROUBLESHOOTING:")
    print("   Problem: 'Package X not found'")
    print("   Solution: sudo apt install texlive-latex-extra")
    print()
    print("   Problem: 'Font not found'")
    print("   Solution: sudo apt install texlive-fonts-extra")

    print("="*70 + "\n")


# Standalone usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("╔═══════════════════════════════════════════════════════════════╗")
        print("║      LaTeX to PDF Converter (Resume Optimized - 2025)        ║")
        print("╚═══════════════════════════════════════════════════════════════╝")
        print()
        print("USAGE:")
        print("   python latex_to_pdf.py <file.tex>")
        print("   python latex_to_pdf.py <file.tex> --no-cleanup")
        print("   python latex_to_pdf.py --help")
        print()
        print("OPTIONS:")
        print("   --help          Show installation instructions")
        print("   --no-cleanup    Keep auxiliary files (.aux, .log, etc.)")
        print("   --no-validate   Skip pre-compilation validation")
        print()
        print("EXAMPLES:")
        print("   python latex_to_pdf.py resume.tex")
        print("   python latex_to_pdf.py myresume.tex --no-cleanup")
        print()
        sys.exit(1)

    if sys.argv[1] in ["--help", "-h", "help"]:
        install_latex_instructions()
        sys.exit(0)

    tex_file = sys.argv[1]

    # Parse options
    cleanup = '--no-cleanup' not in sys.argv
    validate = '--no-validate' not in sys.argv

    converter = LaTeXToPDFConverter()

    # Show version info
    version = converter.get_compiler_version()
    if version:
        print(f"📌 {version}\n")

    if not converter.is_latex_installed():
        print("\n❌ LaTeX is not installed!")
        print("   A LaTeX distribution is required to compile resumes.\n")
        install_latex_instructions()
        sys.exit(1)

    # Convert
    success, pdf_path, error = converter.convert(
        tex_file,
        cleanup=cleanup,
        validate=validate
    )

    print()  # Blank line
    if success:
        print("╔═══════════════════════════════════════════════════════════════╗")
        print("║                    ✅ SUCCESS!                                ║")
        print("╚═══════════════════════════════════════════════════════════════╝")
        print(f"\n📄 PDF created: {pdf_path}")
        print(f"📊 Size: {Path(pdf_path).stat().st_size / 1024:.1f} KB")
        print("\n💡 Next steps:")
        print("   1. Open PDF and verify formatting")
        print("   2. Test with ATS checker (Jobscan, Resume Worded)")
        print("   3. Ensure text is selectable (not scanned image)")
        print()
    else:
        print("╔═══════════════════════════════════════════════════════════════╗")
        print("║                    ❌ FAILED                                  ║")
        print("╚═══════════════════════════════════════════════════════════════╝")
        print(f"\n{error}")
        print("\n💡 Debugging tips:")
        print("   1. Check for typos in LaTeX commands")
        print("   2. Ensure all packages are installed")
        print("   3. Run with --no-cleanup to see .log file")
        print("   4. Look for missing .cls or .sty files")
        print()
        sys.exit(1)
