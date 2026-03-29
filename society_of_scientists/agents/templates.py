"""Proposal template system with agency-specific templates."""

import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)


class TemplateType(str, Enum):
    """Types of proposal templates."""

    NIH_R01 = "nih_r01"
    NIH_R21 = "nih_r21"
    NIH_R03 = "nih_r03"
    NSF_STANDARD = "nsf_standard"
    NSF_CAREER = "nsf_career"
    NSF_EARLY = "nsf_early"
    DOE_STANDARD = "doe_standard"
    DOE_EARLY_CAREER = "doe_early_career"
    PRIVATE_FOUNDATION = "private"
    CUSTOM = "custom"


@dataclass
class ProposalSection:
    """Individual proposal section."""

    name: str
    title: str
    description: str = ""
    required: bool = True
    max_words: Optional[int] = None
    max_pages: Optional[float] = None
    content: str = ""
    guidance: str = ""
    examples: List[str] = field(default_factory=list)


@dataclass
class ProposalTemplate:
    """Complete proposal template."""

    template_id: str
    name: str
    agency: str
    proposal_type: str
    description: str
    sections: List[ProposalSection] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    guidelines_url: str = ""
    page_limit: int = 15
    format_requirements: Dict[str, str] = field(default_factory=dict)


class TemplateRegistry:
    """Registry for proposal templates."""

    _templates: Dict[str, ProposalTemplate] = {}

    @classmethod
    def register(cls, template: ProposalTemplate):
        """Register a template."""
        cls._templates[template.template_id] = template
        logger.info("Registered template: %s", template.template_id)

    @classmethod
    def get(cls, template_id: str) -> Optional[ProposalTemplate]:
        """Get a template by ID."""
        return cls._templates.get(template_id)

    @classmethod
    def list_templates(cls, agency: Optional[str] = None) -> List[ProposalTemplate]:
        """List all templates, optionally filtered by agency."""
        templates = list(cls._templates.values())
        if agency:
            templates = [t for t in templates if t.agency.lower() == agency.lower()]
        return templates

    @classmethod
    def register_default_templates(cls):
        """Register default agency templates."""
        # NIH R01 Template
        nih_r01 = ProposalTemplate(
            template_id=TemplateType.NIH_R01.value,
            name="NIH R01",
            agency="NIH",
            proposal_type="R01 Research Project Grant",
            description="Standard NIH research project grant for discrete, specified, circumscribed projects",
            sections=[
                ProposalSection(
                    name="specific_aims",
                    title="Specific Aims",
                    description="Describe the goals of the proposed research and summarize expected outcomes",
                    required=True,
                    max_pages=1,
                    guidance="Outline specific objectives, research strategy, and expected impact",
                ),
                ProposalSection(
                    name="significance",
                    title="Significance",
                    description="Explain the broader importance and impact of the proposed research",
                    required=True,
                    max_pages=1,
                    guidance="Discuss how the research addresses a critical problem",
                ),
                ProposalSection(
                    name="innovation",
                    title="Innovation",
                    description="Describe the novel aspects of the research",
                    required=True,
                    max_pages=1,
                    guidance="Explain how the research challenges existing paradigms",
                ),
                ProposalSection(
                    name="approach",
                    title="Approach",
                    description="Detail the experimental design and methods",
                    required=True,
                    max_pages=9,
                    guidance="Provide a rigorous statistical analysis plan and alternative approaches",
                ),
                ProposalSection(
                    name="environment",
                    title="Environment",
                    description="Describe the institutional environment and resources",
                    required=True,
                    max_pages=1,
                    guidance="Discuss facilities, equipment, and collaborative opportunities",
                ),
            ],
            metadata={
                "submission_type": "Investigator-Initiated",
                "budget": "Modular budget or detailed budget",
                "duration": "3-5 years",
            },
            page_limit=12,
            format_requirements={
                "font": "Arial, Helvetica, Palatino Linotype, or Georgia",
                "font_size": "11 point",
                "margins": "0.5 inch on all sides",
                "page_limit": "12 pages for Research Strategy",
            },
        )
        cls.register(nih_r01)

        # NSF Standard Template
        nsf_standard = ProposalTemplate(
            template_id=TemplateType.NSF_STANDARD.value,
            name="NSF Standard",
            agency="NSF",
            proposal_type="Standard NSF Grant",
            description="Standard NSF research proposal",
            sections=[
                ProposalSection(
                    name="project_summary",
                    title="Project Summary",
                    description="Overview of the project including broader impacts",
                    required=True,
                    max_pages=1,
                    guidance="Include intellectual merit and broader impacts",
                ),
                ProposalSection(
                    name="references_cited",
                    title="References Cited",
                    description="Bibliographic references",
                    required=True,
                    guidance="Use standard citation format",
                ),
                ProposalSection(
                    name="project_description",
                    title="Project Description",
                    description="Full project description",
                    required=True,
                    max_pages=15,
                    guidance="Include results from prior NSF support if applicable",
                ),
                ProposalSection(
                    name="intellectual_merit",
                    title="Intellectual Merit",
                    description="How the research advances knowledge",
                    required=True,
                    guidance="Describe the potential to transform understanding",
                ),
                ProposalSection(
                    name="broader_impacts",
                    title="Broader Impacts",
                    description="Broader societal benefits",
                    required=True,
                    guidance="Include education, diversity, and societal benefits",
                ),
            ],
            metadata={
                "submission_type": "Investigator-Initiated",
                "budget": "Required",
                "duration": "1-5 years",
            },
            page_limit=15,
            format_requirements={
                "font": "Times New Roman, Courier New, or Arial",
                "font_size": "11 point",
                "margins": "1 inch on all sides",
                "page_limit": "15 pages for Project Description",
            },
        )
        cls.register(nsf_standard)

        # NSF CAREER Template
        nsf_career = ProposalTemplate(
            template_id=TemplateType.NSF_CAREER.value,
            name="NSF CAREER",
            agency="NSF",
            proposal_type="CAREER Award",
            description="NSF Faculty Early Career Development Program",
            sections=[
                ProposalSection(
                    name="project_summary",
                    title="Project Summary",
                    description="Overview with integrated education plan",
                    required=True,
                    max_pages=1,
                    guidance="Clearly integrate research and education",
                ),
                ProposalSection(
                    name="project_description",
                    title="Project Description",
                    description="Research plan",
                    required=True,
                    max_pages=15,
                    guidance="Include results from prior NSF support",
                ),
                ProposalSection(
                    name="integration",
                    title="Integration of Education and Research",
                    description="How education is integrated with research",
                    required=True,
                    guidance="Describe the cohesive education plan",
                ),
                ProposalSection(
                    name="management_plan",
                    title="Management Plan",
                    description="Project management and feasibility",
                    required=True,
                    guidance="Show capability to conduct the proposed work",
                ),
                ProposalSection(
                    name="broader_impacts",
                    title="Broader Impacts",
                    description="Societal benefits",
                    required=True,
                    guidance="Include diversity, outreach, and dissemination",
                ),
            ],
            metadata={
                "submission_type": "Early Career Faculty",
                "budget": "Required (5-year minimum)",
                "duration": "5 years minimum",
                "eligibility": "PhD, tenure-track faculty, within 6 years from PhD",
            },
            page_limit=15,
            format_requirements={
                "font": "Times New Roman, Courier New, or Arial",
                "font_size": "11 point",
                "margins": "1 inch on all sides",
            },
        )
        cls.register(nsf_career)

        # DOE Standard Template
        doe_standard = ProposalTemplate(
            template_id=TemplateType.DOE_STANDARD.value,
            name="DOE Standard",
            agency="DOE",
            proposal_type="Standard DOE Grant",
            description="Department of Energy research proposal",
            sections=[
                ProposalSection(
                    name="cover_page",
                    title="Cover Page",
                    description="Project title, PI information, budget summary",
                    required=True,
                    max_pages=1,
                ),
                ProposalSection(
                    name="project_narrative",
                    title="Project Narrative",
                    description="Technical description of the proposed work",
                    required=True,
                    max_pages=10,
                    guidance="Include scientific merit and innovation",
                ),
                ProposalSection(
                    name="background",
                    title="Background and Significance",
                    description="Literature review and relevance to DOE mission",
                    required=True,
                    max_pages=2,
                ),
                ProposalSection(
                    name="approach",
                    title="Research Approach",
                    description="Methodology and timeline",
                    required=True,
                    max_pages=5,
                    guidance="Include detailed experimental plan",
                ),
                ProposalSection(
                    name="team",
                    title="Research Team and Capabilities",
                    description="PI and team qualifications",
                    required=True,
                    max_pages=2,
                ),
            ],
            metadata={
                "submission_type": "Investigator-Initiated",
                "budget": "Required",
                "duration": "1-5 years",
            },
            page_limit=10,
            format_requirements={
                "font": "Arial or Times New Roman",
                "font_size": "11-12 point",
                "margins": "1 inch on all sides",
            },
        )
        cls.register(doe_standard)


