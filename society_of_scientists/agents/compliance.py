"""Grant compliance system with agency-specific rules and validation."""

import re
import logging
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class Agency(str, Enum):
    """Funding agencies."""

    NIH = "nih"
    NSF = "nsf"
    DOE = "doe"
    DOD = "dod"
    NASA = "nasa"
    AFOSR = "afosr"
    ARL = "arl"
    PRIVATE_FOUNDATION = "private"


class ComplianceStatus(str, Enum):
    """Compliance check status."""

    PASS = "pass"
    WARNING = "warning"
    FAIL = "fail"
    SKIP = "skip"


@dataclass
class ComplianceRule:
    """Individual compliance rule."""

    rule_id: str
    category: str
    description: str
    severity: str = field(default="warning")  # error, warning, info
    check_fn: Optional[Callable[[Dict[str, Any]], bool]] = None
    suggestion: Optional[str] = None


@dataclass
class ComplianceIssue:
    """Compliance issue found."""

    rule_id: str
    category: str
    section: str
    issue: str
    severity: ComplianceStatus
    suggestion: str
    line_number: Optional[int] = None


@dataclass
class ComplianceReport:
    """Full compliance report."""

    agency: Agency
    proposal_type: str
    total_rules: int = 0
    passed: int = 0
    warnings: int = 0
    failed: int = 0
    skipped: int = 0
    issues: List[ComplianceIssue] = field(default_factory=list)
    overall_status: ComplianceStatus = ComplianceStatus.PASS
    score: float = 0.0


# ============================================================================
# NIH Compliance Rules
# ============================================================================


class NIHComplianceRules:
    """NIH-specific compliance rules."""

    @staticmethod
    def get_rules() -> List[ComplianceRule]:
        """Get all NIH compliance rules."""
        return [
            ComplianceRule(
                rule_id="nih_abstract_word_count",
                category="Content",
                description="Abstract ≤ 30 lines (≤ ~300 words)",
                severity="error",
                check_fn=lambda d: NIHComplianceRules._check_abstract_length(d),
                suggestion="Condense abstract to 30 lines or fewer.",
            ),
            ComplianceRule(
                rule_id="nih_specific_aims_one_page",
                category="Content",
                description="Specific Aims limited to 1 page",
                severity="error",
                check_fn=lambda d: NIHComplianceRules._check_specific_aims_length(d),
                suggestion="Condense Specific Aims to fit in 1 page.",
            ),
            ComplianceRule(
                rule_id="nih_research_strategy_12_pages",
                category="Content",
                description="Research Strategy ≤ 12 pages (if R01)",
                severity="error",
                check_fn=lambda d: NIHComplianceRules._check_research_strategy_length(
                    d
                ),
                suggestion="Reduce Research Strategy to 12 pages or fewer.",
            ),
            ComplianceRule(
                rule_id="nih_biosketch_present",
                category="Required",
                description="Biographical Sketch present for all investigators",
                severity="error",
                check_fn=lambda d: d.get("biosketches", "") != "",
                suggestion="Add Biographical Sketch for each investigator.",
            ),
            ComplianceRule(
                rule_id="nih_hipaa_compliance",
                category="Compliance",
                description="HIPAA compliance information",
                severity="warning",
                check_fn=lambda d: "HIPAA" in d.get("compliance_sections", ""),
                suggestion="Include HIPAA compliance information if relevant.",
            ),
            ComplianceRule(
                rule_id="nih_human_subjects",
                category="Compliance",
                description="Human subjects section",
                severity="warning",
                check_fn=lambda d: "human subjects"
                in d.get("compliance_sections", "").lower(),
                suggestion="Ensure human subjects section is included if applicable.",
            ),
            ComplianceRule(
                rule_id="nih_responsible_conduct",
                category="Training",
                description="Responsible Conduct of Research (RCR) described",
                severity="info",
                check_fn=lambda d: "responsible conduct"
                in d.get("training", "").lower()
                or "RCR" in d.get("training", ""),
                suggestion="Consider including RCR training information.",
            ),
        ]

    @staticmethod
    def _check_abstract_length(data: Dict[str, Any]) -> bool:
        """Check abstract length (≤ 30 lines)."""
        abstract = data.get("abstract", "")
        lines = abstract.split("\n")
        return len(lines) <= 30

    @staticmethod
    def _check_specific_aims_length(data: Dict[str, Any]) -> bool:
        """Check Specific Aims length (≤ 1 page)."""
        aims = data.get("specific_aims", "")
        # Approximate: 1 page ≈ 2500 characters
        return len(aims) <= 2500

    @staticmethod
    def _check_research_strategy_length(data: Dict[str, Any]) -> bool:
        """Check Research Strategy length (≤ 12 pages ≈ 30000 characters)."""
        strategy = data.get("research_strategy", "")
        return len(strategy) <= 30000


