"""Enhanced agent orchestration with iterative refinement."""

import asyncio
import logging
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


class AgentRole(str, Enum):
    """Agent roles in the proposal generation pipeline."""

    DIRECTOR = "director"
    RESEARCHER = "researcher"
    WRITER = "writer"
    METHODOLOGIST = "methodologist"
    BUDGET_PLANNER = "budget_planner"
    REVIEWER = "reviewer"
    CITATION_MANAGER = "citation_manager"
    COMPLIANCE_CHECKER = "compliance_checker"


@dataclass
class ProposalDraft:
    """A draft version of a proposal."""

    version: int
    content: Dict[str, str] = field(default_factory=dict)
    sections: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    scores: Dict[str, float] = field(default_factory=dict)
    feedback: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    agent_notes: Dict[str, str] = field(default_factory=dict)


@dataclass
class AgentMessage:
    """Message between agents."""

    from_agent: AgentRole
    to_agent: AgentRole
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    proposal_version: int = 0


@dataclass
class ProposeConfiguration:
    """Configuration for proposal generation."""

    num_drafts: int = 3
    num_iterations: int = 3
    max_rounds_per_agent: int = 10
    refinement_threshold: float = 0.8
    quality_threshold: float = 0.75
    enable_parallel: bool = True
    enable_citation: bool = True
    enable_compliance: bool = True


