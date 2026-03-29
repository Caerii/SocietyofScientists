"""Research integration for literature search and citation management."""

import asyncio
import logging
import re
from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import httpx

logger = logging.getLogger(__name__)


class DatabaseType(str, Enum):
    """Available research databases."""

    PUBMED = "pubmed"
    ARXIV = "arxiv"
    CROSSREF = "crossref"
    SEMANTIC_SCHOLAR = "semantic_scholar"
    EXA = "exa"


@dataclass
class Citation:
    """Academic citation."""

    id: str = ""
    title: str = ""
    authors: List[str] = field(default_factory=list)
    journal: str = ""
    year: int = 0
    volume: str = ""
    issue: str = ""
    pages: str = ""
    doi: str = ""
    pmid: str = ""
    abstract: str = ""
    keywords: Set[str] = field(default_factory=set)
    relevance_score: float = 0.0
    citation_count: int = 0

    def format_apa(self) -> str:
        """Format citation in APA style."""
        authors_str = ", ".join(self.authors[:3])
        if len(self.authors) > 3:
            authors_str += ", et al."

        if self.doi:
            return f"{authors_str} ({self.year}). {self.title}. {self.journal}, {self.volume}({self.issue}), {self.pages}. https://doi.org/{self.doi}"
        else:
            return f"{authors_str} ({self.year}). {self.title}. {self.journal}, {self.volume}({self.issue}), {self.pages}."

    def format_vancouver(self) -> str:
        """Format citation in Vancouver style."""
        if len(self.authors) > 6:
            authors_str = f"{self.authors[0]} et al."
        else:
            authors_str = ", ".join(self.authors)

        return f"{authors_str}. {self.journal} {self.year};{self.volume}({self.issue}):{self.pages}."


