"""
AI-Powered Resume Optimizer - ENHANCED VERSION
Tracks used verbs globally, targets 80-90% metrics coverage, optimizes only latest 3 experiences
"""

from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
from collections import Counter
import re

from data.data_classes import ResumeData
from src.ai_integration import AIResumeAssistant
from src.keyword_generator import KeywordProfile


@dataclass
class OptimizationResult:
    """Result of content optimization"""
    original: str
    optimized: str
    keywords_added: List[str]
    improvements: List[str]
    repetitions_fixed: Dict[str, int]
    factuality_score: float
    has_metrics: bool  # NEW: Track if bullet has metrics


@dataclass
class RepetitionAnalysis:
    """Analysis of word repetitions"""
    repeated_words: Dict[str, int]
    suggested_synonyms: Dict[str, List[str]]
    severity: str


class IntelligentResumeOptimizer:
    """
    Enhanced resume optimizer that:
    1. Tracks ALL verbs used (including non-leading)
    2. Only optimizes latest 3 experiences
    3. Ensures 80-90% bullets have metrics
    4. Prevents verb repetition globally
    """

    # ALL available power verbs
    ALL_POWER_VERBS = [
        # Leadership
        'Spearheaded', 'Directed', 'Led', 'Drove', 'Championed', 'Orchestrated',
        # Technical
        'Architected', 'Engineered', 'Built', 'Designed', 'Implemented', 'Developed',
        # Optimization
        'Optimized', 'Enhanced', 'Streamlined', 'Improved', 'Accelerated', 'Refined',
        # Scale
        'Scaled', 'Expanded', 'Migrated', 'Transformed', 'Modernized',
        # Delivery
        'Delivered', 'Shipped', 'Launched', 'Deployed', 'Released', 'Executed',
        # Other
        'Reduced', 'Increased', 'Created', 'Established', 'Coordinated'
    ]

    POWER_VERB_SYNONYMS = {
        'designed': ['architected', 'engineered', 'crafted', 'built', 'planned'],
        'built': ['engineered', 'developed', 'created', 'constructed', 'established'],
        'created': ['established', 'generated', 'initiated', 'built', 'developed'],
        'developed': ['engineered', 'built', 'implemented', 'delivered', 'created'],
        'implemented': ['deployed', 'executed', 'delivered', 'launched', 'established'],
        'reduced': ['decreased', 'minimized', 'cut', 'lowered', 'slashed'],
        'improved': ['enhanced', 'optimized', 'strengthened', 'boosted', 'elevated'],
        'increased': ['boosted', 'elevated', 'expanded', 'grew', 'scaled'],
        'led': ['spearheaded', 'directed', 'drove', 'championed', 'headed'],
        'managed': ['oversaw', 'directed', 'coordinated', 'supervised', 'administered'],
        'optimized': ['enhanced', 'streamlined', 'refined', 'accelerated', 'improved'],
        'delivered': ['shipped', 'launched', 'deployed', 'executed', 'released'],
        'collaborated': ['partnered', 'coordinated', 'teamed with', 'worked with'],
        'analyzed': ['evaluated', 'assessed', 'examined', 'investigated', 'studied'],
        'architected': ['engineered', 'designed', 'built', 'created', 'developed']
    }

    # Metric patterns
    METRIC_PATTERNS = [
        r'\d+%', r'\d+\+', r'\d+[KMB]\+?', r'\d+x',
        r'\d+\.\d+%', r'\d+,\d+', r'\d+TB', r'\d+GB',
        r'\d+ hours?', r'\d+ minutes?', r'\d+ users?',
        r'\d+ tables?', r'\d+ events?', r'\d+ reports?'
    ]

    def __init__(self, ai_assistant: AIResumeAssistant):
        """Initialize with AI assistant"""
        self.ai = ai_assistant
        self.used_verbs = Counter()  # Track ALL verb usage counts
        self.bullets_total = 0
        self.bullets_with_metrics = 0

    def optimize_content(
        self,
        content: str,
        section_type: str,
        keyword_profile: KeywordProfile,
        context: Dict = None
    ) -> OptimizationResult:
        """Optimize content with AI"""

        if not content or len(content.strip()) < 10:
            return OptimizationResult(
                original=content,
                optimized=content,
                keywords_added=[],
                improvements=["Skipped: Too short"],
                repetitions_fixed={},
                factuality_score=1.0,
                has_metrics=False
            )

        try:
            # Check if content already has metrics
            has_metrics_before = self._has_metrics(content)

            # Extract ALL verbs in content (not just leading)
            content_verbs = self._extract_all_verbs(content)
            for verb in content_verbs:
                self.used_verbs[verb.lower()] += 1

            # Get leading verb
            current_verb = self._extract_leading_verb(content)

            # Analyze repetitions
            repetition_analysis = self._analyze_repetitions(content)

            # Get keywords
            current_keywords = self._extract_keywords(content, keyword_profile)
            missing_keywords = self._find_missing_keywords(content, keyword_profile)

            # Get context tech
            context_tech = []
            if context and 'technologies' in context:
                context_tech = context['technologies'][:5]

            # Calculate metrics coverage
            metrics_coverage = (self.bullets_with_metrics / self.bullets_total * 100) if self.bullets_total > 0 else 0
            needs_metrics = not has_metrics_before and metrics_coverage < 85

            # Build enhanced prompt
            prompt = self._build_enhanced_prompt(
                content, section_type,
                missing_keywords, context_tech,
                repetition_analysis,
                dict(self.used_verbs),  # Pass verb counts
                needs_metrics
            )

            # Call AI
            optimized = self.ai.generate_content(f"{section_type}_optimization", prompt, "")

            if not optimized or len(optimized.strip()) == 0:
                return OptimizationResult(
                    original=content,
                    optimized=content,
                    keywords_added=[],
                    improvements=["No AI response"],
                    repetitions_fixed={},
                    factuality_score=1.0,
                    has_metrics=has_metrics_before
                )

            # Clean output
            optimized = self._clean_output(optimized, section_type)

            # Simple validation
            if not self._validate_simple(content, optimized):
                return OptimizationResult(
                    original=content,
                    optimized=content,
                    keywords_added=[],
                    improvements=["Validation failed"],
                    repetitions_fixed={},
                    factuality_score=0.5,
                    has_metrics=has_metrics_before
                )

            # Track new verbs in optimized content
            new_verbs = self._extract_all_verbs(optimized)
            for verb in new_verbs:
                if verb.lower() not in [v.lower() for v in content_verbs]:
                    self.used_verbs[verb.lower()] += 1

            # Check if metrics were added
            has_metrics_after = self._has_metrics(optimized)

            # Track improvements
            new_keywords = [k for k in self._extract_keywords(optimized, keyword_profile)
                          if k not in current_keywords]
            repetitions_fixed = self._count_repetitions_fixed(repetition_analysis, optimized)

            improvements = []
            if new_keywords:
                improvements.append(f"+{len(new_keywords)} keywords")
            if repetitions_fixed:
                improvements.append(f"Fixed {sum(repetitions_fixed.values())} reps")
            if has_metrics_after and not has_metrics_before:
                improvements.append("Added metrics")

            new_verb = self._extract_leading_verb(optimized)
            if new_verb and current_verb and new_verb.lower() != current_verb.lower():
                improvements.append(f"Varied verb")
            elif optimized != content:
                improvements.append("Enhanced")

            return OptimizationResult(
                original=content,
                optimized=optimized,
                keywords_added=new_keywords,
                improvements=improvements,
                repetitions_fixed=repetitions_fixed,
                factuality_score=1.0,
                has_metrics=has_metrics_after
            )

        except Exception as e:
            return OptimizationResult(
                original=content,
                optimized=content,
                keywords_added=[],
                improvements=[f"Error: {str(e)[:40]}"],
                repetitions_fixed={},
                factuality_score=1.0,
                has_metrics=False
            )

    def optimize_resume_data(
        self,
        resume_data: ResumeData,
        keyword_profile: KeywordProfile
    ) -> Tuple[ResumeData, Dict]:
        """Optimize complete resume - ONLY LATEST 3 EXPERIENCES"""

        # Reset counters
        self.used_verbs = Counter()
        self.bullets_total = 0
        self.bullets_with_metrics = 0

        stats = {
            'sections_optimized': 0,
            'keywords_added': 0,
            'repetitions_fixed': 0,
            'bullets_optimized': 0,
            'metrics_added': 0,
            'verbs_varied': 0,
            'errors': []
        }

        # 1. Optimize Summary
        if resume_data.summary:
            print("\n   📝 Professional Summary...")
            summary_text = (
                f"{resume_data.summary.title} with {resume_data.summary.years_of_experience}+ years "
                f"specializing in {', '.join(resume_data.summary.specializations)}. "
                f"{resume_data.summary.key_achievement}"
            )

            result = self.optimize_content(
                content=summary_text,
                section_type='summary',
                keyword_profile=keyword_profile,
                context={'role': resume_data.summary.title}
            )

            if result.optimized != result.original:
                print(f"      ✓ {', '.join(result.improvements)}")
                stats['sections_optimized'] += 1
                stats['keywords_added'] += len(result.keywords_added)
            else:
                print(f"      ⚠️  No changes")

        # 2. Optimize ONLY LATEST 3 EXPERIENCES
        print("\n   💼 Work Experience (Latest 3 only)...")
        experiences_to_optimize = resume_data.experience[:3]  # Only first 3

        for i, exp in enumerate(experiences_to_optimize):
            print(f"\n      Company {i+1}/3: {exp.company}")
            exp_stats = {'optimized': 0, 'keywords': 0, 'verbs': 0, 'metrics': 0}

            # Count total bullets first
            valid_bullets = [a for a in exp.achievements if len(a.strip()) >= 20]
            self.bullets_total += len(valid_bullets)

            # Count existing metrics
            for achievement in valid_bullets:
                if self._has_metrics(achievement):
                    self.bullets_with_metrics += 1

            # Now optimize
            for j, achievement in enumerate(exp.achievements):
                if len(achievement.strip()) < 20:
                    continue

                result = self.optimize_content(
                    content=achievement,
                    section_type='experience',
                    keyword_profile=keyword_profile,
                    context={
                        'company': exp.company,
                        'position': exp.position,
                        'technologies': exp.technologies
                    }
                )

                if result.optimized != result.original:
                    exp.achievements[j] = result.optimized
                    exp_stats['optimized'] += 1
                    exp_stats['keywords'] += len(result.keywords_added)

                    # Track metrics added
                    if result.has_metrics and not self._has_metrics(result.original):
                        exp_stats['metrics'] += 1
                        self.bullets_with_metrics += 1

                    if 'Varied verb' in ', '.join(result.improvements):
                        exp_stats['verbs'] += 1

                    stats['bullets_optimized'] += 1
                    stats['keywords_added'] += len(result.keywords_added)

            if exp_stats['optimized'] > 0:
                print(f"      ✓ {exp_stats['optimized']}/{len(valid_bullets)} bullets (+{exp_stats['keywords']} kw, {exp_stats['verbs']} verbs, {exp_stats['metrics']} metrics)")
                stats['sections_optimized'] += 1
                stats['verbs_varied'] += exp_stats['verbs']
                stats['metrics_added'] += exp_stats['metrics']
            else:
                print(f"      ⚠️  No changes")

        # Skip older experiences
        if len(resume_data.experience) > 3:
            print(f"\n      ⏭️  Skipped {len(resume_data.experience) - 3} older experiences")

        # 3. Optimize Projects
        featured = [p for p in resume_data.projects if p.is_featured]
        if featured:
            print("\n   🚀 Projects...")
            for i, proj in enumerate(featured):
                print(f"\n      Project {i+1}/{len(featured)}: {proj.name}")

                result = self.optimize_content(
                    content=proj.description,
                    section_type='projects',
                    keyword_profile=keyword_profile,
                    context={
                        'project_name': proj.name,
                        'technologies': proj.technologies
                    }
                )

                if result.optimized != result.original:
                    proj.description = result.optimized
                    print(f"      ✓ {', '.join(result.improvements)}")
                    stats['sections_optimized'] += 1
                    stats['keywords_added'] += len(result.keywords_added)
                else:
                    print(f"      ⚠️  No changes")

        # Calculate metrics coverage
        metrics_coverage = (self.bullets_with_metrics / self.bullets_total * 100) if self.bullets_total > 0 else 0

        # Print summary
        print(f"\n   {'='*76}")
        print(f"   ✅ OPTIMIZATION SUMMARY")
        print(f"   {'='*76}")
        print(f"   Sections Optimized:     {stats['sections_optimized']}")
        print(f"   Bullets Optimized:      {stats['bullets_optimized']}")
        print(f"   Keywords Added:         {stats['keywords_added']}")
        print(f"   Verbs Varied:           {stats['verbs_varied']}")
        print(f"   Metrics Added:          {stats['metrics_added']}")
        print(f"   Metrics Coverage:       {self.bullets_with_metrics}/{self.bullets_total} ({metrics_coverage:.1f}%)")
        print(f"   Unique Verbs Used:      {len(self.used_verbs)}")

        # Show most used verbs
        if self.used_verbs:
            top_verbs = self.used_verbs.most_common(5)
            print(f"   Top Verbs:              {', '.join([f'{v}({c})' for v, c in top_verbs])}")

        print(f"   {'='*76}")

        return resume_data, stats

    # ==================== HELPER METHODS ====================

    def _has_metrics(self, content: str) -> bool:
        """Check if content has quantified metrics"""
        return any(re.search(pattern, content) for pattern in self.METRIC_PATTERNS)

    def _extract_leading_verb(self, content: str) -> str:
        """Extract the leading verb from a bullet"""
        match = re.match(r'^([A-Z][a-z]+)', content.strip())
        return match.group(1) if match else ""

    def _extract_all_verbs(self, content: str) -> List[str]:
        """Extract ALL power verbs from content (not just leading)"""
        found_verbs = []
        content_lower = content.lower()

        for verb in self.ALL_POWER_VERBS:
            pattern = r'\b' + re.escape(verb.lower()) + r'\b'
            if re.search(pattern, content_lower):
                found_verbs.append(verb)

        return found_verbs

    def _build_enhanced_prompt(
        self,
        content: str,
        section_type: str,
        missing_keywords: List[str],
        context_tech: List[str],
        repetition_analysis: RepetitionAnalysis,
        verb_counts: Dict[str, int],
        needs_metrics: bool
    ) -> str:
        """Build enhanced prompt with verb avoidance and metrics guidance"""

        # Get overused verbs (used 3+ times)
        overused_verbs = [v for v, count in verb_counts.items() if count >= 3]

        # Get available verbs
        available_verbs = [v for v in self.ALL_POWER_VERBS if v.lower() not in overused_verbs]

        # Current verb warning
        current_verb = self._extract_leading_verb(content)
        verb_warning = ""
        if current_verb and current_verb.lower() in verb_counts:
            count = verb_counts[current_verb.lower()]
            if count >= 2:
                verb_warning = f"\n🚨 CRITICAL: '{current_verb}' already used {count}x. MUST use different verb!"

        # Metrics guidance
        metrics_guidance = ""
        if needs_metrics:
            metrics_guidance = "\n⚠️ IMPORTANT: This bullet LACKS metrics! Add quantified impact (numbers, %, scale, users, etc.)"

        # Keywords
        relevant_kw = []
        for kw in missing_keywords[:5]:
            kw_lower = kw.lower()
            if kw_lower in ['ai', 'ml', 'llm', 'rag', 'genai']:
                if any(tech.lower() in ['vector', 'semantic', 'nlp', 'ai', 'ml'] for tech in context_tech):
                    relevant_kw.append(kw)
            else:
                relevant_kw.append(kw)

        if section_type == 'experience':
            prompt = f"""Improve this resume bullet for maximum impact.

CURRENT:
{content}

KEYWORDS: {', '.join(relevant_kw[:3]) if relevant_kw else 'Focus on existing tech'}
TECH CONTEXT: {', '.join(context_tech[:3]) if context_tech else 'General'}

⛔ VERBS TO AVOID (already overused):
{', '.join(overused_verbs) if overused_verbs else 'None'}
{verb_warning}

✅ AVAILABLE VERBS (use these):
{', '.join(available_verbs[:12])}
{metrics_guidance}

INSTRUCTIONS:
1. Keep ALL existing numbers (%, +, K/M, etc.)
2. Start with a FRESH verb from "Available Verbs"
3. {'Add quantified metrics (numbers, %, scale)' if needs_metrics else 'Keep existing metrics'}
4. Add 1-2 relevant keywords
5. Maximum 2 lines

GOOD EXAMPLES:
- "Built pipeline" → "Engineered real-time pipeline processing 50M+ events with 99.9% uptime"
- "Improved system" → "Optimized query performance by 60% reducing latency from 3s to 1.2s"

OUTPUT: Improved bullet only (no explanation)"""

        elif section_type == 'summary':
            prompt = f"""Enhance this professional summary.

CURRENT:
{content}

KEYWORDS: {', '.join(relevant_kw[:2]) if relevant_kw else 'None'}

INSTRUCTIONS:
1. Keep ALL years and numbers
2. Add 1-2 relevant buzzwords
3. Sound more impressive
4. 60-80 words max

OUTPUT: Enhanced summary only"""

        else:  # projects
            prompt = f"""Improve this project description.

CURRENT:
{content}

KEYWORDS: {', '.join(relevant_kw[:2]) if relevant_kw else 'None'}

INSTRUCTIONS:
1. Keep technical details
2. Add specific tech stack
3. Show scale/impact clearly
4. 1-2 lines

OUTPUT: Improved description only"""

        return prompt

    def _validate_simple(self, original: str, optimized: str) -> bool:
        """Simple validation"""
        orig_nums = re.findall(r'\d+', original)
        preserved = sum(1 for num in orig_nums if num in optimized)

        if orig_nums and preserved / len(orig_nums) < 0.8:
            return False

        if len(optimized) > len(original) * 3 or len(optimized) < len(original) * 0.4:
            return False

        return True

    def _analyze_repetitions(self, content: str) -> RepetitionAnalysis:
        """Analyze word repetitions"""
        words = re.findall(r'\b[a-z]+\b', content.lower())
        word_counts = Counter(words)

        repeated_words = {}
        suggested_synonyms = {}

        for word, count in word_counts.items():
            if count >= 3 and len(word) > 3:
                repeated_words[word] = count
                if word in self.POWER_VERB_SYNONYMS:
                    suggested_synonyms[word] = self.POWER_VERB_SYNONYMS[word]

        severity = "low" if not repeated_words else "high"

        return RepetitionAnalysis(
            repeated_words=repeated_words,
            suggested_synonyms=suggested_synonyms,
            severity=severity
        )

    def _count_repetitions_fixed(self, original_analysis: RepetitionAnalysis, optimized: str) -> Dict[str, int]:
        """Count repetitions fixed"""
        fixed = {}
        opt_words = re.findall(r'\b[a-z]+\b', optimized.lower())
        opt_counts = Counter(opt_words)

        for word, orig_count in original_analysis.repeated_words.items():
            new_count = opt_counts.get(word, 0)
            if new_count < orig_count:
                fixed[word] = orig_count - new_count

        return fixed

    def _extract_keywords(self, content: str, profile: KeywordProfile) -> List[str]:
        """Extract keywords present"""
        found = []
        content_lower = content.lower()
        for keyword in profile.primary_keywords + profile.secondary_keywords:
            if keyword.lower() in content_lower:
                found.append(keyword)
        return found

    def _find_missing_keywords(self, content: str, profile: KeywordProfile) -> List[str]:
        """Find missing keywords"""
        missing = []
        content_lower = content.lower()
        for keyword in profile.primary_keywords:
            if keyword.lower() not in content_lower:
                missing.append(keyword)
        return missing[:10]

    def _clean_output(self, text: str, section_type: str) -> str:
        """Clean AI output"""
        if not text:
            return text

        text = text.strip()
        text = re.sub(r'^[\d\-\*•]+[\.\)]\s*', '', text)
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)

        if section_type == 'experience':
            sentences = re.split(r'[.!?]\s+', text)
            if len(sentences) > 2:
                text = sentences[0]
                if not text.endswith('.'):
                    text += '.'

        text = re.sub(r'\s+', ' ', text)
        return text.strip()


class BatchOptimizer:
    """Deprecated"""
    def __init__(self, optimizer: IntelligentResumeOptimizer):
        self.optimizer = optimizer