# Initialize default templates
TemplateRegistry.register_default_templates()


class ProposalTemplateBuilder:
    """Builder for creating proposals from templates."""

    def __init__(self, template_id: str):
        self.template = TemplateRegistry.get(template_id)
        if not self.template:
            raise ValueError(f"Template not found: {template_id}")

        self._section_content: Dict[str, str] = {}

    def set_section(self, section_name: str, content: str) -> "ProposalTemplateBuilder":
        """Set content for a section."""
        self._section_content[section_name] = content
        return self

    def get_section(self, section_name: str) -> str:
        """Get content for a section."""
        return self._section_content.get(section_name, "")

    def build(self) -> Dict[str, Any]:
        """Build the complete proposal."""
        sections = {}
        missing_sections = []

        for section in self.template.sections:
            if section.name in self._section_content:
                sections[section.name] = {
                    "title": section.title,
                    "content": self._section_content[section.name],
                    "required": section.required,
                }
            elif section.required:
                missing_sections.append(section.name)

        return {
            "template_id": self.template.template_id,
            "name": self.template.name,
            "agency": self.template.agency,
            "proposal_type": self.template.proposal_type,
            "sections": sections,
            "missing_sections": missing_sections,
            "metadata": self.template.metadata,
            "page_limit": self.template.page_limit,
        }

    def validate(self) -> tuple[bool, List[str]]:
        """Validate the proposal against template requirements."""
        issues = []

        for section in self.template.sections:
            if section.required and section.name not in self._section_content:
                issues.append(f"Missing required section: {section.title}")

            if section.name in self._section_content:
                content = self._section_content[section.name]
                if section.max_words and len(content.split()) > section.max_words:
                    issues.append(
                        f"Section '{section.title}' exceeds {section.max_words} word limit"
                    )

        return len(issues) == 0, issues

    def export_markdown(self) -> str:
        """Export proposal as Markdown."""
        lines = [
            f"# {self.template.name}",
            f"\n{self.template.description}",
            f"\n---",
        ]

        for section in self.template.sections:
            lines.append(f"\n## {section.title}")
            if section.description:
                lines.append(f"\n{section.description}")
            if section.guidance:
                lines.append(f"\n*{section.guidance}*")

            if section.name in self._section_content:
                lines.append(f"\n{self._section_content[section.name]}")
            else:
                lines.append(f"\n*[Content to be added]*")

        return "\n".join(lines)

    def export_latex(self) -> str:
        """Export proposal as LaTeX."""
        lines = [
            f"\\documentclass[12pt]{{article}}",
            f"\\usepackage[margin=1in]{{geometry}}",
            f"\\usepackage{{times}}",
            f"\\title{{{self.template.name}}}",
            f"\\author{{[Your Name]}}",
            f"\\date{{\\today}}",
            f"\\begin{{document}}",
            f"\\maketitle",
            f"\\section{{{self.template.name}}}",
            f"{self.template.description}",
        ]

        for section in self.template.sections:
            lines.append(f"\\subsection{{{section.title}}}")
            if section.description:
                lines.append(f"{section.description}")

            if section.name in self._section_content:
                lines.append(f"{self._section_content[section.name]}")
            else:
                lines.append(f"[Content to be added]")

        lines.append(f"\\end{{document}}")
        return "\n".join(lines)