class ResearchIntegrator:
    """Integrate with academic databases for literature search."""

    def __init__(self):
        self._client = httpx.AsyncClient(timeout=30.0)
        self._cache = {}

    async def search_papers(
        self,
        query: str,
        database: DatabaseType = DatabaseType.PUBMED,
        max_results: int = 20,
        year_from: Optional[int] = None,
    ) -> List[Citation]:
        """
        Search for academic papers across databases.

        Args:
            query: Search query
            database: Database to search
            max_results: Maximum number of results
            year_from: Minimum publication year

        Returns:
            List of citations
        """
        cache_key = f"{database.value}:{query}:{max_results}:{year_from or 'all'}"

        if cache_key in self._cache:
            logger.debug("Returning cached results for %s", cache_key)
            return self._cache[cache_key]

        try:
            if database == DatabaseType.PUBMED:
                citations = await self._search_pubmed(query, max_results, year_from)
            elif database == DatabaseType.ARXIV:
                citations = await self._search_arxiv(query, max_results)
            elif database == DatabaseType.CROSSREF:
                citations = await self._search_crossref(query, max_results, year_from)
            elif database == DatabaseType.SEMANTIC_SCHOLAR:
                citations = await self._search_semantic_scholar(query, max_results)
            else:
                citations = []

            citations = citations[:max_results]
            self._cache[cache_key] = citations
            return citations

        except Exception as e:
            logger.error("Failed to search %s: %s", database.value, e, exc_info=True)
            return []

    async def _search_pubmed(
        self, query: str, max_results: int, year_from: Optional[int]
    ) -> List[Citation]:
        """Search PubMed database."""
        try:
            # PubMed API endpoint
            base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

            # Search for PMIDs
            search_url = f"{base_url}/esearch.fcgi"
            params = {
                "db": "pubmed",
                "term": query,
                "retmax": max_results,
                "retmode": "json",
            }

            if year_from:
                params["term"] += f" AND {year_from}:3000[PDAT]"

            response = await self._client.get(search_url, params=params)
            data = response.json()
            pmids = data.get("esearchresult", {}).get("idlist", [])

            if not pmids:
                return []

            # Fetch details
            summary_url = f"{base_url}/esummary.fcgi"
            params = {
                "db": "pubmed",
                "id": ",".join(pmids),
                "retmode": "json",
            }

            response = await self._client.get(summary_url, params=params)
            data = response.json()
            results = data.get("result", {})

            citations = []
            for pmid in pmids:
                if pmid == "uids":
                    continue

                article_data = results.get(pmid, {})
                citation = Citation()
                citation.pmid = pmid
                citation.title = article_data.get("title", "").rstrip(".")
                citation.authors = [
                    author.get("name", "") for author in article_data.get("authors", [])
                ]
                citation.journal = article_data.get("source", "")
                citation.year = article_data.get("pubdate", "")[:4].strip() or 0
                citation.volume = article_data.get("volume", "")
                citation.issue = article_data.get("issue", "")
                citation.pages = article_data.get("pages", "")

                citations.append(citation)

            return citations

        except Exception as e:
            logger.error("PubMed search failed: %s", e)
            return []

    async def _search_arxiv(self, query: str, max_results: int) -> List[Citation]:
        """Search arXiv database."""
        try:
            # arXiv API
            base_url = "http://export.arxiv.org/api/query"
            params = {
                "search_query": f"all:{query}",
                "max_results": max_results,
                "start": 0,
            }

            response = await self._client.get(base_url, params=params)
            content = response.text

            citations = []
            # Parse arXiv XML response
            import xml.etree.ElementTree as ET

            root = ET.fromstring(content)

            # Define namespace
            ns = {
                "atom": "http://www.w3.org/2005/Atom",
                "arxiv": "http://arxiv.org/schemas/atom",
            }

            for entry in root.findall("atom:entry", ns):
                citation = Citation()
                citation.id = entry.find("atom:id", ns).text
                citation.title = entry.find("atom:title", ns).text.strip()

                # Parse authors
                authors = entry.findall("atom:author", ns)
                citation.authors = [
                    author.find("atom:name", ns).text for author in authors
                ]

                # Parse year
                published = entry.find("atom:published", ns).text
                if published:
                    citation.year = int(published[:4])

                # Parse summary (abstract)
                summary = entry.find("atom:summary", ns)
                if summary is not None:
                    citation.abstract = summary.text.strip()

                citations.append(citation)

            return citations

        except Exception as e:
            logger.error("arXiv search failed: %s", e)
            return []

    async def _search_crossref(
        self, query: str, max_results: int, year_from: Optional[int]
    ) -> List[Citation]:
        """Search CrossRef database."""
        try:
            # CrossRef API
            base_url = "https://api.crossref.org/works"
            params = {
                "query": query,
                "rows": max_results,
                "select": "title,author,container-title,volume,issue,page,published-online,DOI",
            }

            if year_from:
                params["filter"] = f"from-pub-date:{year_from}"

            response = await self._client.get(base_url, params=params)
            data = response.json()

            citations = []
            for item in data.get("message", {}).get("items", []):
                citation = Citation()
                citation.title = (
                    " ".join(item.get("title", [])) if item.get("title") else ""
                )
                citation.authors = [
                    f"{a.get('given', '')} {a.get('family', '')}"
                    for a in item.get("author", [])
                ]
                citation.journal = (
                    " ".join(item.get("container-title", []))
                    if item.get("container-title")
                    else ""
                )
                citation.volume = item.get("volume", "")
                citation.issue = item.get("issue", "")
                citation.pages = item.get("page", "")
                citation.doi = item.get("DOI", "")

                # Parse year
                published = item.get("published-online", {})
                if isinstance(published, dict) and "date-parts" in published:
                    citation.year = published["date-parts"][0][0]

                citations.append(citation)

            return citations

        except Exception as e:
            logger.error("CrossRef search failed: %s", e)
            return []

    async def _search_semantic_scholar(
        self, query: str, max_results: int
    ) -> List[Citation]:
        """Search Semantic Scholar database."""
        try:
            # Semantic Scholar API
            base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
            params = {
                "query": query,
                "limit": max_results,
                "fields": "title,authors,year,journal,citationCount,abstract,externalIds",
            }

            response = await self._client.get(base_url, params=params)
            data = response.json()

            citations = []
            for item in data.get("data", []):
                citation = Citation()
                citation.title = item.get("title", "")
                citation.authors = [a.get("name", "") for a in item.get("authors", [])]
                citation.year = item.get("year", 0)
                citation.journal = item.get("journal", {}).get("name", "")
                citation.citation_count = item.get("citationCount", 0)
                citation.abstract = item.get("abstract", "")

                external_ids = item.get("externalIds", {})
                citation.doi = external_ids.get("DOI", "")
                citation.pmid = external_ids.get("PubMed", "")

                citations.append(citation)

            return citations

        except Exception as e:
            logger.error("Semantic Scholar search failed: %s", e)
            return []

    async def get_citation_metrics(self, doi: str) -> Dict[str, int]:
        """Get citation metrics for a paper."""
        try:
            url = f"https://api.crossref.org/works/{doi}"
            response = await self._client.get(url)
            data = response.json()

            message = data.get("message", {})
            return {
                "is_referenced_by_count": message.get("is-referenced-by-count", 0),
            }
        except Exception as e:
            logger.error("Failed to get citation metrics: %s", e)
            return {}

    async def close(self):
        """Close the HTTP client."""
        await self._client.aclose()


