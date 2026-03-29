"""Quality assessment and scoring system for grant proposals."""

import re
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class Criterion(str, Enum):
    """Evaluation criteria."""

    SIGNIFICANCE = "significance"
    INNOVATION = "innovation"
    APPROACH = "approach"
    ENVIRONMENT = "environment"
    INVESTIGATOR = "investigator"
    BUDGET = "budget"
    COMPLIANCE = "compliance"
    CLARITY = "clarity"
    COMPLETENESS = "completeness"
    IMPACT = "impact"


@dataclass
class CriterionScore:
    """Score for a single criterion."""

    criterion: Criterion
    score: float  # 0-10
    weight: float = 1.0
    comments: List[str] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


@dataclass
class QualityAssessment:
    """Complete quality assessment."""

    overall_score: float = 0.0
    criterion_scores: List[CriterionScore] = field(default_factory=list)
    summary: str = ""
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    estimated_success_rate: float = 0.0


class ProposalEvaluator:
    """Evaluate grant proposal quality."""

    # Criterion weights for NIH-style review
    NIH_WEIGHTS = {
        Criterion.SIGNIFICANCE: 0.3,
        Criterion.INNOVATION: 0.3,
        Criterion.APPROACH: 0.25,
        Criterion.INVESTIGATOR: 0.1,
        Criterion.ENVIRONMENT: 0.05,
    }

    # Criterion weights for NSF-style review
    NSF_WEIGHTS = {
        Criterion.INTELLECTUAL_MERIT: 0.5,
        Criterion.BROADER_IMPACTS: 0.5,
    }

    def __init__(self, agency: str = "nih"):
        self.agency = agency.lower()
        self._weights = self._get_weights()

    def _get_weights(self) -> Dict[Criterion, float]:
        """Get criterion weights based on agency."""
        if self.agency.startswith("nsf"):
            return self.NSF_WEIGHTS
        return self.NIH_WEIGHTS

    def evaluate(self, proposal: Dict[str, Any]) -> QualityAssessment:
        """
        Evaluate proposal quality.

        Args:
            proposal: Proposal dictionary with sections

        Returns:
            Quality assessment with scores
        """
        assessment = QualityAssessment()

        # Evaluate each criterion
        for criterion, weight in self._weights.items():
            score = self._evaluate_criterion(criterion, proposal)
            assessment.criterion_scores.append(score)

        # Calculate overall score
        assessment.overall_score = self._calculate_overall_score(
            assessment.criterion_scores
        )

        # Generate summary and recommendations
        assessment.summary = self._generate_summary(assessment)
        assessment.strengths, assessment.weaknesses = (
            self._extract_strengths_weaknesses(assessment.criterion_scores)
        )
        assessment.recommendations = self._generate_recommendations(
            assessment.criterion_scores
        )
        assessment.estimated_success_rate = self._estimate_success_rate(
            assessment.overall_score
        )

        return assessment

    def _evaluate_criterion(
        self, criterion: Criterion, proposal: Dict[str, Any]
    ) -> CriterionScore:
        """Evaluate a single criterion."""
        score_obj = CriterionScore(criterion=criterion, score=0.0)

        if criterion == Criterion.SIGNIFICANCE:
            self._evaluate_significance(proposal, score_obj)
        elif criterion == Criterion.INNOVATION:
            self._evaluate_innovation(proposal, score_obj)
        elif criterion == Criterion.APPROACH:
            self._evaluate_approach(proposal, score_obj)
        elif criterion == Criterion.INVESTIGATOR:
            self._evaluate_investigator(proposal, score_obj)
        elif criterion == Criterion.ENVIRONMENT:
            self._evaluate_environment(proposal, score_obj)
        elif criterion == Criterion.COMPLIANCE:
            self._evaluate_compliance(proposal, score_obj)
        elif criterion == Criterion.CLARITY:
            self._evaluate_clarity(proposal, score_obj)
        elif criterion == Criterion.COMPLETENESS:
            self._evaluate_completeness(proposal, score_obj)

        return score_obj

    def _evaluate_significance(self, proposal: Dict[str, Any], score: CriterionScore):
        """Evaluate Significance criterion."""
        significance_text = self._get_section_text(proposal, "significance")

        if not significance_text:
            score.score = 2.0
            score.weaknesses.append("Significance section is missing or empty")
            score.suggestions.append("Add a strong significance section")
            return

        # Check for key elements
        score.score = 5.0

        # Problem statement
        if re.search(
            r"(problem|gap|challenge|need|critical)", significance_text, re.IGNORECASE
        ):
            score.score += 1.0
            score.strengths.append("Clear articulation of the problem")
        else:
            score.weaknesses.append("Problem statement unclear")

        # Impact
        if re.search(
            r"(impact|benefit|improve|advance|advance)",
            significance_text,
            re.IGNORECASE,
        ):
            score.score += 1.0
            score.strengths.append("Potential impact described")
        else:
            score.suggestions.append("Add more detail about potential impact")

        # Public health relevance (for NIH)
        if self.agency.startswith("nih"):
            if re.search(
                r"(public health|patient|clinical|health|disease)",
                significance_text,
                re.IGNORECASE,
            ):
                score.score += 1.0
                score.strengths.append("Public health relevance clear")

        # Length and depth
        word_count = len(significance_text.split())
        if word_count > 200:
            score.score += 0.5
        else:
            score.suggestions.append("Expand significance section with more detail")

        score.score = min(score.score, 10.0)

    def _evaluate_innovation(self, proposal: Dict[str, Any], score: CriterionScore):
        """Evaluate Innovation criterion."""
        innovation_text = self._get_section_text(proposal, "innovation")

        if not innovation_text:
            score.score = 2.0
            score.weaknesses.append("Innovation section is missing or empty")
            score.suggestions.append("Add an innovation section")
            return

        score.score = 5.0

        # Novelty indicators
        novelty_words = [
            "novel",
            "new",
            "unique",
            "original",
            "first",
            "innovative",
            "pioneer",
        ]
        novelty_count = sum(
            1 for word in novelty_words if word in innovation_text.lower()
        )

        if novelty_count >= 2:
            score.score += 1.5
            score.strengths.append("Emphasizes novelty and innovation")
        elif novelty_count == 1:
            score.score += 0.5
        else:
            score.weaknesses.append("Limited discussion of novelty")
            score.suggestions.append("Emphasize the novel aspects of the work")

        # Paradigm shifting
        if re.search(
            r"(paradigm|challenge.*existing|advance.*field|transformative)",
            innovation_text,
            re.IGNORECASE,
        ):
            score.score += 1.0
            score.strengths.append("Potential to advance the field")

        # Technical innovation
        if re.search(
            r"(technol|method|approach|technique|platform)",
            innovation_text,
            re.IGNORECASE,
        ):
            score.score += 0.5

        score.score = min(score.score, 10.0)

    def _evaluate_approach(self, proposal: Dict[str, Any], score: CriterionScore):
        """Evaluate Approach criterion."""
        approach_text = self._get_section_text(proposal, "approach")

        if not approach_text:
            score.score = 2.0
            score.weaknesses.append("Approach section is missing or empty")
            score.suggestions.append("Add a detailed approach section")
            return

        score.score = 5.0

        # Experimental design
        if re.search(
            r"(design|experiment|method|methodology|protocol)",
            approach_text,
            re.IGNORECASE,
        ):
            score.score += 1.0
            score.strengths.append("Experimental design described")

        # Data analysis
        if re.search(
            r"(analysis|statistical|data|quantit|measure)", approach_text, re.IGNORECASE
        ):
            score.score += 1.0
            score.strengths.append("Data analysis plan present")

        # Alternative approaches
        if re.search(
            r"(alternative|back.*up|contingency|fallback)", approach_text, re.IGNORECASE
        ):
            score.score += 1.0
            score.strengths.append("Alternative approaches considered")

        # Feasibility
        if re.search(
            r"(feasible|feasibility|practical|achievable|realistic)",
            approach_text,
            re.IGNORECASE,
        ):
            score.score += 0.5

        # Timeline
        if re.search(
            r"(timeline|month|year|schedule|milestone)", approach_text, re.IGNORECASE
        ):
            score.score += 0.5

        # Length and detail
        word_count = len(approach_text.split())
        if word_count > 500:
            score.score += 0.5
        else:
            score.suggestions.append("Add more detail to experimental approach")

        score.score = min(score.score, 10.0)

    def _evaluate_investigator(self, proposal: Dict[str, Any], score: CriterionScore):
        """Evaluate Investigator criterion."""
        investigator_text = self._get_section_text(proposal, "investigator") or ""

        score.score = 5.0

        # Check for CV/biosketch
        if (
            "cv" in proposal
            or "biosketch" in proposal
            or "cv" in investigator_text.lower()
        ):
            score.score += 1.0
            score.strengths.append("Biosketch/CV included")

        # Experience
        if re.search(
            r"(experience|expert|publicat|previous|track record)",
            investigator_text,
            re.IGNORECASE,
        ):
            score.score += 1.0
            score.strengths.append("Investigator experience highlighted")

        # Publications
        if re.search(
            r"(publication|peer.review|journal|paper)", investigator_text, re.IGNORECASE
        ):
            score.score += 1.0
            score.strengths.append("Track record in publications")

        # Collaboration
        if re.search(
            r"(collaborat|team|multi.disciplinary|consortium)",
            investigator_text,
            re.IGNORECASE,
        ):
            score.score += 0.5

        score.score = min(score.score, 10.0)

    def _evaluate_environment(self, proposal: Dict[str, Any], score: CriterionScore):
        """Evaluate Environment criterion."""
        environment_text = self._get_section_text(proposal, "environment") or ""

        if not environment_text:
            score.score = 3.0
            score.suggestions.append("Consider adding environment section")
            return

        score.score = 5.0

        # Facilities
        if re.search(
            r"(facility|laborat|equipment|resources)", environment_text, re.IGNORECASE
        ):
            score.score += 1.5
            score.strengths.append("Facilities and resources described")

        # Institutional support
        if re.search(
            r"(institution|support|commitment|collabor)",
            environment_text,
            re.IGNORECASE,
        ):
            score.score += 1.0
            score.strengths.append("Institutional support evident")

        # Collaborative environment
        if re.search(
            r"(collaborative|team|interdisciplinary)", environment_text, re.IGNORECASE
        ):
            score.score += 0.5

        score.score = min(score.score, 10.0)

    def _evaluate_compliance(self, proposal: Dict[str, Any], score: CriterionScore):
        """Evaluate Overall Compliance."""
        score.score = 5.0

        # Check if compliance score is provided
        compliance_score = proposal.get("compliance_score", 0)
        if compliance_score:
            score.score = compliance_score / 10.0
            if score.score >= 0.8:
                score.strengths.append("Excellent compliance")
            elif score.score >= 0.6:
                score.strengths.append("Good compliance")
            else:
                score.weaknesses.append("Compliance issues need attention")

        return

    def _evaluate_clarity(self, proposal: Dict[str, Any], score: CriterionScore):
        """Evaluate Clarity of writing."""
        all_text = " ".join(proposal.get("sections", {}).values())

        score.score = 5.0

        # Check for clear structure
        if re.search(
            r"(###?|\\section|clear|first|next|then)", all_text, re.IGNORECASE
        ):
            score.score += 1.0
            score.strengths.append("Clear structure and organization")

        # Length
        word_count = len(all_text.split())
        if 500 < word_count < 5000:
            score.score += 1.5
            score.strengths.append("Appropriate length")
        elif word_count < 500:
            score.suggestions.append("Expand content for better clarity")
        elif word_count > 10000:
            score.suggestions.append("Consider condensing for better readability")

        # Sentence length (simple heuristic)
        sentences = re.split(r"[.!?]", all_text)
        avg_length = (
            sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
        )

        if 10 <= avg_length <= 25:
            score.score += 1.0
            score.strengths.append("Good sentence structure")
        elif avg_length > 30:
            score.suggestions.append("Consider breaking up long sentences for clarity")

        score.score = min(score.score, 10.0)

    def _evaluate_completeness(self, proposal: Dict[str, Any], score: CriterionScore):
        """Evaluate Completeness of required sections."""
        required_sections = [
            "title",
            "abstract",
            "specific_aims",
            "background",
            "approach",
        ]

        score.score = 5.0

        present = []
        missing = []

        sections = proposal.get("sections", {})
        for section in required_sections:
            if section in sections and sections[section]:
                present.append(section)
            else:
                missing.append(section)

        completion_rate = len(present) / len(required_sections)

        score.score = 5.0 + completion_rate * 5.0

        if completion_rate >= 0.9:
            score.strengths.append("All required sections present")
        elif completion_rate >= 0.7:
            score.strengths.append("Most required sections present")
            score.weaknesses.extend([f"Missing section: {s}" for s in missing])
        else:
            score.weaknesses.append("Many required sections missing")
            score.suggestions.extend([f"Add section: {s}" for s in missing])

        score.score = min(score.score, 10.0)

    def _get_section_text(self, proposal: Dict[str, Any], section_name: str) -> str:
        """Get text for a section."""
        sections = proposal.get("sections", {})
        # Try exact match first
        if section_name in sections:
            return sections[section_name]

        # Try partial match
        for key, value in sections.items():
            if section_name in key.lower():
                return value

        return ""

    def _calculate_overall_score(self, criterion_scores: List[CriterionScore]) -> float:
        """Calculate weighted overall score."""
        total = 0.0
        total_weight = 0.0

        for score_obj in criterion_scores:
            weight = self._weights.get(score_obj.criterion, 1.0)
            total += score_obj.score * weight
            total_weight += weight

        if total_weight == 0:
            return 0.0

        overall = total / total_weight
        return round(overall, 1)

    def _generate_summary(self, assessment: QualityAssessment) -> str:
        """Generate assessment summary."""
        score = assessment.overall_score

        if score >= 9.0:
            return "Exceptional proposal with significant strengths and minor weaknesses. Highly competitive."
        elif score >= 7.5:
            return "Strong proposal with good strengths and some areas for improvement. Competitive."
        elif score >= 6.0:
            return "Satisfactory proposal with adequate strengths and several areas needing improvement. Moderately competitive."
        elif score >= 4.5:
            return "Marginal proposal with limited strengths and multiple weaknesses. May need significant revision."
        else:
            return "Unsatisfactory proposal with significant weaknesses and limited strengths. Major revision required."

    def _extract_strengths_weaknesses(
        self, criterion_scores: List[CriterionScore]
    ) -> tuple[List[str], List[str]]:
        """Extract overall strengths and weaknesses."""
        strengths = []
        weaknesses = []

        for score_obj in criterion_scores:
            if score_obj.score >= 7.0:
                strengths.extend(score_obj.strengths)
            elif score_obj.score < 5.0:
                weaknesses.extend(score_obj.weaknesses)

        return strengths[:5], weaknesses[:5]

    def _generate_recommendations(
        self, criterion_scores: List[CriterionScore]
    ) -> List[str]:
        """Generate overall recommendations."""
        recommendations = []

        for score_obj in criterion_scores:
            if score_obj.score < 6.0:
                recommendations.extend(score_obj.suggestions[:2])

        return recommendations[:8]

    def _estimate_success_rate(self, overall_score: float) -> float:
        """Estimate funding success probability based on score."""
        # This is a rough heuristic based on typical NIH/NSF scoring
        if overall_score >= 9.0:
            return 0.5
        elif overall_score >= 8.0:
            return 0.35
        elif overall_score >= 7.0:
            return 0.20
        elif overall_score >= 6.0:
            return 0.10
        else:
            return 0.05

    def get_score_breakdown(self, assessment: QualityAssessment) -> Dict[str, Any]:
        """Get a detailed score breakdown."""
        return {
            "overall_score": assessment.overall_score,
            "success_rate": assessment.estimated_success_rate,
            "summary": assessment.summary,
            "criterion_scores": [
                {
                    "criterion": score_obj.criterion.value,
                    "score": score_obj.score,
                    "weight": self._weights.get(score_obj.criterion, 1.0),
                    "strengths": score_obj.strengths,
                    "weaknesses": score_obj.weaknesses,
                    "suggestions": score_obj.suggestions,
                }
                for score_obj in assessment.criterion_scores
            ],
        }


def quick_score(proposal: Dict[str, Any], agency: str = "nih") -> Dict[str, Any]:
    """
    Quick scoring function for proposals.

    Args:
        proposal: Proposal dictionary
        agency: Funding agency

    Returns:
        Score breakdown
    """
    evaluator = ProposalEvaluator(agency)
    assessment = evaluator.evaluate(proposal)
    return evaluator.get_score_breakdown(assessment)
