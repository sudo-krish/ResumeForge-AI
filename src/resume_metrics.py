"""
Comprehensive 2025 Resume Metrics Analyzer - FIXED SCORING
Based on FAANG hiring standards, ATS requirements, and industry best practices
"""

import re
from typing import Dict, List, Set
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class ResumeScore:
    """Resume quality score breakdown"""
    overall: float  # 0-100
    content: float  # 0-50
    format: float  # 0-20
    keywords: float  # 0-20
    technical: float  # 0-10 (was ats_compliance - FIXED)
    grade: str  # A+, A, B+, B, C, F


@dataclass
class ComplianceReport:
    """Detailed compliance analysis"""
    passed: List[str]
    failed: List[str]
    warnings: List[str]
    recommendations: List[str]


class Comprehensive2025ResumeAnalyzer:
    """
    Analyze resume against 2025 FAANG/Data Engineer standards

    FIXED: Correct scoring calculation
    - Content Quality: 50 points
    - Format & ATS: 20 points
    - Keywords: 20 points
    - Technical Depth: 10 points
    = Total: 100 points
    """

    # 2025 Critical Keywords
    CRITICAL_KEYWORDS_2025 = {
        'tier1': {
            'keywords': ['AI', 'ML', 'LLM', 'GenAI', 'RAG', 'Vector Database', 'Langchain'],
            'weight': 3.0,
            'target': (2, 3),
            'category': 'AI/ML'
        },
        'tier2': {
            'keywords': ['Real-time', 'Streaming', 'Event-driven', 'CDC', 'Kafka', 'Kinesis'],
            'weight': 2.5,
            'target': (2, 4),
            'category': 'Real-Time'
        },
        'tier3': {
            'keywords': ['AWS', 'Cloud-native', 'Serverless', 'Docker', 'Kubernetes',
                        'dbt', 'Airflow', 'Spark'],
            'weight': 2.0,
            'target': (2, 3),
            'category': 'Cloud/Modern Stack'
        },
        'tier4': {
            'keywords': ['Python', 'SQL', 'ETL', 'Data Pipeline', 'Data Warehouse',
                        'Data Lake', 'PostgreSQL'],
            'weight': 1.5,
            'target': (1, 3),
            'category': 'Core Skills'
        }
    }

    # Power Verbs
    POWER_VERBS = {
        'Leadership': {
            'verbs': ['Spearheaded', 'Directed', 'Led', 'Drove', 'Championed', 'Orchestrated'],
            'required': 2,
            'weight': 2.0
        },
        'Technical': {
            'verbs': ['Architected', 'Engineered', 'Built', 'Designed', 'Implemented', 'Developed'],
            'required': 4,
            'weight': 2.5
        },
        'Optimization': {
            'verbs': ['Optimized', 'Enhanced', 'Streamlined', 'Improved', 'Accelerated', 'Reduced'],
            'required': 2,
            'weight': 2.0
        },
        'Scale': {
            'verbs': ['Scaled', 'Expanded', 'Migrated', 'Transformed', 'Modernized'],
            'required': 1,
            'weight': 1.5
        },
        'Delivery': {
            'verbs': ['Delivered', 'Shipped', 'Launched', 'Deployed', 'Released'],
            'required': 1,
            'weight': 1.5
        }
    }

    # ATS-killing elements
    ATS_KILLERS = [
        (r'\\includegraphics', 'Images/Graphics'),
        (r'\\begin\{figure\}', 'Figure environments'),
        (r'\\begin\{multicols\}', 'Multi-column layout'),
        (r'\\twocolumn', 'Two-column layout'),
        (r'\\fontspec', 'Custom fonts'),
        (r'\\begin\{wrapfigure\}', 'Text wrapping around images'),
    ]

    def __init__(self):
        """Initialize analyzer"""
        self.keyword_frequency = defaultdict(int)
        self.metrics_count = 0
        self.power_verb_usage = defaultdict(int)
        self.section_lengths = {}
        self.sections_found = set()
        self.ats_issues = []
        self.bullets_analyzed = 0
        self.bullets_with_metrics = 0

    def analyze_comprehensive(self, content: str, latex_content: str = "") -> Dict:
        """Comprehensive resume analysis"""
        print("\n" + "="*80)
        print("🔍 COMPREHENSIVE 2025 RESUME ANALYSIS")
        print("="*80)

        analysis_text = latex_content if latex_content else content

        # Analysis phases
        content_score = self._analyze_content(analysis_text)
        format_score = self._analyze_format(analysis_text)
        keyword_score = self._analyze_keywords(analysis_text)
        technical_score = self._analyze_technical_depth(analysis_text)

        # CORRECT CALCULATION
        overall_score = content_score + format_score + keyword_score + technical_score

        grade = self._calculate_grade(overall_score)
        recommendations = self._generate_recommendations()

        # FIXED: Use 'technical' not 'ats_compliance'
        report = {
            'score': ResumeScore(
                overall=round(overall_score, 1),
                content=round(content_score, 1),
                format=round(format_score, 1),
                keywords=round(keyword_score, 1),
                technical=round(technical_score, 1),  # FIXED
                grade=grade
            ),
            'detailed_analysis': {
                'content': self._get_content_breakdown(),
                'keywords': self._get_keyword_breakdown(),
                'format': self._get_format_breakdown(),
                'technical': self._get_technical_breakdown()
            },
            'recommendations': recommendations,
            'compliance': self._get_compliance_report()
        }

        self._print_comprehensive_report(report)
        return report

    def _analyze_content(self, content: str) -> float:
        """Analyze content quality (50 points)"""
        score = 0.0
        content_lower = content.lower()

        self._identify_sections(content)

        # Track power verbs
        for category, config in self.POWER_VERBS.items():
            for verb in config['verbs']:
                pattern = r'\b' + re.escape(verb.lower()) + r'\b'
                matches = re.findall(pattern, content_lower)
                if matches:
                    self.power_verb_usage[f"{category}:{verb}"] = len(matches)

        # Count bullets
        self.bullets_analyzed = content.count('\\resumeItem{')
        if self.bullets_analyzed == 0:
            self.bullets_analyzed = content.count('\\item ')

        # Metric patterns
        metrics_patterns = [
            r'\d+\\%', r'\d+%', r'\d+\+', r'\d+[KMB]\+?', r'\d+[KMB]',
            r'\d+\.\d+\\%', r'\d+\.\d+%', r'\d+,\d+\+?', r'\d+TB', r'\d+GB',
            r'\d+x', r'\d+ hours?', r'\d+ minutes?', r'\d+ seconds?',
            r'\d+ users?', r'\d+ tables?', r'\d+ events?', r'\d+ reports?',
            r'from \d+\\?%', r'to \d+\\?%',
        ]

        all_metrics = set()
        for pattern in metrics_patterns:
            matches = re.findall(pattern, content)
            all_metrics.update(matches)
        self.metrics_count = len(all_metrics)

        # Count bullets with metrics
        bullets_with_metrics = 0
        if self.bullets_analyzed > 0:
            items = content.split('\\resumeItem{')[1:]
            for item in items:
                brace_count = 1
                bullet_text = ""
                for char in item:
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            break
                    if brace_count > 0:
                        bullet_text += char

                has_metric = any(re.search(pattern, bullet_text) for pattern in metrics_patterns)
                if has_metric:
                    bullets_with_metrics += 1

            self.bullets_with_metrics = bullets_with_metrics
            metrics_ratio = bullets_with_metrics / self.bullets_analyzed

            # Score metrics (15 pts)
            if metrics_ratio >= 0.9:
                score += 15
            elif metrics_ratio >= 0.7:
                score += 12
            elif metrics_ratio >= 0.5:
                score += 8
            else:
                score += max(3, int(metrics_ratio * 15))
        else:
            score += 5

        # Power verb diversity (10 pts)
        score += min(10, self._calculate_power_verb_score())

        # Section balance (10 pts)
        score += min(10, self._calculate_section_balance())

        # Professional language (10 pts)
        score += min(10, self._check_professional_language(content))

        # No fluff (5 pts)
        score += max(0, 5 - self._check_fluff_words(content))

        return min(50, score)

    def _analyze_format(self, latex_content: str) -> float:
        """Analyze format & ATS compliance (20 points)"""
        score = 20.0

        for pattern, name in self.ATS_KILLERS:
            if re.search(pattern, latex_content):
                score -= 2
                self.ats_issues.append(f"ATS Killer: {name}")

        sections_found = 0
        for section_group in [
            ['summary', 'professional summary', 'objective'],
            ['skills', 'technical skills', 'core competencies'],
            ['experience', 'professional experience', 'work experience'],
            ['education'],
            ['projects', 'key projects']
        ]:
            if any(s in self.sections_found for s in section_group):
                sections_found += 1

        if sections_found < 5:
            score -= (5 - sections_found) * 2

        table_count = latex_content.count('\\begin{tabular}')
        if table_count > 1:
            score -= (table_count - 1) * 0.5

        return max(0, score)

    def _analyze_keywords(self, content: str) -> float:
        """Analyze keyword optimization (20 points)"""
        score = 0.0
        content_lower = content.lower()
        keyword_scores = {}

        for tier, config in self.CRITICAL_KEYWORDS_2025.items():
            tier_score = 0
            for keyword in config['keywords']:
                count = content_lower.count(keyword.lower())
                self.keyword_frequency[keyword] = count

                min_target, max_target = config['target']

                if min_target <= count <= max_target:
                    tier_score += config['weight']
                elif count > max_target:
                    tier_score += config['weight'] * 0.5
                elif count == min_target - 1:
                    tier_score += config['weight'] * 0.7

            keyword_scores[config['category']] = tier_score

        if keyword_scores.get('AI/ML', 0) >= 6:
            score += 10
        elif keyword_scores.get('AI/ML', 0) >= 3:
            score += 6
        else:
            score += 2

        total_other = sum(v for k, v in keyword_scores.items() if k != 'AI/ML')
        score += min(10, total_other / 2)

        return score

    def _analyze_technical_depth(self, content: str) -> float:
        """Analyze technical depth (10 points)"""
        score = 0.0

        specific_tech = [
            'Apache Kafka', 'AWS Lambda', 'Redshift', 'Kinesis', 'dbt',
            'PySpark', 'Airflow', 'PostgreSQL', 'Docker', 'Kubernetes',
            'Terraform', 'CloudFormation', 'Pinecone', 'Weaviate'
        ]

        tech_count = sum(1 for tech in specific_tech if tech in content)
        score += min(5, tech_count / 2)

        arch_keywords = ['architecture', 'designed', 'architected', 'scalable',
                        'distributed', 'microservices', 'event-driven']
        arch_count = sum(1 for kw in arch_keywords if kw.lower() in content.lower())
        score += min(2, arch_count / 2)

        if re.search(r'\d+M\+|\d+TB|\d+K\+', content):
            score += 3

        return score

    def _calculate_power_verb_score(self) -> float:
        """Calculate power verb diversity score"""
        score = 0.0
        for category, config in self.POWER_VERBS.items():
            verbs_used = set()
            for key in self.power_verb_usage.keys():
                if key.startswith(f"{category}:"):
                    verb = key.split(':', 1)[1]
                    verbs_used.add(verb)

            count = len(verbs_used)
            if count >= config['required']:
                score += config['weight']
            elif count >= config['required'] * 0.5:
                score += config['weight'] * 0.7
            else:
                if config['required'] > 0:
                    score += (count / config['required']) * config['weight'] * 0.5

        return score

    def _calculate_section_balance(self) -> float:
        """Calculate section balance score"""
        total_words = sum(self.section_lengths.values())
        if total_words == 0:
            return 5

        score = 10.0
        exp_words = self.section_lengths.get('experience', 0)
        exp_ratio = exp_words / total_words

        if 0.40 <= exp_ratio <= 0.50:
            pass
        elif 0.35 <= exp_ratio < 0.40 or 0.50 < exp_ratio <= 0.55:
            score -= 2
        else:
            score -= 4

        return max(0, score)

    def _check_professional_language(self, content: str) -> float:
        """Check for professional language"""
        score = 10.0
        pronouns = len(re.findall(r'\b(I|me|my|we|our)\b', content, re.IGNORECASE))
        score -= min(3, pronouns / 2)

        passive_indicators = ['was built', 'were created', 'is managed']
        passive_count = sum(content.lower().count(p) for p in passive_indicators)
        score -= min(2, passive_count)

        return max(0, score)

    def _check_fluff_words(self, content: str) -> int:
        """Check for fluff/buzzwords"""
        fluff_words = ['synergy', 'leverage', 'paradigm', 'utilize', 'facilitate',
                      'innovative', 'cutting-edge', 'best-in-class', 'world-class']
        penalty = sum(0.5 for word in fluff_words if word in content.lower())
        return int(penalty)

    def _identify_sections(self, content: str):
        """Identify sections in resume"""
        content_lower = content.lower()
        section_patterns = {
            'summary': [r'\\section\{summary\}', r'\\section\{professional summary\}',
                       'summary', 'professional summary'],
            'skills': [r'\\section\{technical skills\}', r'\\section\{skills\}',
                      'technical skills', 'skills'],
            'experience': [r'\\section\{experience\}', r'\\section\{professional experience\}',
                          'experience', 'professional experience'],
            'education': [r'\\section\{education\}', 'education'],
            'projects': [r'\\section\{projects\}', r'\\section\{key projects\}',
                        'projects', 'key projects'],
            'certifications': [r'\\section\{certifications\}', 'certifications']
        }

        for section, patterns in section_patterns.items():
            for pattern in patterns:
                if '\\section' in pattern:
                    if re.search(pattern, content_lower):
                        self.sections_found.add(section)
                        break
                else:
                    if pattern in content_lower:
                        self.sections_found.add(section)
                        break

    def _calculate_grade(self, score: float) -> str:
        """Calculate letter grade"""
        if score >= 95:
            return 'A+'
        elif score >= 90:
            return 'A'
        elif score >= 85:
            return 'A-'
        elif score >= 80:
            return 'B+'
        elif score >= 75:
            return 'B'
        elif score >= 70:
            return 'B-'
        elif score >= 60:
            return 'C'
        else:
            return 'F'

    def _get_content_breakdown(self) -> Dict:
        """Get detailed content quality breakdown"""
        metrics_ratio = (self.bullets_with_metrics / self.bullets_analyzed * 100) if self.bullets_analyzed > 0 else 0
        return {
            'quantification': {
                'bullets_analyzed': self.bullets_analyzed,
                'bullets_with_metrics': self.bullets_with_metrics,
                'metrics_ratio': round(metrics_ratio, 1),
                'total_metrics': self.metrics_count,
                'status': '✅' if metrics_ratio >= 90 else '⚠️'
            },
            'power_verbs': {
                'total_verbs': len(self.power_verb_usage),
                'breakdown': self._get_verb_category_breakdown(),
                'status': '✅' if len(self.power_verb_usage) >= 10 else '⚠️'
            }
        }

    def _get_keyword_breakdown(self) -> Dict:
        """Get detailed keyword analysis breakdown"""
        return {
            'total_unique_keywords': len([k for k, v in self.keyword_frequency.items() if v > 0]),
            'total_mentions': sum(self.keyword_frequency.values())
        }

    def _get_format_breakdown(self) -> Dict:
        """Get detailed format & ATS compliance breakdown"""
        return {
            'ats_compliance': {
                'issues_found': len(self.ats_issues),
                'details': self.ats_issues,
                'status': '✅' if not self.ats_issues else '❌'
            },
            'sections': {
                'required_found': len(self.sections_found),
                'sections_list': list(self.sections_found),
                'status': '✅' if len(self.sections_found) >= 5 else '⚠️'
            }
        }

    def _get_technical_breakdown(self) -> Dict:
        """Get detailed technical depth breakdown"""
        return {'status': '✅'}

    def _get_verb_category_breakdown(self) -> Dict:
        """Get power verb usage by category"""
        breakdown = {}
        for category, config in self.POWER_VERBS.items():
            used_verbs = set()
            for key in self.power_verb_usage.keys():
                if key.startswith(f"{category}:"):
                    verb = key.split(':', 1)[1]
                    used_verbs.add(verb)

            breakdown[category] = {
                'used': len(used_verbs),
                'required': config['required'],
                'verbs': list(used_verbs),
                'status': '✅' if len(used_verbs) >= config['required'] else '⚠️'
            }

        return breakdown

    def _get_missing_sections(self) -> List[str]:
        """Get list of missing critical sections"""
        critical_sections = [
            ['summary', 'professional summary'],
            ['skills', 'technical skills'],
            ['experience', 'professional experience'],
            ['education'],
            ['projects', 'key projects']
        ]

        missing = []
        for section_group in critical_sections:
            if not any(s in self.sections_found for s in section_group):
                missing.append(section_group[0])

        return missing

    def _generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations"""
        recs = []

        if self.bullets_analyzed > 0:
            metrics_ratio = self.bullets_with_metrics / self.bullets_analyzed
            if metrics_ratio < 0.9:
                missing = int((0.9 - metrics_ratio) * self.bullets_analyzed)
                recs.append(f"🎯 Add metrics to {missing} more bullet points")

        for category, config in self.POWER_VERBS.items():
            verbs_used = set()
            for key in self.power_verb_usage.keys():
                if key.startswith(f"{category}:"):
                    verbs_used.add(key.split(':', 1)[1])

            count = len(verbs_used)
            if count < config['required']:
                recs.append(f"💪 Add {config['required'] - count} more {category} power verbs")

        missing = self._get_missing_sections()
        if missing:
            recs.append(f"📋 Add missing sections: {', '.join(missing)}")

        return recs[:10]

    def _get_compliance_report(self) -> ComplianceReport:
        """Generate compliance report"""
        passed = []
        failed = []

        if self.metrics_count >= 15:
            passed.append("✅ Sufficient quantification")
        else:
            failed.append(f"❌ Insufficient metrics ({self.metrics_count}/15)")

        if not self.ats_issues:
            passed.append("✅ ATS-friendly format")

        return ComplianceReport(
            passed=passed,
            failed=failed,
            warnings=[],
            recommendations=self._generate_recommendations()
        )

    def _print_comprehensive_report(self, report: Dict):
        """Print detailed report - FIXED"""
        score = report['score']

        print(f"\n{'='*80}")
        print(f"📊 OVERALL SCORE: {score.overall}/100 (Grade: {score.grade})")
        print(f"{'='*80}")

        print(f"\n📈 Score Breakdown:")
        print(f"   Content Quality:      {score.content}/50  {'✅' if score.content >= 40 else '⚠️'}")
        print(f"   Format & ATS:         {score.format}/20  {'✅' if score.format >= 16 else '⚠️'}")
        print(f"   Keyword Optimization: {score.keywords}/20  {'✅' if score.keywords >= 16 else '⚠️'}")
        print(f"   Technical Depth:      {score.technical}/10  {'✅' if score.technical >= 8 else '⚠️'}")  # FIXED

        print(f"\n🎯 Key Metrics:")
        if self.bullets_analyzed > 0:
            print(f"   Bullets with Metrics: {self.bullets_with_metrics}/{self.bullets_analyzed} ({self.bullets_with_metrics/self.bullets_analyzed*100:.1f}%)")
        print(f"   Total Metrics: {self.metrics_count}")
        print(f"   Power Verbs: {len(self.power_verb_usage)} used")
        print(f"   2025 Hot Keywords: {sum(1 for k, v in self.keyword_frequency.items() if v > 0)}")

        print(f"\n💡 TOP RECOMMENDATIONS:")
        for i, rec in enumerate(report['recommendations'][:5], 1):
            print(f"   {i}. {rec}")

        print(f"\n{'='*80}\n")
