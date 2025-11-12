# 🤖 ResumeForge-AI

> AI-Powered ATS-Friendly Resume Generator for 2025 FAANG Applications

**ResumeForge-AI** is an intelligent resume generation system that transforms your portfolio data into perfectly optimized, ATS-friendly resumes using advanced AI techniques. Built specifically for data engineers and tech professionals targeting FAANG and top-tier companies.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ollama](https://img.shields.io/badge/Ollama-qwen2.5--coder-green.svg)](https://ollama.ai/)

---

## ✨ Features

### 🎯 AI-Powered Optimization
- **Smart Verb Variation**: Automatically tracks and varies power verbs across resume (prevents "architected" 16x!)
- **Keyword Optimization**: Generates role-specific keywords (AI/ML, Cloud, Streaming, etc.)
- **Metrics Coverage**: Ensures 80-90% of bullets have quantified metrics
- **ATS Compliance**: 20-point ATS scoring system with validation

### 📊 Intelligent Analysis
- **Comprehensive Scoring**: 100-point grading system (Content 50 + Format 20 + Keywords 20 + Technical 10)
- **Power Verb Tracking**: Monitors usage across 5 categories (Leadership, Technical, Optimization, Scale, Delivery)
- **Metrics Detection**: 15+ metric patterns (%, +, K/M/B, x, TB/GB, users, etc.)
- **Repetition Analysis**: Identifies and fixes overused words automatically

### 🎨 Multiple Templates
- **Jake Template**: Clean, ATS-optimized, single-column (recommended)
- **Classic Template**: Traditional, professional format
- Easily extensible for custom templates

### 🚀 Smart Features
- **Latest 3 Experiences Only**: Optimizes recent roles, skips older ones
- **Vector Embeddings**: Uses `mxbai-embed-large` for semantic understanding
- **Interactive CLI**: User-friendly prompts for job role and template selection
- **LaTeX → PDF**: Automatic conversion with validation

---

## 📋 Requirements

### System Requirements
- Python 3.8+
- [Ollama](https://ollama.ai/) (local LLM runtime)
- LaTeX distribution (for PDF generation):
  - **Ubuntu/Debian**: `sudo apt-get install texlive-full`
  - **macOS**: `brew install --cask mactex`
  - **Windows**: [MiKTeX](https://miktex.org/download)

### Python Dependencies
```
pip install -r requirements.txt
```

**Key dependencies:**
- `langchain` - LLM orchestration
- `ollama` - Local LLM runtime
- `chromadb` - Vector database
- `pyyaml` - Data loading
- `pdflatex` - PDF conversion

---

## 🚀 Quick Start

### 1. Install Ollama and Pull Model
```
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull recommended model
ollama pull qwen2.5-coder:7b-instruct-q4_K_M

# Pull embedding model
ollama pull mxbai-embed-large
```

### 2. Clone Repository
```
git clone https://github.com/yourusername/ResumeForge-AI.git
cd ResumeForge-AI
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

### 4. Configure Your Data
Edit `data/portfolio_data.yml` with your information:

```
personal:
  name: "Your Name"
  email: "your.email@example.com"
  phone: "+1-234-567-8900"
  location: "San Francisco, CA"
  linkedin: "linkedin.com/in/yourprofile"
  github: "github.com/yourusername"

summary:
  title: "Senior Data Engineer"
  years_of_experience: 5
  specializations:
    - "Real-Time Data Engineering"
    - "Cloud Architecture (AWS)"
  key_achievement: "Reduced pipeline latency by 99%"

experience:
  - company: "Tech Company"
    position: "Senior Data Engineer"
    location: "Remote"
    start_date: "2024-01-01"
    end_date: "Present"
    achievements:
      - "Built real-time pipeline processing 50M+ events daily"
      - "Reduced costs by 30% through optimization"
# ... more experiences

projects:
  - name: "Real-Time Analytics Platform"
    description: "Built streaming pipeline with Kafka and Spark"
    technologies: ["Apache Kafka", "Spark", "AWS"]
    is_featured: true
# ... more projects
```

### 5. Generate Resume

**Interactive Mode (Recommended):**
```
python main.py
```

Follow the prompts:
```
📋 SELECT TARGET JOB ROLE
1. Data Engineer
2. Software Engineer
3. Machine Learning Engineer
...

🎨 SELECT RESUME TEMPLATE
1. JAKE (Clean, ATS-optimized)
2. CLASSIC (Traditional format)
```

**Command-Line Mode:**
```
# Quick generation
python main.py --role "Data Engineer" --template jake

# With custom model
python main.py --role "ML Engineer" --template classic --model llama3:8b

# Skip confirmation
python main.py --role "Data Engineer" --template jake --yes
```

---

## 📖 Usage Examples

### Example 1: Data Engineer Resume
```
python main.py --role "Data Engineer" --template jake --output output/data_engineer.tex
```

**Output:**
```
📊 OVERALL SCORE: 89.5/100 (Grade: A)
📈 Score Breakdown:
   Content Quality:      46.5/50  ✅
   Format & ATS:         20.0/20  ✅
   Keyword Optimization: 20.0/20  ✅
   Technical Depth:      10.0/10  ✅

🎯 Key Metrics:
   Bullets with Metrics: 27/29 (93.1%)
   Total Metrics: 35
   Power Verbs: 14 used
   Metrics Coverage: 17/18 (94.4%)
   Unique Verbs Used: 16
```

### Example 2: ML Engineer Resume
```
python main.py --role "Machine Learning Engineer" --template classic
```

### Example 3: List Available Templates
```
python main.py --list-templates
```

---

## 🏗️ Architecture

```
ResumeForge-AI/
├── main.py                      # CLI entry point
├── data/
│   └── portfolio_data.yml       # Your portfolio data
├── src/
│   ├── ai_integration.py        # AI/LLM integration (Ollama)
│   ├── resume_generator.py      # Main generator class
│   ├── content_optimizer.py     # Intelligent optimizer (verb tracking, metrics)
│   ├── keyword_generator.py     # Role-specific keyword generation
│   ├── resume_templates.py      # Template management (Jake, Classic)
│   └── resume_analyzer.py       # 100-point scoring system
├── utils/
│   ├── portfolio_data.py        # Data loading
│   ├── data_transformer.py      # Portfolio → Resume transformation
│   └── latex_to_pdf.py          # LaTeX → PDF conversion
└── output/
    ├── resume.tex               # Generated LaTeX
    └── resume.pdf               # Final PDF
```

---

## 🎨 Templates

### Jake Template (Recommended)
- **Style**: Clean, modern, single-column
- **ATS Score**: 20/20
- **Best For**: FAANG, startups, tech companies
- **Features**: Clear sections, optimal whitespace, ATS-friendly

### Classic Template
- **Style**: Traditional, professional
- **ATS Score**: 18/20
- **Best For**: Corporate, enterprise roles
- **Features**: Conservative design, detailed sections

### Adding Custom Templates
1. Create template class in `src/resume_templates.py`
2. Inherit from `BaseResumeTemplate`
3. Implement `generate_latex()` method
4. Register in `TemplateManager`

```
class MyTemplate(BaseResumeTemplate):
    def generate_latex(self, data: ResumeData, **kwargs) -> str:
        # Your LaTeX generation logic
        return latex_content
```

---

## 🧠 How It Works

### Phase 1: Keyword Generation
```
1. Analyze target job role
2. Generate tier-1 keywords (AI, ML, LLM, RAG)
3. Generate tier-2 keywords (Real-time, Kafka, Streaming)
4. Create power verb categories
```

### Phase 2: AI Optimization
```
1. Track ALL verbs used (global counter)
2. For each bullet:
   - Extract current verb
   - Check if overused (3+ times)
   - Suggest fresh alternatives
   - Check metrics coverage
   - Add metrics if < 85% coverage
3. Optimize only latest 3 experiences
4. Ensure 80-90% bullets have metrics
```

### Phase 3: Scoring
```
Content Quality (50 pts):
  - Quantification (15 pts): Bullets with metrics
  - Power Verbs (10 pts): Diversity across 5 categories
  - Section Balance (10 pts): Experience vs. other sections
  - Professional Language (10 pts): No pronouns, passive voice
  - No Fluff (5 pts): Avoid buzzwords

Format & ATS (20 pts):
  - No ATS killers (images, graphics, multi-column)
  - All required sections present
  - Clean LaTeX structure

Keywords (20 pts):
  - AI/ML keywords (10 pts)
  - Domain-specific keywords (10 pts)

Technical Depth (10 pts):
  - Specific technologies mentioned
  - Architecture keywords
  - Scale indicators (50M+, 10TB+)
```

---

## 🎯 Optimization Features

### Verb Variation System
**Problem:** Overused verbs (e.g., "Architected" 16 times)

**Solution:**
- Tracks verb usage globally using `Counter()`
- Marks verbs used 3+ times as "overused"
- Provides fresh alternatives from 30+ power verbs
- Categorizes by type (Leadership, Technical, Optimization, Scale, Delivery)

**Example:**
```
Before: Architected, Architected, Architected...
After: Spearheaded, Engineered, Optimized, Delivered, Scaled...
```

### Metrics Coverage
**Target:** 80-90% bullets with quantified metrics

**Tracked Patterns:**
- Percentages: `99%`, `99.9%`
- Scale: `50M+`, `10TB`, `500+ users`
- Improvements: `60% faster`, `3x throughput`
- Reductions: `from 3 hours to 1 minute`

**Example:**
```
Before: Built data pipeline for processing
After: Engineered real-time pipeline processing 50M+ events with 99.9% uptime
```

### Smart Experience Filtering
**Only optimizes latest 3 experiences:**
- Skips older roles (4+ years ago)
- Saves AI tokens
- Focuses on relevant experience
- Prints: "⏭️ Skipped 2 older experiences"

---

## 📊 Sample Output

```
================================================================================
🤖 AI-POWERED RESUME GENERATOR (2025 EDITION)
================================================================================

✅ Template: JAKE
✅ Optimizer: Enabled

🎯 TARGET ROLE: Data Engineer
🏢 TARGET: FAANG

================================================================================
PHASE 1: KEYWORD GENERATION
================================================================================
✅ Keyword Profile Generated:
   Primary Keywords: 10 (AI, ML, LLM, GenAI, RAG...)
   Secondary Keywords: 11
   Top Keywords: AI, ML, LLM, GenAI, RAG

================================================================================
PHASE 2: AI-POWERED OPTIMIZATION
================================================================================
   📝 Professional Summary...
      ✓ +2 keywords, Enhanced

   💼 Work Experience (Latest 3 only)...
      Company 1/3: DTDC Express Limited
      ✓ 5/6 bullets (+9 kw, 4 verbs, 1 metrics)

      Company 2/3: Quantiphi Analytics Solutions
      ✓ 6/6 bullets (+0 kw, 4 verbs, 0 metrics)

      Company 3/3: Cognizant Technology Solutions
      ✓ 6/6 bullets (+1 kw, 6 verbs, 5 metrics)

      ⏭️  Skipped 2 older experiences

   ============================================================================
   ✅ OPTIMIZATION SUMMARY
   ============================================================================
   Bullets Optimized:      17
   Keywords Added:         15
   Verbs Varied:           14
   Metrics Added:          6
   Metrics Coverage:       17/18 (94.4%)
   Unique Verbs Used:      16
   Top Verbs:              reduced(4), built(4), architected(3)
   ============================================================================

================================================================================
PHASE 4: COMPREHENSIVE QUALITY ANALYSIS
================================================================================
📊 OVERALL SCORE: 89.5/100 (Grade: A)

📈 Score Breakdown:
   Content Quality:      46.5/50  ✅
   Format & ATS:         20.0/20  ✅
   Keyword Optimization: 20.0/20  ✅
   Technical Depth:      10.0/10  ✅

💡 EXCELLENT RESUME:
   ✅ Strong verb diversity (16 unique)
   ✅ Comprehensive quantification (94.4%)
   ✅ ATS-optimized format
   ✅ Keyword-rich technical depth
```

---

## 🔧 Configuration

### Model Configuration
Edit `src/ai_integration.py`:

```
DEFAULT_MODEL = "qwen2.5-coder:7b-instruct-q4_K_M"
EMBEDDING_MODEL = "mxbai-embed-large"
TEMPERATURE = 0.2  # Lower = more consistent
```

### Optimization Settings
Edit `src/content_optimizer.py`:

```
METRICS_TARGET = 0.85  # 85% bullets with metrics
MAX_EXPERIENCES = 3    # Only optimize latest 3
VERB_OVERUSE_THRESHOLD = 3  # Flag verbs used 3+ times
```

### Keywords Customization
Edit `src/keyword_generator.py`:

```
CRITICAL_KEYWORDS_2025 = {
    'tier1': {
        'keywords': ['AI', 'ML', 'LLM', 'GenAI', 'RAG'],
        'weight': 3.0,
        'target': (2, 3)  # Appear 2-3 times
    }
}
```

---

## 🐛 Troubleshooting

### Ollama Connection Error
```
# Start Ollama service
ollama serve

# Check if model is available
ollama list
```

### LaTeX Compilation Failed
```
# Install LaTeX
sudo apt-get install texlive-full

# Or use manual conversion
pdflatex output/resume.tex
```

### Low Score (< 70/100)
**Common issues:**
1. **Missing metrics** → Add quantified achievements (%, +, scale)
2. **Overused verbs** → System will auto-fix on next run
3. **Missing keywords** → Add relevant tech stack to `portfolio_data.yml`
4. **Weak bullets** → Add specific numbers, scale, impact

---

## 📝 TODO / Roadmap

- [ ] Add more templates (Modern, Minimalist, Executive)
- [ ] Support multiple output formats (JSON, Markdown, HTML)
- [ ] Add cover letter generation
- [ ] Web UI (Streamlit/Gradio)
- [ ] Resume comparison mode
- [ ] A/B testing different versions
- [ ] Export to LinkedIn format
- [ ] Integration with job boards (LinkedIn, Indeed)
- [ ] Multi-language support
- [ ] Cloud deployment (AWS Lambda, Docker)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

**Areas for contribution:**
- New resume templates
- Additional keyword profiles (SWE, DevOps, etc.)
- Better scoring algorithms
- Additional LLM model support
- Documentation improvements

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Ollama** - Local LLM runtime
- **LangChain** - LLM orchestration framework
- **Jake's Resume Template** - Original LaTeX template inspiration
- **ChromaDB** - Vector database

---

## 📧 Contact

**Krishnanand Anil**
- LinkedIn: [linkedin.com/in/krishnanand-anil](https://linkedin.com/in/krishnanand-anil)
- GitHub: [github.com/sudo-krish](https://github.com/sudo-krish)
- Email: krishnanandpanil@gmail.com
- portfolio: [krishnanandanil.com](https://krishnanandanil.com)

---

## ⭐ Star History

If this project helped you land a job, please give it a star! ⭐

---

**Made with ❤️ by Krishnanand Anil**
