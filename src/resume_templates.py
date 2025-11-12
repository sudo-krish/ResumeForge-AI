"""
Resume Template System
Dynamically discovers and manages LaTeX templates
"""

from typing import Dict, Type, List
from enum import Enum
import importlib
import inspect
import pkgutil
from pathlib import Path

# Base template import
from src.base_template.base import BaseTemplate


class ResumeTemplate(Enum):
    """
    Available resume templates
    Auto-populated by template discovery
    """
    JAKE = "jake"
    CLASSIC = "classic"
    # Add new templates here or let discovery handle it


class TemplateRegistry:
    """
    Registry for template discovery and management
    Automatically discovers templates from template/ directory
    """

    _registry: Dict[str, Type[BaseTemplate]] = {}
    _metadata: Dict[str, Dict] = {}

    @classmethod
    def register(cls, name: str, template_class: Type[BaseTemplate], metadata: Dict = None):
        """
        Register a template manually

        Args:
            name: Template identifier (e.g., 'jake', 'classic')
            template_class: Template class (must inherit BaseTemplate)
            metadata: Optional template metadata
        """
        if not issubclass(template_class, BaseTemplate):
            raise ValueError(f"{template_class.__name__} must inherit from BaseTemplate")

        cls._registry[name] = template_class
        cls._metadata[name] = metadata or cls._extract_metadata(template_class)

    @classmethod
    def discover_templates(cls, templates_dir: str = "template"):
        """
        Automatically discover and register templates

        Scans the templates directory for Python files containing
        classes that inherit from BaseTemplate

        Args:
            templates_dir: Directory containing template files
        """
        cls._registry.clear()
        cls._metadata.clear()

        try:
            # Get the templates directory path
            template_path = Path(templates_dir)

            if not template_path.exists():
                print(f"⚠️  Template directory not found: {templates_dir}")
                return

            # Scan for Python files
            for file_path in template_path.glob("*.py"):
                if file_path.name.startswith("_"):
                    continue  # Skip __init__.py and private files

                module_name = file_path.stem

                try:
                    # Import the module
                    module = importlib.import_module(f"{templates_dir}.{module_name}")

                    # Find BaseTemplate subclasses
                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        if (issubclass(obj, BaseTemplate) and
                                obj is not BaseTemplate and
                                obj.__module__ == module.__name__):
                            # Extract template name from class name
                            # e.g., JakeTemplate -> jake, ClassicTemplate -> classic
                            template_name = name.replace('Template', '').lower()

                            # Register
                            cls.register(template_name, obj)
                            print(f"   ✓ Discovered template: {template_name} ({name})")

                except Exception as e:
                    print(f"   ⚠️  Error loading {module_name}: {e}")

        except Exception as e:
            print(f"❌ Template discovery failed: {e}")

    @classmethod
    def get_template(cls, template_name: str) -> BaseTemplate:
        """
        Get template instance by name

        Args:
            template_name: Template identifier

        Returns:
            Template instance
        """
        if not cls._registry:
            cls.discover_templates()

        template_class = cls._registry.get(template_name.lower())

        if not template_class:
            print(f"⚠️  Template '{template_name}' not found, using default (jake)")
            template_class = cls._registry.get('jake')

            if not template_class:
                raise ValueError("No templates available! Check template directory.")

        return template_class()

    @classmethod
    def list_templates(cls) -> Dict[str, Dict]:
        """
        List all available templates with metadata

        Returns:
            Dictionary of template metadata
        """
        if not cls._registry:
            cls.discover_templates()

        return cls._metadata.copy()

    @classmethod
    def get_template_names(cls) -> List[str]:
        """Get list of available template names"""
        if not cls._registry:
            cls.discover_templates()

        return list(cls._registry.keys())

    @classmethod
    def _extract_metadata(cls, template_class: Type[BaseTemplate]) -> Dict:
        """
        Extract metadata from template class docstring and attributes

        Args:
            template_class: Template class

        Returns:
            Metadata dictionary
        """
        docstring = template_class.__doc__ or ""

        # Parse docstring for features
        features = []
        if "Features:" in docstring:
            features_section = docstring.split("Features:")[1].split("\n\n")[0]
            features = [line.strip("- ").strip() for line in features_section.split("\n") if
                        line.strip().startswith("-")]

        # Extract description (first line of docstring)
        description = docstring.split("\n")[0].strip() if docstring else template_class.__name__

        # Build metadata
        metadata = {
            'name': template_class.__name__.replace('Template', ' Template'),
            'description': description,
            'features': features,
            'class': template_class.__name__,
            'best_for': cls._infer_best_for(template_class.__name__.lower()),
            'popularity': '⭐⭐⭐⭐'  # Default
        }

        return metadata

    @classmethod
    def _infer_best_for(cls, name: str) -> str:
        """Infer best use case from template name"""
        use_cases = {
            'jake': 'Tech roles, FAANG applications, ATS-friendly',
            'classic': 'All industries, traditional companies',
            'modern': 'Creative roles, startups, design-focused',
            'academic': 'Academia, research positions',
            'executive': 'C-level, senior leadership',
            'minimal': 'Minimalist preference, any industry'
        }

        return use_cases.get(name, 'General purpose')


class TemplateManager:
    """
    Template Manager (Facade)
    Provides simple interface to TemplateRegistry
    """

    @staticmethod
    def get_template(template_name: ResumeTemplate) -> BaseTemplate:
        """
        Get template by enum or string

        Args:
            template_name: ResumeTemplate enum or string

        Returns:
            Template instance
        """
        if isinstance(template_name, ResumeTemplate):
            name = template_name.value
        else:
            name = str(template_name)

        return TemplateRegistry.get_template(name)

    @staticmethod
    def list_templates() -> Dict[str, Dict]:
        """List all available templates"""
        return TemplateRegistry.list_templates()

    @staticmethod
    def print_available_templates():
        """Print formatted list of templates"""
        templates = TemplateRegistry.list_templates()

        if not templates:
            print("No templates available!")
            return

        print("\n" + "=" * 80)
        print("📋 AVAILABLE RESUME TEMPLATES")
        print("=" * 80)

        for name, meta in templates.items():
            print(f"\n✨ {meta['name'].upper()}")
            print(f"   Description: {meta['description']}")
            print(f"   Best For: {meta['best_for']}")
            print(f"   Features:")
            for feature in meta['features'][:5]:
                print(f"      • {feature}")
            print(f"   Popularity: {meta.get('popularity', 'N/A')}")

        print("\n" + "=" * 80 + "\n")


# Auto-discover templates on module import
print("🔍 Discovering resume templates...")
TemplateRegistry.discover_templates()
print(
    f"✅ Found {len(TemplateRegistry.get_template_names())} templates: {', '.join(TemplateRegistry.get_template_names())}\n")