# ============================================================================
# NSF Compliance Rules
# ============================================================================


class NSFComplianceRules:
    """NSF-specific compliance rules."""

    @staticmethod
    def get_rules() -> List[ComplianceRule]:
        """Get all NSF compliance rules."""
        return [
            ComplianceRule(
                rule_id="nsf_project_summary_one_page",
                category="Content",
                description="Project Summary limited to 1 page (≤ 250 words for overview)",
                severity="error",
                check_fn=lambda d: NSFComplianceRules._check_project_summary(d),
                suggestion="Condense Project Summary to 1 page or fewer.",
            ),
            ComplianceRule(
                rule_id="nsf_career_proposal_length",
                category="Content",
                description="CAREER proposal ≤ 15 pages (excluding references, biosketches)",
                severity="error",
                check_fn=lambda d: NSFComplianceRules._check_career_length(d),
                suggestion="Reduce proposal text to 15 pages or fewer.",
            ),
            ComplianceRule(
                rule_id="nsf_broader_impacts",
                category="Content",
                description="Broader Impacts section present",
                severity="error",
                check_fn=lambda d: len(d.get("broader_impacts", "").strip()) > 100,
                suggestion="Add or expand Broader Impacts section.",
            ),
            ComplianceRule(
                rule_id="nsf_intellectual_merit",
                category="Content",
                description="Intellectual Merit section present",
                severity="error",
                check_fn=lambda d: len(d.get("intellectual_merit", "").strip()) > 100,
                suggestion="Add or expand Intellectual Merit section.",
            ),
            ComplianceRule(
                rule_id="nsf_mgmt_plan",
                category="Required",
                description="Management Plan present for CAREER proposals",
                severity="warning",
                check_fn=lambda d: len(d.get("management_plan", "").strip()) > 50,
                suggestion="Include management plan for CAREER proposals.",
            ),
            ComplianceRule(
                rule_id="nsf_evaluation_plan",
                category="Required",
                description="Evaluation Plan present",
                severity="warning",
                check_fn=lambda d: len(d.get("evaluation_plan", "").strip()) > 50,
                suggestion="Include evaluation plan.",
            ),
            ComplianceRule(
                rule_id="nsf_gender_compliance",
                category="Compliance",
                description="Gender/Sex equity addressed",
                severity="info",
                check_fn=lambda d: "gender" in d.get("compliance_sections", "").lower()
                or "sex" in d.get("compliance_sections", "").lower(),
                suggestion="Consider addressing gender/sex in research design.",
            ),
        ]

    @staticmethod
    def _check_project_summary(data: Dict[str, Any]) -> bool:
        """Check Project Summary length."""
        summary = data.get("project_summary", "")
        # ≤ 1 page ≈ 2500 characters
        return len(summary) <= 2500

    @staticmethod
    def _check_career_length(data: Dict[str, Any]) -> bool:
        """Check CAREER proposal length."""
        body = data.get("project_description", "")
        # 15 pages ≈ 37500 characters
        return len(body) <= 37500


# ============================================================================
# DOE Compliance Rules
# ============================================================================


class DOEComplianceRules:
    """DOE-specific compliance rules."""

    @staticmethod
    def get_rules() -> List[ComplianceRule]:
        """Get all DOE compliance rules."""
        return [
            ComplianceRule(
                rule_id="doe_project_narrative",
                category="Content",
                description="Project Narrative ≤ 10 pages",
                severity="error",
                check_fn=lambda d: len(d.get("project_narrative", "")) <= 25000,
                suggestion="Condense Project Narrative to 10 pages.",
            ),
            ComplianceRule(
                rule_id="doe_alignment",
                category="Content",
                description="DOE program alignment addressed",
                severity="warning",
                check_fn=lambda d: "energy" in d.get("alignment", "").lower()
                or "DOE" in d.get("alignment", ""),
                suggestion="Ensure proposal aligns with DOE mission.",
            ),
            ComplianceRule(
                rule_id="doe_safety",
                category="Safety",
                description="Safety plan described",
                severity="warning",
                check_fn=lambda d: len(d.get("safety_plan", "").strip()) > 50,
                suggestion="Include safety plan.",
            ),
            ComplianceRule(
                rule_id="doe_technology_readiness",
                category="Content",
                description="Technology Readiness Level (TRL) discussed",
                severity="info",
                check_fn=lambda d: "TRL" in d.get("technical_development", "")
                or "technology readiness" in d.get("technical_development", "").lower(),
                suggestion="Consider including TRL information.",
            ),
        ]


