"""
AI Integration - Facade Module
Provides backward-compatible interface to vector_store and llm_generator
"""

from utils.vector_store import VectorStoreManager
from src.llm_generator import LLMContentGenerator, ResumeContentAssistant


class AIResumeAssistant:
    """
    Main AI Assistant - Facade pattern
    Combines vector store and LLM generator for easy use
    """

    def __init__(self, model_name="llama3.1", persist_directory="./resume_db", temperature=0.2):
        """
        Initialize AI Assistant

        Args:
            model_name: Ollama model for LLM
            persist_directory: Vector database directory
            temperature: LLM temperature
        """
        print(f"🎯 Initializing AI Resume Assistant...")

        # Initialize vector store
        self.vector_store = VectorStoreManager(persist_directory=persist_directory)

        # Initialize LLM generator
        self.llm_generator = LLMContentGenerator(
            model_name=model_name,
            temperature=temperature
        )

        # Create high-level assistant
        self.assistant = None

        print("✅ AI Resume Assistant ready")

    def vectorize_portfolio_data(self, portfolio_data):
        """Vectorize portfolio data"""
        num_docs = self.vector_store.vectorize_data(portfolio_data)

        # Initialize assistant after vectorization
        self.assistant = ResumeContentAssistant(
            self.vector_store,
            self.llm_generator
        )

        return num_docs

    def retrieve_context(self, query, k=5):
        """Retrieve context from vector database"""
        return self.vector_store.get_context_string(query, k=k)

    def generate_objective(self, context):
        """Generate objective statement"""
        return self.llm_generator.generate_objective_statement(context)

    def generate_content(self, section_name, context, requirements=""):
        """Generate section content"""
        return self.llm_generator.generate_section_content(
            section_name, context, requirements
        )

    def cleanup(self):
        """Clean up resources"""
        self.vector_store.cleanup()
        print("🧹 AI Assistant cleaned up")
