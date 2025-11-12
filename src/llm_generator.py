"""
LLM Generator Module
Handles all LLM interactions for content generation using Ollama
"""

from langchain_community.llms import Ollama


class LLMContentGenerator:
    """Generates resume content using Ollama LLM"""

    def __init__(self, model_name="llama3.1", temperature=0.2):
        """
        Initialize LLM Generator

        Args:
            model_name: Ollama model to use
            temperature: Generation temperature (0.0-1.0)
        """
        print(f"🤖 Initializing LLM Generator with {model_name}...")

        self.llm = Ollama(
            model=model_name,
            temperature=temperature
        )

        self.model_name = model_name
        self.temperature = temperature

        print("✅ LLM Generator initialized")

    def generate_professional_summary(self, context):
        """
        Generate professional summary from context

        Args:
            context: Relevant context from vector database

        Returns:
            Professional summary text
        """
        prompt = f"""You are an expert resume writer specializing in ATS-friendly content.

Based on the following professional information, write a compelling professional summary (2-3 sentences maximum).

Professional Context:
{context}

Requirements:
- Highlight years of experience and key technical expertise
- Mention specializations and career focus
- Include 1-2 quantified achievements
- Use strong action words and industry keywords
- Make it ATS-optimized

Write ONLY the summary text, no labels or formatting."""

        response = self.llm.invoke(prompt)
        return response.strip()

    def generate_objective_statement(self, context):
        """
        Generate objective statement from context

        Args:
            context: Relevant context

        Returns:
            Objective statement
        """
        prompt = f"""You are an expert resume writer.

Based on this context, write a concise objective statement (1-2 sentences):

{context}

Focus on:
- Career goals and target role
- Key qualifications
- Value proposition

Write only the objective text."""

        response = self.llm.invoke(prompt)
        return response.strip()

    def enhance_bullet_points(self, bullet_points, context=""):
        """
        Enhance bullet points with better action verbs and quantification

        Args:
            bullet_points: List of bullet points to enhance
            context: Additional context

        Returns:
            List of enhanced bullet points
        """
        enhanced = []

        for bullet in bullet_points[:5]:  # Limit to 5
            prompt = f"""Enhance this resume bullet point to be more impactful and ATS-friendly:

Original: {bullet}

Requirements:
- Start with a strong action verb
- Keep quantified metrics
- Make it concise (1-2 lines max)
- Use industry keywords

Write only the enhanced bullet point."""

            response = self.llm.invoke(prompt)
            enhanced.append(response.strip())

        return enhanced

    def generate_section_content(self, section_name, context, requirements=""):
        """
        Generate content for any resume section

        Args:
            section_name: Name of the section
            context: Relevant context
            requirements: Specific requirements

        Returns:
            Generated content
        """
        prompt = f"""You are an expert resume writer creating ATS-optimized content.

Section: {section_name}
Context: {context}
Requirements: {requirements}

Generate professional, quantified, achievement-focused content. Use action verbs and metrics. Make it concise and ATS-compliant.

Output only the content, no explanations."""

        response = self.llm.invoke(prompt)
        return response.strip()

    def format_skills_description(self, skills_list):
        """
        Format skills list into a narrative description

        Args:
            skills_list: List of skills

        Returns:
            Formatted skills description
        """
        skills_str = ", ".join(skills_list[:15])

        prompt = f"""Create a concise, professional description of these technical skills for a resume:

Skills: {skills_str}

Make it 1-2 sentences, highlighting versatility and expertise. Use ATS keywords.

Output only the description."""

        response = self.llm.invoke(prompt)
        return response.strip()

    def generate_with_custom_prompt(self, custom_prompt):
        """
        Generate content with a completely custom prompt

        Args:
            custom_prompt: Custom prompt string

        Returns:
            Generated content
        """
        response = self.llm.invoke(custom_prompt)
        return response.strip()

    def batch_generate(self, prompts_list):
        """
        Generate multiple responses in batch

        Args:
            prompts_list: List of prompt strings

        Returns:
            List of generated responses
        """
        responses = []
        for prompt in prompts_list:
            response = self.llm.invoke(prompt)
            responses.append(response.strip())
        return responses


class ResumeContentAssistant:
    """
    High-level assistant combining vector search and LLM generation
    """

    def __init__(self, vector_store, llm_generator):
        """
        Initialize assistant with vector store and LLM generator

        Args:
            vector_store: VectorStoreManager instance
            llm_generator: LLMContentGenerator instance
        """
        self.vector_store = vector_store
        self.llm = llm_generator
        print("✅ Resume Content Assistant ready")

    def generate_professional_summary(self):
        """Generate professional summary using vector search + LLM"""
        context = self.vector_store.get_context_string(
            "professional summary career experience achievements", k=5
        )
        return self.llm.generate_professional_summary(context)

    def generate_objective(self):
        """Generate objective statement"""
        context = self.vector_store.get_context_string(
            "career goals objectives aspirations target role", k=3
        )
        return self.llm.generate_objective_statement(context)

    def enhance_experience_bullets(self, company_name):
        """Enhance bullets for specific company"""
        docs = self.vector_store.similarity_search(
            f"experience at {company_name}", k=3
        )

        if not docs:
            return []

        # Extract responsibilities from context
        context = docs[0].page_content
        return self.llm.enhance_bullet_points(context.split('|'))

    def generate_section(self, section_name, requirements=""):
        """Generate any section with context"""
        context = self.vector_store.get_context_string(section_name, k=5)
        return self.llm.generate_section_content(section_name, context, requirements)
