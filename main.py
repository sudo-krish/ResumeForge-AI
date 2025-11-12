#!/usr/bin/env python3
"""
AI-Powered Resume Generator - Interactive Mode
"""

import argparse
import os
from dataclasses import asdict

from src.resume_templates import TemplateManager, ResumeTemplate
from utils.portfolio_data import get_portfolio_data
from utils.data_transformer import PortfolioToResumeTransformer
from src.ai_integration import AIResumeAssistant
from src.resume_generator import ATSResumeGenerator
from utils.latex_to_pdf import LaTeXToPDFConverter, install_latex_instructions


def print_banner():
    """Print application banner"""
    print("\n" + "=" * 80)
    print("🤖 AI-POWERED RESUME GENERATOR (2025 EDITION)")
    print("=" * 80)


def prompt_job_role() -> str:
    """
    Interactive prompt for job role

    Returns:
        Selected job role
    """
    print("\n📋 SELECT TARGET JOB ROLE")
    print("-" * 80)

    # Predefined roles
    common_roles = [
        "Data Engineer",
        "Software Engineer",
        "Machine Learning Engineer",
        "Full Stack Developer",
        "DevOps Engineer",
        "Data Scientist",
        "Backend Engineer",
        "Frontend Engineer",
        "Cloud Architect",
        "AI/ML Engineer",
        "Custom (Enter your own)"
    ]

    print("\nCommon Roles:")
    for i, role in enumerate(common_roles, 1):
        print(f"  {i}. {role}")

    while True:
        try:
            choice = input(f"\nSelect role [1-{len(common_roles)}]: ").strip()

            if not choice:
                print("❌ Please enter a number")
                continue

            choice_num = int(choice)

            if 1 <= choice_num <= len(common_roles):
                selected_role = common_roles[choice_num - 1]

                if selected_role == "Custom (Enter your own)":
                    custom_role = input("\n✏️  Enter your custom job role: ").strip()
                    if custom_role:
                        return custom_role
                    else:
                        print("❌ Role cannot be empty")
                        continue
                else:
                    return selected_role
            else:
                print(f"❌ Please enter a number between 1 and {len(common_roles)}")

        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            print("\n\n❌ Cancelled by user")
            exit(0)


def prompt_template() -> str:
    """
    Interactive prompt for template selection

    Returns:
        Selected template name
    """
    print("\n🎨 SELECT RESUME TEMPLATE")
    print("-" * 80)

    # Get available templates
    templates = TemplateManager.list_templates()
    template_list = list(templates.items())

    if not template_list:
        print("⚠️  No templates found, using default (jake)")
        return "jake"

    print("\nAvailable Templates:\n")
    for i, (key, info) in enumerate(template_list, 1):
        print(f"  {i}. {info['name'].upper()}")
        print(f"     Description: {info['description']}")
        print(f"     Best for: {info['best_for']}")
        print(f"     Popularity: {info.get('popularity', '⭐⭐⭐⭐')}")
        print()

    while True:
        try:
            choice = input(f"Select template [1-{len(template_list)}] (default: 1): ").strip()

            # Default to first template (usually jake)
            if not choice:
                choice = "1"

            choice_num = int(choice)

            if 1 <= choice_num <= len(template_list):
                selected_template = template_list[choice_num - 1][0]
                return selected_template
            else:
                print(f"❌ Please enter a number between 1 and {len(template_list)}")

        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            print("\n\n❌ Cancelled by user")
            exit(0)


def confirm_selection(role: str, template: str) -> bool:
    """
    Confirm user selections

    Args:
        role: Selected job role
        template: Selected template

    Returns:
        True if confirmed, False otherwise
    """
    print("\n" + "=" * 80)
    print("📝 CONFIRMATION")
    print("=" * 80)
    print(f"\n  Target Role: {role}")
    print(f"  Template: {template.upper()}")

    while True:
        confirm = input("\nProceed with these settings? [Y/n]: ").strip().lower()

        if confirm in ['', 'y', 'yes']:
            return True
        elif confirm in ['n', 'no']:
            return False
        else:
            print("❌ Please enter 'y' or 'n'")