class ProposalOrchestrator:
    """Orchestrates multi-agent proposal generation with refinement."""

    def __init__(self, config: Optional[ProposeConfiguration] = None):
        self._config = config or ProposeConfiguration()
        self._drafts: List[ProposalDraft] = []
        self._messages: List[AgentMessage] = []
        self._current_version = 0

    async def generate_proposal(
        self,
        topic: str,
        agency: str,
        budget: float,
        progress_callback: Optional[Callable[[float, str], None]] = None,
    ) -> ProposalDraft:
        """
        Generate a proposal with iterative refinement.

        Args:
            topic: Research topic
            agency: Funding agency
            budget: Grant amount
            progress_callback: Optional callback for progress updates

        Returns:
            Final proposal draft
        """
        self._current_version = 0
        self._drafts = []
        self._messages = []

        try:
            # Phase 1: Generate multiple initial drafts
            await self._progress(progress_callback, 0.1, "Generating initial drafts...")
            initial_drafts = await self._generate_initial_drafts(topic, agency, budget)

            # Phase 2: Evaluate and select best draft
            await self._progress(progress_callback, 0.3, "Evaluating drafts...")
            best_draft = self._select_best_draft(initial_drafts)

            # Phase 3: Iterative refinement
            for iteration in range(self._config.num_iterations):
                await self._progress(
                    progress_callback,
                    0.3 + (iteration / self._config.num_iterations) * 0.6,
                    f"Refining proposal (iteration {iteration + 1}/{self._config.num_iterations})...",
                )
                refined_draft = await self._refine_proposal(
                    best_draft, topic, agency, budget
                )

                # Compare and select better version
                if self._compare_drafts(refined_draft, best_draft):
                    best_draft = refined_draft

                # Check if we've met quality threshold
                quality_score = self._calculate_quality_score(best_draft)
                if quality_score >= self._config.quality_threshold:
                    logger.info(
                        "Quality threshold met: %.2f >= %.2f",
                        quality_score,
                        self._config.quality_threshold,
                    )
                    break

            # Phase 4: Final checks
            await self._progress(progress_callback, 0.9, "Running final checks...")
            await self._run_final_checks(best_draft, agency)

            await self._progress(progress_callback, 1.0, "Proposal complete!")
            return best_draft

        except Exception as e:
            logger.error("Proposal generation failed: %s", e, exc_info=True)
            raise RuntimeError(f"Proposal generation failed: {e}") from e

    async def _generate_initial_drafts(
        self, topic: str, agency: str, budget: float
    ) -> List[ProposalDraft]:
        """Generate multiple initial draft proposals."""
        drafts = []

        for i in range(self._config.num_drafts):
            draft = ProposalDraft(version=i + 1)

            # Each draft gets a slightly different angle
            angle = self._get_draft_angle(i, self._config.num_drafts)

            # Generate sections
            draft.sections = await self._generate_sections(topic, agency, budget, angle)
            draft.content = self._merge_sections(draft.sections)
            draft.metadata = {
                "angle": angle,
                "agency": agency,
                "budget": budget,
                "created_by": "initial_generation",
            }

            drafts.append(draft)
            self._drafts.append(draft)

        return drafts

    def _get_draft_angle(self, index: int, total: int) -> str:
        """Get a unique angle for each draft."""
        angles = [
            "innovation-focused",
            "impact-focused",
            "methodology-focused",
            "collaborative-focused",
            "translational-focused",
        ]
        return angles[index % len(angles)]

    async def _generate_sections(
        self, topic: str, agency: str, budget: float, angle: str
    ) -> Dict[str, str]:
        """Generate proposal sections based on agency template."""
        # This would be implemented with actual agent calls
        # For now, return placeholder structure

        sections = {
            "title": await self._generate_title(topic, agency),
            "abstract": await self._generate_abstract(topic, agency, angle),
            "specific_aims": await self._generate_specific_aims(topic, angle),
            "background": await self._generate_background(topic),
            "significance": await self._generate_significance(topic, agency),
            "innovation": await self._generate_innovation(topic, angle),
            "approach": await self._generate_approach(topic, angle),
            "budget_justification": await self._generate_budget_justification(
                budget, agency
            ),
        }

        # Agency-specific sections
        if agency.lower().startswith("nsf"):
            sections["broader_impacts"] = await self._generate_broader_impacts(topic)
            sections["intellectual_merit"] = await self._generate_intellectual_merit(
                topic
            )
            sections["management_plan"] = await self._generate_management_plan(topic)

        elif agency.lower().startswith("nih"):
            sections["research_strategy"] = await self._generate_research_strategy(
                topic
            )
            sections["environment"] = await self._generate_environment(topic)

        return sections

    async def _generate_title(self, topic: str, agency: str) -> str:
        """Generate proposal title."""
        # Would call researcher agent
        return f"Innovative Research on {topic}: {agency.capitalize()} Proposal"

    async def _generate_abstract(self, topic: str, agency: str, angle: str) -> str:
        """Generate abstract."""
        return f"This proposal focuses on {topic} with a {angle} approach..."

    async def _generate_specific_aims(self, topic: str, angle: str) -> str:
        """Generate specific aims."""
        return f"Aim 1: Investigate {topic} fundamentals..."

    async def _generate_background(self, topic: str) -> str:
        """Generate background section."""
        return f"The field of {topic} has seen significant advances..."

    async def _generate_significance(self, topic: str, agency: str) -> str:
        """Generate significance section."""
        return f"This research addresses a critical gap in {topic}..."

    async def _generate_innovation(self, topic: str, angle: str) -> str:
        """Generate innovation section."""
        return f"Our approach to {topic} is novel because..."

    async def _generate_approach(self, topic: str, angle: str) -> str:
        """Generate approach section."""
        return f"We will study {topic} using the following methodology..."

    async def _generate_budget_justification(self, budget: float, agency: str) -> str:
        """Generate budget justification."""
        return f"The requested budget of ${budget:,.0f} is justified for..."

    async def _generate_broader_impacts(self, topic: str) -> str:
        """Generate broader impacts (NSF)."""
        return f"This research will have broad impacts on society through..."

    async def _generate_intellectual_merit(self, topic: str) -> str:
        """Generate intellectual merit (NSF)."""
        return f"The intellectual merit of this work lies in..."

    async def _generate_management_plan(self, topic: str) -> str:
        """Generate management plan (NSF)."""
        return f"The project will be managed with..."

    async def _generate_research_strategy(self, topic: str) -> str:
        """Generate research strategy (NIH)."""
        return f"Our research strategy for {topic} involves..."

    async def _generate_environment(self, topic: str) -> str:
        """Generate environment section (NIH)."""
        return f"The research environment for {topic} includes..."

    def _merge_sections(self, sections: Dict[str, str]) -> str:
        """Merge sections into full proposal text."""
        return "\n\n".join(
            [
                f"## {key.replace('_', ' ').title()}\n\n{value}"
                for key, value in sections.items()
            ]
        )

    def _select_best_draft(self, drafts: List[ProposalDraft]) -> ProposalDraft:
        """Select the best draft based on quality scores."""
        scored_drafts = [
            (draft, self._calculate_quality_score(draft)) for draft in drafts
        ]
        scored_drafts.sort(key=lambda x: x[1], reverse=True)
        best_draft = scored_drafts[0][0]

        logger.info(
            "Selected draft %d with score %.2f", best_draft.version, scored_drafts[0][1]
        )
        return best_draft

    def _calculate_quality_score(self, draft: ProposalDraft) -> float:
        """Calculate overall quality score for a draft."""
        # This would use more sophisticated metrics
        section_scores = []

        for section, text in draft.sections.items():
            if len(text) > 50:
                section_scores.append(0.8)
            else:
                section_scores.append(0.3)

        return sum(section_scores) / len(section_scores) if section_scores else 0.0

    async def _refine_proposal(
        self, draft: ProposalDraft, topic: str, agency: str, budget: float
    ) -> ProposalDraft:
        """Refine a proposal draft through agent collaboration."""
        self._current_version += 1
        refined = ProposalDraft(version=self._current_version)

        refined.content = draft.content.copy()
        refined.sections = draft.sections.copy()
        refined.metadata = draft.metadata.copy()
        refined.metadata["refined_by"] = "iterative_process"

        # Simulate agent refinement
        for section in refined.sections:
            refined.sections[section] = await self._refine_section(
                section, refined.sections[section], topic, agency
            )

        refined.content = self._merge_sections(refined.sections)
        return refined

    async def _refine_section(
        self, section: str, content: str, topic: str, agency: str
    ) -> str:
        """Refine a specific section."""
        # Would call appropriate agent based on section
        return content

    def _compare_drafts(self, draft1: ProposalDraft, draft2: ProposalDraft) -> bool:
        """Compare two drafts and return True if draft1 is better."""
        score1 = self._calculate_quality_score(draft1)
        score2 = self._calculate_quality_score(draft2)

        improvement = score1 - score2
        is_better = improvement > self._config.refinement_threshold

        if is_better:
            logger.info(
                "Draft %d improved: %.2f > %.2f (+%.2f)",
                draft1.version,
                score1,
                score2,
                improvement,
            )

        return is_better

    async def _run_final_checks(self, draft: ProposalDraft, agency: str):
        """Run final compliance and quality checks."""
        # This would integrate with compliance system
        pass

    async def _progress(
        self, callback: Optional[Callable], progress: float, message: str
    ):
        """Call progress callback if provided."""
        if callback:
            await callback(progress, message)

    @property
    def all_messages(self) -> List[AgentMessage]:
        """Get all agent messages."""
        return self._messages.copy()

    @property
    def all_drafts(self) -> List[ProposalDraft]:
        """Get all generated drafts."""
        return self._drafts.copy()
