"""Smart summary selection for reducing prompt sizes."""

import re
import logging
from typing import List, Dict, Optional, Set
from dataclasses import dataclass, field
from collections import Counter
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class ResearchSummary:
    """Research summary with metadata."""

    text: str
    title: str = ""
    url: str = ""
    relevance_score: float = 0.0
    tokens_estimate: int = 0
    keywords: Set[str] = field(default_factory=set)
    year: Optional[int] = None

    @property
    def word_count(self) -> int:
        """Estimate word count."""
        return len(self.text.split())

    def __len__(self) -> int:
        return len(self.text)


@dataclass
class SelectionConfig:
    """Configuration for summary selection."""

    max_total_tokens: int = 4000
    max_summaries: int = 5
    min_relevance_score: float = 0.5
    recent_year_bonus: float = 0.1
    keyword_match_bonus: float = 0.15
    diversity_weight: float = 0.3
    relevance_weight: float = 0.7


class SummarySelector:
    """Select most relevant research summaries to reduce prompt size."""

    def __init__(self, config: Optional[SelectionConfig] = None):
        self._config = config or SelectionConfig()

    def _extract_keywords(self, text: str, max_keywords: int = 10) -> Set[str]:
        """Extract important keywords from text."""
        # Convert to lowercase and remove special characters
        cleaned = re.sub(r"[^\w\s]", " ", text.lower())

        # Extract words (filter out common stop words)
        stop_words = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
            "from",
            "is",
            "are",
            "was",
            "were",
            "be",
            "been",
            "being",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "will",
            "would",
            "should",
            "could",
            "may",
            "might",
            "must",
            "can",
            "this",
            "that",
            "these",
            "those",
            "it",
            "its",
            "we",
            "our",
            "their",
            "as",
            "if",
            "then",
            "when",
            "where",
            "how",
        }

        words = [w for w in cleaned.split() if w not in stop_words and len(w) > 3]

        # Count word frequency
        word_freq = Counter(words)

        # Return top keywords
        top_words = word_freq.most_common(max_keywords)
        return {word for word, _ in top_words}

    def _compute_keyword_overlap(
        self, summary_keywords: Set[str], query_keywords: Set[str]
    ) -> float:
        """Compute keyword overlap score."""
        if not query_keywords:
            return 0.0

        overlap = summary_keywords & query_keywords
        return len(overlap) / max(len(query_keywords), 1)

    def _compute_relevance_score(
        self,
        summary: ResearchSummary,
        query: str,
        query_keywords: Optional[Set[str]] = None,
    ) -> float:
        """Compute relevance score for a summary."""
        if query_keywords is None:
            query_keywords = self._extract_keywords(query)

        score = summary.relevance_score

        # Keyword match bonus
        if summary.keywords:
            keyword_score = self._compute_keyword_overlap(
                summary.keywords, query_keywords
            )
            score += keyword_score * self._config.keyword_match_bonus

        # Recent year bonus
        if summary.year:
            current_year = datetime.now().year
            age = current_year - summary.year
            recent_bonus = max(0, 1 - age / 5) * self._config.recent_year_bonus
            score += recent_bonus

        return min(score, 1.0)

    def _compute_diversity_score(
        self, summary: ResearchSummary, selected_summaries: List[ResearchSummary]
    ) -> float:
        """Compute diversity score relative to already selected summaries."""
        if not selected_summaries:
            return 1.0

        diversity_scores = []
        for selected in selected_summaries:
            keyword_overlap = self._compute_keyword_overlap(
                summary.keywords, selected.keywords
            )
            diversity_scores.append(1 - keyword_overlap)

        return sum(diversity_scores) / len(diversity_scores)

    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count (rough approximation)."""
        return int(len(text.split()) * 1.3)

    def select_summaries(
        self,
        summaries: List[ResearchSummary],
        query: str,
    ) -> List[ResearchSummary]:
        """
        Select the most relevant and diverse summaries.

        Args:
            summaries: List of research summaries to select from
            query: Query string for relevance matching

        Returns:
            List of selected summaries
        """
        if not summaries:
            return []

        # Extract keywords from query
        query_keywords = self._extract_keywords(query)

        # Compute relevance scores for all summaries
        scored_summaries = []
        for summary in summaries:
            summary.keywords = summary.keywords or self._extract_keywords(summary.text)
            summary.tokens_estimate = self._estimate_tokens(summary.text)
            relevance = self._compute_relevance_score(summary, query, query_keywords)
            scored_summaries.append((summary, relevance))

        # Filter by minimum relevance score
        scored_summaries = [
            (s, r) for s, r in scored_summaries if r >= self._config.min_relevance_score
        ]

        if not scored_summaries:
            return []

        # Sort by relevance score
        scored_summaries.sort(key=lambda x: x[1], reverse=True)

        # Greedy selection with diversity consideration
        selected: List[ResearchSummary] = []
        total_tokens = 0

        for summary, relevance in scored_summaries:
            if len(selected) >= self._config.max_summaries:
                break

            # Check token budget
            new_tokens = total_tokens + summary.tokens_estimate
            if new_tokens > self._config.max_total_tokens:
                continue

            # Compute final score (relevance + diversity)
            diversity = self._compute_diversity_score(summary, selected)
            final_score = (
                relevance * self._config.relevance_weight
                + diversity * self._config.diversity_weight
            )

            # Insert at appropriate position
            inserted = False
            for i in range(len(selected)):
                existing = selected[i]
                existing_relevance = self._compute_relevance_score(
                    existing, query, query_keywords
                )
                existing_diversity = self._compute_diversity_score(
                    existing, selected[:i] + selected[i + 1 :]
                )
                existing_score = (
                    existing_relevance * self._config.relevance_weight
                    + existing_diversity * self._config.diversity_weight
                )

                if final_score > existing_score:
                    selected.insert(i, summary)
                    inserted = True
                    break

            if not inserted:
                selected.append(summary)

            total_tokens = sum(s.tokens_estimate for s in selected)

        logger.debug(
            "Selected %d summaries from %d candidates (target tokens: %d, actual: %d)",
            len(selected),
            len(summaries),
            self._config.max_total_tokens,
            total_tokens,
        )

        return selected

    def prepare_context(
        self, summaries: List[ResearchSummary], query: str
    ) -> Dict[str, any]:
        """
        Prepare context with selected summaries.

        Args:
            summaries: List of research summaries
            query: Query string

        Returns:
            Dictionary with context information
        """
        selected = self.select_summaries(summaries, query)

        return {
            "summaries": selected,
            "count": len(selected),
            "total_tokens": sum(s.tokens_estimate for s in selected),
            "total_words": sum(s.word_count for s in selected),
            "avg_relevance": sum(
                self._compute_relevance_score(s, query) for s in selected
            )
            / len(selected)
            if selected
            else 0.0,
        }


def create_research_summaries(
    search_results: List[Dict[str, any]],
) -> List[ResearchSummary]:
    """
    Convert Exa search results to ResearchSummary objects.

    Args:
        search_results: List of search result dictionaries

    Returns:
        List of ResearchSummary objects
    """
    summaries = []

    for result in search_results:
        text = result.get("text", result.get("summary", "") or result.get("title", ""))
        if text:
            # Extract year from URL or published date if available
            year = None
            if "publishedDate" in result:
                try:
                    year = datetime.fromisoformat(result["publishedDate"]).year
                except:
                    pass

            summary = ResearchSummary(
                text=text[:5000],
                title=result.get("title", "")[:200],
                url=result.get("url", "")[:500],
                relevance_score=result.get("score", 0.5),
                year=year,
            )
            summaries.append(summary)

    return summaries
