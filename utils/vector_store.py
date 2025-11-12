"""
Vector Store Module
Handles document vectorization and semantic search using ChromaDB
"""

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import json


class VectorStoreManager:
    """Manages vector database operations for resume data"""

    def __init__(self, persist_directory="./resume_db", embedding_model="mxbai-embed-large"):
        """
        Initialize Vector Store Manager

        Args:
            persist_directory: Path to store vector database
            embedding_model: Ollama embedding model to use
        """
        print(f"🗄️  Initializing Vector Store with {embedding_model}...")

        # Initialize embeddings
        self.embeddings = OllamaEmbeddings(model=embedding_model)

        # Vector database setup
        self.persist_directory = persist_directory
        self.vectorstore = None

        # Text splitter for chunking documents
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        )

        print("✅ Vector Store Manager initialized")

    def create_documents_from_portfolio(self, portfolio_data):
        """
        Convert portfolio data into Document objects

        Args:
            portfolio_data: Dictionary containing portfolio information

        Returns:
            List of Document objects
        """
        documents = []

        # Process personal information
        if 'personal' in portfolio_data:
            personal = portfolio_data['personal']
            personal_docs = [
                f"Name: {personal.get('name', '')}",
                f"Job Title: {personal.get('jobTitle', '')}",
                f"Professional Bio: {personal.get('bio', '')}",
                f"Contact: {personal.get('email', '')} | {personal.get('phone', '')}",
                f"Location: {personal.get('address', {}).get('city', '')}, {personal.get('address', {}).get('state', '')}",
                f"Professional Links: LinkedIn: {personal.get('socialLinks', {}).get('linkedin', '')}, GitHub: {personal.get('socialLinks', {}).get('github', '')}",
                f"Years of Experience: {personal.get('yearsOfExperience', 0)} years",
                f"Core Competencies: {', '.join(personal.get('topSkills', []))}",
                f"Technical Skills: {', '.join(personal.get('skills', []))}",
                f"Career Achievements: {' | '.join(personal.get('achievements', []))}"
            ]

            for doc_text in personal_docs:
                documents.append(Document(
                    page_content=doc_text,
                    metadata={"section": "personal", "type": "info"}
                ))

        # Process education
        if 'education' in portfolio_data:
            for edu in portfolio_data['education']:
                edu_text = (
                    f"Education: {edu.get('degree', '')} in {edu.get('field', '')} "
                    f"from {edu.get('university', '')} (Graduated: {edu.get('graduationYear', '')}). "
                    f"GPA: {edu.get('gpa', 'N/A')}. Location: {edu.get('location', '')}"
                )
                documents.append(Document(
                    page_content=edu_text,
                    metadata={"section": "education", "university": edu.get('university', '')}
                ))

        # Process work experience
        if 'companies' in portfolio_data:
            for company in portfolio_data['companies']:
                company_text = (
                    f"Work Experience at {company.get('name', '')}: "
                    f"Position: {company.get('position', '')}. "
                    f"Duration: {company.get('duration', '')}. "
                    f"Description: {company.get('description', '')}. "
                    f"Key Achievements: {' | '.join(company.get('responsibilities', []))}. "
                    f"Technologies: {', '.join(company.get('technologies', []))}"
                )
                documents.append(Document(
                    page_content=company_text,
                    metadata={
                        "section": "experience",
                        "company": company.get('name', ''),
                        "current": company.get('current', False)
                    }
                ))

        # Process projects
        if 'projects' in portfolio_data:
            for project in portfolio_data['projects']:
                metrics_text = ""
                if 'metrics' in project:
                    metrics_text = f" Metrics: {json.dumps(project['metrics'])}"

                project_text = (
                    f"Project: {project.get('name', '')}. "
                    f"Description: {project.get('longDescription', project.get('description', ''))}. "
                    f"Technologies: {', '.join(project.get('technologies', []))}. "
                    f"Languages: {', '.join(project.get('languages', []))}.{metrics_text}"
                )
                documents.append(Document(
                    page_content=project_text,
                    metadata={
                        "section": "projects",
                        "featured": project.get('featured', False)
                    }
                ))

        # Process certifications
        if 'certifications' in portfolio_data:
            for cert in portfolio_data['certifications']:
                cert_text = (
                    f"Certification: {cert.get('name', '')} "
                    f"from {cert.get('issuer', '')} ({cert.get('dateIssued', '')}). "
                    f"Category: {cert.get('category', '')}"
                )
                documents.append(Document(
                    page_content=cert_text,
                    metadata={"section": "certifications"}
                ))

        # Process research papers
        if 'researchPapers' in portfolio_data:
            for paper in portfolio_data['researchPapers']:
                year = paper.get('datePublished', '')[:4] if paper.get('datePublished') else ''
                paper_text = (
                    f"Research Publication: {paper.get('title', '')} "
                    f"in {paper.get('journal', '')} ({year}). "
                    f"Abstract: {paper.get('abstract', '')}"
                )
                documents.append(Document(
                    page_content=paper_text,
                    metadata={"section": "research"}
                ))

        return documents

    def vectorize_data(self, portfolio_data):
        """
        Create and populate vector database from portfolio data

        Args:
            portfolio_data: Dictionary containing portfolio information

        Returns:
            Number of documents vectorized
        """
        print("📊 Creating documents from portfolio data...")

        # Create documents
        documents = self.create_documents_from_portfolio(portfolio_data)

        print(f"📄 Created {len(documents)} documents")
        print("🔍 Splitting and vectorizing documents...")

        # Split documents for better retrieval
        split_docs = self.text_splitter.split_documents(documents)

        # Create vector store
        self.vectorstore = Chroma.from_documents(
            documents=split_docs,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )

        print(f"✅ Vectorized {len(documents)} sections into {len(split_docs)} chunks")
        return len(documents)

    def similarity_search(self, query, k=5, filter_metadata=None):
        """
        Perform semantic search on vector database

        Args:
            query: Search query string
            k: Number of results to return
            filter_metadata: Optional metadata filter

        Returns:
            List of relevant Document objects
        """
        if not self.vectorstore:
            raise ValueError("Vector database not initialized. Call vectorize_data() first.")

        if filter_metadata:
            results = self.vectorstore.similarity_search(
                query,
                k=k,
                filter=filter_metadata
            )
        else:
            results = self.vectorstore.similarity_search(query, k=k)

        return results

    def get_context_string(self, query, k=5):
        """
        Get concatenated context string from similarity search

        Args:
            query: Search query
            k: Number of results

        Returns:
            Concatenated context string
        """
        results = self.similarity_search(query, k=k)
        context = "\n\n".join([doc.page_content for doc in results])
        return context

    def search_by_section(self, section_name, k=5):
        """
        Search for documents from a specific section

        Args:
            section_name: Section to search (e.g., 'experience', 'projects')
            k: Number of results

        Returns:
            List of Document objects from that section
        """
        return self.similarity_search(
            query=section_name,
            k=k,
            filter_metadata={"section": section_name}
        )

    def cleanup(self):
        """Clean up vector store resources"""
        if self.vectorstore:
            self.vectorstore = None
        print("🧹 Vector Store cleaned up")