# ============================================================================
# Main Compliance Checker
# ============================================================================


class ComplianceChecker:
    """Check proposals against agency-specific compliance rules."""

    # Rule set registry
    _rule_sets = {
        Agency.NIH: NIHComplianceRules.get_rules,
        Agency.NSF: NSFComplianceRules.get_rules,
        Agency.DOE: DOEComplianceRules.get_rules,
    }

    @classmethod
    def check_compliance(
        cls,
        agency: Agency,
        proposal_data: Dict[str, Any],
        proposal_type: str = "standard",
    ) -> ComplianceReport:
        """
        Check proposal compliance against agency rules.

        Args:
            agency: Funding agency
            proposal_data: Proposal sections and metadata
            proposal_type: Type of proposal (standard, CAREER, etc.)

        Returns:
            ComplianceReport with issues and status
        """
        report = ComplianceReport(agency=agency, proposal_type=proposal_type)

        # Get rules for this agency
        rules_getter = cls._rule_sets.get(agency)
        if not rules_getter:
            logger.warning("No compliance rules defined for agency: %s", agency)
            return report

        rules = rules_getter()

        # Apply each rule
        for rule in rules:
            report.total_rules += 1

            try:
                # Check if rule applies based on proposal type
                if hasattr(rule, "check_fn") and rule.check_fn:
                    passed = rule.check_fn(proposal_data)
                else:
                    # Skip if no check function
                    report.skipped += 1
                    continue

                if passed:
                    report.passed += 1
                else:
                    if rule.severity == "error":
                        report.failed += 1
                        status = ComplianceStatus.FAIL
                    elif rule.severity == "warning":
                        report.warnings += 1
                        status = ComplianceStatus.WARNING
                    else:
                        report.warnings += 1
                        status = ComplianceStatus.WARNING

                    # Create issue
                    issue = ComplianceIssue(
                        rule_id=rule.rule_id,
                        category=rule.category,
                        section=rule.rule_id.split("_")[1]
                        if "_" in rule.rule_id
                        else "general",
                        issue=rule.description,
                        severity=status,
                        suggestion=rule.suggestion or "Please review.",
                    )
                    report.issues.append(issue)

            except Exception as e:
                logger.error("Error checking rule %s: %s", rule.rule_id, e)
                report.failed += 1
                issue = ComplianceIssue(
                    rule_id=rule.rule_id,
                    category=rule.category,
                    section="general",
                    issue=f"Rule check failed: {str(e)}",
                    severity=ComplianceStatus.FAIL,
                    suggestion="Contact support for assistance.",
                )
                report.issues.append(issue)

        # Determine overall status
        cls._calculate_status(report)

        return report

    @classmethod
    def _calculate_status(cls, report: ComplianceReport):
        """Calculate overall compliance status and score."""
        if report.failed > 0:
            report.overall_status = ComplianceStatus.FAIL
            report.score = max(0, 50 - report.failed * 10)
        elif report.warnings > 0:
            report.overall_status = ComplianceStatus.WARNING
            report.score = 70 + (30 * (1 - min(report.warnings / 10, 1)))
        else:
            report.overall_status = ComplianceStatus.PASS
            report.score = 100.0

        report.score = round(report.score, 1)

    @classmethod
    def get_agency_requirements(cls, agency: Agency) -> Dict[str, Any]:
        """
        Get agency-specific requirements and guidelines.

        Args:
            agency: Funding agency

        Returns:
            Dictionary of requirements
        """
        requirements = {
            Agency.NIH: {
                "name": "National Institutes of Health",
                "page_limit": {
                    "R01": "Research Strategy: 12 pages",
                    "R21": "Research Strategy: 6 pages",
                },
                "required_sections": [
                    "Specific Aims",
                    "Research Strategy",
                    "Biographical Sketch",
                ],
                "format": "PDF with specific fonts and margins",
                "reference_limit": "No limit, but should be reasonable",
                "biosketch_format": "NIH biosketch format",
            },
            Agency.NSF: {
                "name": "National Science Foundation",
                "page_limit": {
                    "Standard": "Project Description: 15 pages",
                    "CAREER": "Project Description: 15 pages",
                },
                "required_sections": [
                    "Project Summary",
                    "Project Description",
                    "Broader Impacts",
                    "Intellectual Merit",
                ],
                "format": "PDF with standard margins",
                "reference_limit": "References: No limit for most programs",
                "biosketch_format": "NSF biosketch format",
            },
            Agency.DOE: {
                "name": "Department of Energy",
                "page_limit": {
                    "Standard": "Project Narrative: 10 pages",
                    "Early Career": "Research Plan: 10 pages",
                },
                "required_sections": [
                    "Project Narrative",
                    "Budget Justification",
                    "Management Plan",
                ],
                "format": "PDF",
                "reference_limit": "References included in page limit",
                "biosketch_format": "CV format",
            },
        }

        return requirements.get(agency, {})

    @classmethod
    def suggest_improvements(cls, report: ComplianceReport) -> List[Dict[str, str]]:
        """
        Suggest improvements based on compliance issues.

        Args:
            report: Compliance report

        Returns:
            List of suggestions
        """
        suggestions = []

        for issue in report.issues:
            suggestion = {
                "rule_id": issue.rule_id,
                "category": issue.category,
                "severity": issue.severity.value,
                "issue": issue.issue,
                "suggestion": issue.suggestion,
            }
            suggestions.append(suggestion)

        return suggestions

    @classmethod
    def create_checklist(cls, agency: Agency) -> List[str]:
        """
        Create a compliance checklist for proposal preparation.

        Args:
            agency: Funding agency

        Returns:
            List of checklist items
        """
        rules_getter = cls._rule_sets.get(agency)
        if not rules_getter:
            return []

        rules = rules_getter()
        return [f"☐ {rule.description}" for rule in rules]