class CitationManager:
    """Manage citations within proposal text."""

    def __init__(self, citations: List[Citation] = None):
        self._citations: List[Citation] = citations or []
        self._citation_map = {c.id: i for i, c in enumerate(self._citations)}
        self._used_references: Set[str] = set()

    def add_citation(self, citation: Citation) -> int:
        """Add a citation and return its index."""
        if citation.id not in self._citation_map:
            self._citations.append(citation)
            self._citation_map[citation.id] = len(self._citations) - 1
        return self._citation_map[citation.id]

    def get_citation(self, index: int) -> Optional[Citation]:
        """Get citation by index."""
        if 0 <= index < len(self._citations):
            return self._citations[index]
        return None

    def get_best_match(self, text: str) -> Optional[Citation]:
        """Find best matching citation for text."""
        if not self._citations:
            return None

        best_citation = None
        best_score = 0.0

        text_lower = text.lower()
        text_words = set(text_lower.split())

        for citation in self._citations:
            score = 0.0

            # Check title overlap
            title_words = set(citation.title.lower().split())
            title_overlap = text_words & title_words
            score += len(title_overlap) * 2

            # Check abstract overlap
            if citation.abstract:
                abstract_words = set(citation.abstract.lower().split())
                abstract_overlap = text_words & abstract_words
                score += len(abstract_overlap)

            # Keyword overlap
            if citation.keywords:
                keyword_overlap = text_words & citation.keywords
                score += len(keyword_overlap) * 3

            # Year recency bonus
            current_year = datetime.now().year
            if citation.year > 0:
                age = current_year - citation.year
                if age < 2:
                    score += 1
                elif age < 5:
                    score += 0.5

            if score > best_score:
                best_score = score
                best_citation = citation

        return best_citation if best_score > 0 else None

    def insert_citations(
        self, text: str, style: str = "numeric"
    ) -> tuple[str, List[Citation]]:
        """
        Insert citations into text.

        Args:
            text: Input text
            style: Citation style (numeric, author-year, apa)

        Returns:
            Tuple of (text with citations, used citations)
        """
        used_citations = []
        citation_pattern = r"\[cite:([^\]]+)\]"

        def replace_citation(match):
            citation_key = match.group(1)
            best_match = None

            # Find best matching citation
            for citation in self._citations:
                if (
                    citation.id == citation_key
                    or citation_key.lower() in citation.title.lower()
                ):
                    best_match = citation
                    break

            if not best_match:
                # Try keyword matching
                best_match = self.get_best_match(citation_key)

            if not best_match:
                return match.group(0)

            idx = self.add_citation(best_match)
            if idx not in [c.id for c in used_citations]:
                cit_ref = self.get_citation(idx)
                if cit_ref:
                    used_citations.append(cit_ref)

            if style == "numeric":
                return f"[{idx + 1}]"
            elif style == "author-year":
                if best_match.authors:
                    author = best_match.authors[0].split()[-1]
                    return f"({author}, {best_match.year})"
            elif style == "apa":
                return f"({best_match.format_apa()})"

            return match.group(0)

        annotated_text = re.sub(citation_pattern, replace_citation, text)
        return annotated_text, used_citations

    def generate_reference_list(self, style: str = "apa") -> str:
        """Generate formatted reference list."""
        if not self._citations:
            return ""

        references = []
        for i, citation in enumerate(self._citations):
            if style == "apa":
                formatted = f"{i + 1}. {citation.format_apa()}"
            elif style == "vancouver":
                formatted = f"{i + 1}. {citation.format_vancouver()}"
            else:
                formatted = f"{i + 1}. {citation.title}"

            references.append(formatted)

        return "\n\n".join(["## References\n"] + references)

    def export_bib(self) -> str:
        """Export citations in BibTeX format."""
        bib_entries = []

        for citation in self._citations:
            key = re.sub(r"[^a-zA-Z0-9]", "", citation.title[:50].lower())
            key = f"{citation.authors[0].split()[-1] if citation.authors else 'unknown'}{citation.year}{key}"

            entry = f"@article{{{key},\n"
            entry += f"  title = {{{citation.title}}},\n"
            if citation.authors:
                entry += f"  author = {{{' and '.join(citation.authors)}}},\n"
            if citation.journal:
                entry += f"  journal = {{{citation.journal}}},\n"
            if citation.year:
                entry += f"  year = {{{citation.year}}},\n"
            if citation.volume:
                entry += f"  volume = {{{citation.volume}}},\n"
            if citation.issue:
                entry += f"  number = {{{citation.issue}}},\n"
            if citation.pages:
                entry += f"  pages = {{{citation.pages}}},\n"
            if citation.doi:
                entry += f"  doi = {{{citation.doi}}},\n"
            entry += "}\n"

            bib_entries.append(entry)

        return "\n".join(bib_entries)


async def search_relevant_papers(
    topic: str,
    num_papers: int = 20,
    databases: List[DatabaseType] = None,
) -> List[Citation]:
    """
    Search for relevant papers across multiple databases.

    Args:
        topic: Research topic
        num_papers: Number of papers to return
        databases: List of databases to search

    Returns:
        List of relevant citations
    """
    if databases is None:
        databases = [DatabaseType.SEMANTIC_SCHOLAR, DatabaseType.PUBMED]

    integrator = ResearchIntegrator()
    try:
        all_citations = []

        for database in databases:
            citations = await integrator.search_papers(topic, database, num_papers)
            all_citations.extend(citations)

        # Remove duplicates based on title similarity
        unique_citations = []
        seen_titles = set()

        for citation in all_citations:
            title_lower = citation.title.lower()
            if title_lower not in seen_titles:
                seen_titles.add(title_lower)
                unique_citations.append(citation)

        # Sort by relevance score
        unique_citations.sort(key=lambda c: c.citation_count, reverse=True)

        return unique_citations[:num_papers]

    finally:
        await integrator.close()
