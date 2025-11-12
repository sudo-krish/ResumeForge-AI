"""
Portfolio data loader - reads from YAML file
"""

import yaml
from pathlib import Path


def load_portfolio_data(yaml_file='data/portfolio_data.yml'):
    """
    Load portfolio data from YAML file

    Args:
        yaml_file: Path to YAML file (default: portfolio_data.yml)

    Returns:
        Dictionary containing portfolio data
    """
    yaml_path = Path(yaml_file)

    if not yaml_path.exists():
        raise FileNotFoundError(f"Portfolio data file not found: {yaml_file}")

    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    return data


# Cache the loaded data
_PORTFOLIO_DATA = None


def get_portfolio_data():
    """Return the complete portfolio data (cached)"""
    global _PORTFOLIO_DATA

    if _PORTFOLIO_DATA is None:
        _PORTFOLIO_DATA = load_portfolio_data()

    return _PORTFOLIO_DATA


def reload_portfolio_data():
    """Force reload portfolio data from YAML file"""
    global _PORTFOLIO_DATA
    _PORTFOLIO_DATA = load_portfolio_data()
    return _PORTFOLIO_DATA


def get_personal_info():
    """Get personal information section"""
    return get_portfolio_data().get('personal', {})


def get_experience():
    """Get work experience section"""
    return get_portfolio_data().get('companies', [])


def get_education():
    """Get education section"""
    return get_portfolio_data().get('education', [])


def get_projects():
    """Get projects section"""
    return get_portfolio_data().get('projects', [])


def get_featured_projects():
    """Get featured projects only"""
    return [p for p in get_portfolio_data().get('projects', []) if p.get('featured', False)]


def get_certifications():
    """Get certifications section"""
    return get_portfolio_data().get('certifications', [])


def get_research_papers():
    """Get research papers section"""
    return get_portfolio_data().get('researchPapers', [])