def main():
    """Main execution function with interactive mode"""

    parser = argparse.ArgumentParser(
        description='Generate ATS-friendly resume using AI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (recommended)
  python main.py

  # With arguments
  python main.py --role "Data Engineer" --template jake

  # List available templates
  python main.py --list-templates
        """
    )

    parser.add_argument('--model', type=str, default='qwen2.5-coder:7b-instruct-q4_K_M',
                        help='Ollama model (default: qwen2.5-coder:7b-instruct-q4_K_M)')
    parser.add_argument('--temperature', type=float, default=0.2,
                        help='LLM temperature (default: 0.2)')
    parser.add_argument('--output', '-o', default='output/resume.tex',
                        help='Output LaTeX file (default: output/resume.tex)')
    parser.add_argument('--role', '-r', type=str,
                        help='Target job role (interactive if not provided)')
    parser.add_argument('--template', '-t', type=str,
                        help='Resume template (interactive if not provided)')
    parser.add_argument('--list-templates', action='store_true',
                        help='List available templates and exit')
    parser.add_argument('--yes', '-y', action='store_true',
                        help='Skip confirmation prompt')

    args = parser.parse_args()

    # Print banner
    print_banner()

    # Handle --list-templates
    if args.list_templates:
        print("\n📋 AVAILABLE RESUME TEMPLATES")
        print("=" * 80)

        templates = TemplateManager.list_templates()
        for key, info in templates.items():
            print(f"\n✨ {key.upper()}: {info['name']}")
            print(f"   Description: {info['description']}")
            print(f"   Best for: {info['best_for']}")
            print(f"   Popularity: {info.get('popularity', '⭐⭐⭐⭐')}")

        print("\n" + "=" * 80 + "\n")
        return

    # Get job role (interactive or from args)
    if args.role:
        job_role = args.role
        print(f"\n🎯 Target Role: {job_role} (from arguments)")
    else:
        job_role = prompt_job_role()

    # Get template (interactive or from args)
    if args.template:
        template_name = args.template.lower()
        print(f"\n🎨 Template: {template_name.upper()} (from arguments)")
    else:
        template_name = prompt_template()

    # Confirm selections (unless --yes flag is used)
    if not args.yes:
        if not confirm_selection(job_role, template_name):
            print("\n❌ Generation cancelled. Starting over...\n")
            return main()  # Restart

    # Map template name to enum
    template_map = {
        'jake': ResumeTemplate.JAKE,
        'classic': ResumeTemplate.CLASSIC,
    }
    template = template_map.get(template_name, ResumeTemplate.JAKE)

    print(f"\n✅ Confirmed: {job_role} | {template_name.upper()}")

    # Step 1: Load portfolio data
    print("\n" + "=" * 80)
    print("📂 STEP 1: Loading Portfolio Data")
    print("=" * 80)
    portfolio_data = get_portfolio_data()
    print(f"✓ Loaded data for: {portfolio_data['personal']['name']}")

    # Step 2: Transform data
    print("\n" + "=" * 80)
    print("🔄 STEP 2: Transforming Data")
    print("=" * 80)
    transformer = PortfolioToResumeTransformer()
    resume_data = transformer.transform(portfolio_data)
    print("✓ Data transformed successfully")

    # Step 3: Initialize AI
    print("\n" + "=" * 80)
    print("🤖 STEP 3: Initializing AI Assistant")
    print("=" * 80)
    ai_assistant = AIResumeAssistant(
        model_name=args.model,
        temperature=args.temperature
    )
    print(f"✓ Model: {args.model} (temperature: {args.temperature})")

    # Step 4: Vectorize
    print("\n" + "=" * 80)
    print("🔍 STEP 4: Creating Vector Embeddings")
    print("=" * 80)
    resume_dict = asdict(resume_data)
    ai_assistant.vectorize_portfolio_data(resume_dict)
    print("✓ Vector embeddings created")

    # Step 5: Generate resume
    print("\n" + "=" * 80)
    print("✨ STEP 5: Generating Resume")
    print("=" * 80)
    generator = ATSResumeGenerator(
        ai_assistant,
        auto_optimize=True,
        template=template
    )

    latex_content = generator.generate_resume(
        data=resume_data,
        output=args.output,
        job_role=job_role
    )

    print(f"✓ LaTeX file saved: {args.output}")

    # Step 6: Convert to PDF
    print("\n" + "=" * 80)
    print("📄 STEP 6: Converting to PDF")
    print("=" * 80)

    converter = LaTeXToPDFConverter()

    if not converter.is_latex_installed():
        print("⚠️  LaTeX not installed")
        install_latex_instructions()
        print(f"\n💾 LaTeX file saved: {args.output}")
        print(f"   Convert later: python latex_to_pdf.py {args.output}")
    else:
        success, pdf_path, error = converter.convert(tex_file=args.output)

        if success:
            print(f"✓ PDF created: {pdf_path}")
        else:
            print(f"❌ PDF conversion failed: {error}")
            print(f"   Try manually: pdflatex {args.output}")

    # Summary
    print("\n" + "=" * 80)
    print("🎉 RESUME GENERATION COMPLETE!")
    print("=" * 80)

    output_base = args.output.replace('.tex', '')
    pdf_file = f"{output_base}.pdf"

    print(f"\n📁 Files Generated:")
    print(f"   LaTeX: {args.output}")

    if os.path.exists(pdf_file):
        print(f"   PDF: {pdf_file} ✓")

    print(f"\n🎯 Target Role: {job_role}")
    print(f"🎨 Template: {template_name.upper()}")
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback

        traceback.print_exc()
