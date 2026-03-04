"""Exa API integration for research paper search with cached data support."""

import logging
import os
from typing import List, Dict, Any, Optional
from exa_py import Exa
from ..config import Settings
from .data_loader import load_research_summaries

logger = logging.getLogger(__name__)


class ExaSearch:
    """Wrapper for Exa API research paper search."""

    def __init__(self, api_key: Optional[str] = None, use_cache: bool = True):
        """
        Initialize ExaSearch with API key.

        Args:
            api_key: Exa API key. If not provided, will use EXA_API_KEY from settings.
            use_cache: If True, will use cached summaries from exported files first (default: True)
        """
        settings = Settings()
        self.api_key = api_key or settings.get_exa_api_key()
        self.exa = Exa(api_key=self.api_key) if self.api_key else None
        self.result = None
        self.use_cache = use_cache
        self._cached_summaries = None

    def get_cached_summaries(self, topic: Optional[str] = None) -> List[str]:
        """
        Get cached research summaries from exported files.

        Args:
            topic: Optional topic filter. If None, returns all summaries.

        Returns:
            List of summary strings
        """
        if self._cached_summaries is None:
            self._cached_summaries = load_research_summaries(topic)
        return self._cached_summaries

    def search_papers(
        self,
        query: str,
        search_type: str = "neural",
        num_results: int = 20,
        category: str = "research paper",
        start_date: str = "2019-09-01T04:00:01.000Z",
        autoprompt: bool = True,
        exclude_domains: Optional[List[str]] = None,
        include_html_tags: bool = True,
        livecrawl: str = "always",
        highlights: bool = True,
        use_cache_first: bool = True,
    ) -> Any:
        """
        Search for research papers. By default, uses cached summaries first.

        Args:
            query: Search query
            search_type: Type of search (default: "neural")
            num_results: Number of results to return
            category: Category filter (default: "research paper")
            start_date: Start date for papers (ISO format)
            autoprompt: Whether to use autoprompt
            exclude_domains: List of domains to exclude
            include_html_tags: Whether to include HTML tags in text
            livecrawl: Live crawl setting
            highlights: Whether to include highlights
            use_cache_first: If True, returns cached summaries instead of API call (default: True)

        Returns:
            Search results from Exa API or cached summaries
        """
        # Use cached summaries by default to avoid API calls
        if use_cache_first and self.use_cache:
            summaries = self.get_cached_summaries()
            if summaries:
                # Return a mock result structure compatible with existing code
                class CachedResult:
                    def __init__(self, summaries_list):
                        self.results = [
                            type("Result", (), {"summary": s, "title": "", "url": ""})()
                            for s in summaries_list[:num_results]
                        ]

                self.result = CachedResult(summaries)
                return self.result

        # Fall back to Exa API if cache not available or use_cache_first is False
        if not self.exa:
            raise ValueError("Exa API key not configured and no cached data available")

        if exclude_domains is None:
            exclude_domains = ["en.wikipedia.org"]

        try:
            self.result = self.exa.search(
                query,
                type=search_type,
                num_results=num_results,
                contents={"text": True},
                category=category,
                exclude_domains=exclude_domains,
            )
            return self.result
        except Exception as e:
            logger.warning("Exa API call failed: %s — falling back to cached data", e)
            summaries = self.get_cached_summaries()
            if summaries:

                class CachedResult:
                    def __init__(self, summaries_list):
                        self.results = [
                            type("Result", (), {"summary": s, "title": "", "url": ""})()
                            for s in summaries_list[:num_results]
                        ]

                self.result = CachedResult(summaries)
                return self.result
            raise

    def parse_results(self, fields: List[str]) -> List[Dict[str, Any]]:
        """
        Parse search results and extract specified fields.

        Args:
            fields: List of field names to extract

        Returns:
            List of dictionaries with extracted fields

        Raises:
            ValueError: If no results found
        """
        if self.result is None:
            raise ValueError("No search results available. Run search_papers() first.")

        parsed_data = []
        if hasattr(self.result, "results"):
            for entry in self.result.results:
                parsed_entry = {field: getattr(entry, field, None) for field in fields}
                parsed_data.append(parsed_entry)
        else:
            raise ValueError(
                "No 'results' found in the response. Please check the search query or result structure."
            )

        return parsed_data

    def get_parsed_results(self, fields: List[str]) -> List[Dict[str, Any]]:
        """
        Get parsed results for specified fields.

        Args:
            fields: List of field names to extract

        Returns:
            List of dictionaries with extracted fields
        """
        return self.parse_results(fields)

    def export_results_to_file(
        self,
        fields: List[str],
        filename: str = "search_results.txt",
        output_dir: Optional[str] = None,
    ) -> str:
        """
        Export parsed results to a text file.

        Args:
            fields: List of field names to export
            filename: Output filename
            output_dir: Output directory (defaults to data directory from settings)

        Returns:
            Path to the exported file
        """
        parsed_results = self.parse_results(fields)

        if output_dir is None:
            settings = Settings()
            output_dir = settings.DATA_DIR
            os.makedirs(output_dir, exist_ok=True)

        file_path = os.path.join(output_dir, filename)

        with open(file_path, "w", encoding="utf-8") as file:
            for entry in parsed_results:
                for field, value in entry.items():
                    file.write(f"{field}: {value}\n")
                file.write("\n")

        return file_path


def exa_search_function(query: str, use_cache: bool = True) -> str:
    """
    AutoGen-compatible function for Exa search. Uses cached data by default.

    Args:
        query: Search query string
        use_cache: If True, uses cached summaries first (default: True)

    Returns:
        Formatted search results as string
    """
    search = ExaSearch(use_cache=use_cache)
    result = search.search_papers(query, num_results=20, use_cache_first=use_cache)

    # Format results for return
    if hasattr(result, "results") and result.results:
        formatted = []
        for paper in result.results[:10]:  # Return top 10 summaries
            title = getattr(paper, "title", "")
            url = getattr(paper, "url", "")
            summary = getattr(paper, "summary", "No summary")
            if title:
                formatted.append(f"Title: {title}\nURL: {url}\nSummary: {summary}\n")
            else:
                # For cached results, just return the summary
                formatted.append(f"Summary: {summary}\n")
        return "\n".join(formatted) if formatted else "No results found."

    return "No results found."