def check_proposal_compliance(
    proposal_text: str,
    agency: str = "nih",
    proposal_sections: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    Quick compliance check for a proposal.

    Args:
        proposal_text: Full proposal text
        agency: Agency name
        proposal_sections: Optional dictionary of sections

    Returns:
        Compliance report
    """
    try:
        agency_enum = Agency(agency.lower())
    except ValueError:
        agency_enum = Agency.NIH

    # If sections not provided, try to extract from text
    if proposal_sections is None:
        proposal_sections = _extract_sections(proposal_text)

    checker = ComplianceChecker()
    report = checker.check_compliance(agency_enum, proposal_sections)

    return {
        "agency": agency,
        "overall_status": report.overall_status.value,
        "score": report.score,
        "passed": report.passed,
        "warnings": report.warnings,
        "failed": report.failed,
        "issues": [
            {
                "rule_id": issue.rule_id,
                "category": issue.category,
                "section": issue.section,
                "issue": issue.issue,
                "severity": issue.severity.value,
                "suggestion": issue.suggestion,
            }
            for issue in report.issues
        ],
    }


def _extract_sections(text: str) -> Dict[str, str]:
    """Extract sections from proposal text."""
    sections = {}

    # Common section headers
    patterns = [
        (r"##?\s*(?:Specific\s+Aims)(?:\n|$)", "specific_aims"),
        (r"##?\s*(?:Abstract)(?:\n|$)", "abstract"),
        (r"##?\s*(?:Background|Significance)(?:\n|$)", "background"),
        (r"##?\s*(?:Project\s+Summary)(?:\n|$)", "project_summary"),
        (r"##?\s*(?:Broader\s+Impacts)(?:\n|$)", "broader_impacts"),
        (r"##?\s*(?:Intellectual\s+Merit)(?:\n|$)", "intellectual_merit"),
        (r"##?\s*(?:Project\s+Description)(?:\n|$)", "project_description"),
    ]

    for pattern, key in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            start = match.end()
            # Find next section or end
            next_match = re.search(r"##?\s*\w+", text[start:])
            end = start + next_match.start() if next_match else len(text)
            sections[key] = text[start:end].strip()

    return sections