def get_template_for_agency(
    agency: str, proposal_type: str = None
) -> Optional[ProposalTemplate]:
    """Get a template for a specific agency and proposal type."""
    templates = TemplateRegistry.list_templates(agency=agency)

    if proposal_type:
        proposal_type_lower = proposal_type.lower()
        for template in templates:
            if proposal_type_lower in template.proposal_type.lower():
                return template

    return templates[0] if templates else None


def create_blank_proposal(template_id: str) -> Dict[str, Any]:
    """Create a blank proposal from a template."""
    template = TemplateRegistry.get(template_id)
    if not template:
        raise ValueError(f"Template not found: {template_id}")

    return {
        "template_id": template_id,
        "name": template.name,
        "agency": template.agency,
        "proposal_type": template.proposal_type,
        "sections": {
            section.name: {
                "title": section.title,
                "content": "",
                "required": section.required,
                "guidance": section.guidance,
                "max_words": section.max_words,
                "max_pages": section.max_pages,
            }
            for section in template.sections
        },
        "metadata": template.metadata,
    }


def save_proposal(proposal: Dict[str, Any], filepath: str):
    """Save proposal to JSON file."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        json.dump(proposal, f, indent=2)


def load_proposal(filepath: str) -> Dict[str, Any]:
    """Load proposal from JSON file."""
    with open(filepath, "r") as f:
        return json.load(f)
