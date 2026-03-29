"""Pydantic models for API request/response validation."""

from typing import Optional, Dict, List, Literal, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict


class StartProposalRequest(BaseModel):
    """Request to start a new grant proposal session."""

    grant_topic: str = Field(
        ..., min_length=10, max_length=500, description="Research grant topic"
    )
    funding_agency: Optional[str] = Field(
        None, max_length=200, description="Funding agency name"
    )
    grant_amount: Optional[float] = Field(None, gt=0, description="Grant amount in USD")
    keywords: List[str] = Field(default_factory=list, description="Research keywords")
    model: str = Field(
        default="jamba-large-1.7",
        description="AI model to use",
    )

    @field_validator("grant_topic")
    @classmethod
    def validate_topic(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Grant topic cannot be empty")
        return v

    @field_validator("model")
    @classmethod
    def validate_model(cls, v: str) -> str:
        allowed_models = ["jamba-large-1.7", "jamba-mini-2", "jamba-mini-1.7"]
        if v.lower().replace("-", "") not in [
            m.lower().replace("-", "") for m in allowed_models
        ]:
            raise ValueError(f"Model must be one of: {', '.join(allowed_models)}")
        return v

    @field_validator("keywords")
    @classmethod
    def validate_keywords(cls, v: List[str]) -> List[str]:
        if len(v) > 20:
            raise ValueError("Maximum 20 keywords allowed")
        return [k.strip() for k in v if k.strip()][:20]


class SessionStatusResponse(BaseModel):
    """Response containing session status."""

    session_id: str = Field(..., description="Unique session identifier")
    status: str = Field(..., description="Current session status")
    created_at: str = Field(..., description="Session creation timestamp")
    updated_at: str = Field(..., description="Last update timestamp")
    grant_topic: str = Field(..., description="Original grant topic")
    message: Optional[str] = Field(None, description="Status message or error")
    current_agent: Optional[str] = Field(None, description="Currently executing agent")
    progress: float = Field(0.0, ge=0.0, le=1.0, description="Progress estimate (0-1)")


class ProposalContent(BaseModel):
    """Generated proposal content."""

    sections: Dict[str, str] = Field(
        default_factory=dict, description="Proposal sections"
    )
    full_text: str = Field(..., description="Complete proposal text")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )


class SessionDetailResponse(BaseModel):
    """Detailed session information including generated proposal."""

    session_id: str
    status: str = Field(..., description="Session status")
    created_at: str
    updated_at: str
    grant_topic: str
    funding_agency: Optional[str] = None
    grant_amount: Optional[float] = None
    keywords: List[str] = Field(default_factory=list)
    proposal: Optional[ProposalContent] = None
    message: Optional[str] = None
    current_agent: Optional[str] = None
    progress: float = 0.0


class SessionListItem(BaseModel):
    """Item in session history list."""

    session_id: str
    status: str = Field(..., description="Session status")
    created_at: str
    grant_topic: str
    funding_agency: Optional[str] = None
    grant_amount: Optional[float] = None


class SessionHistoryResponse(BaseModel):
    """Response containing session history."""

    sessions: List[SessionListItem] = Field(default_factory=list)
    total: int = Field(0, description="Total number of sessions")
    offset: int = Field(0, description="Pagination offset")
    limit: int = Field(50, description="Pagination limit")


class ErrorResponse(BaseModel):
    """Standard error response."""

    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    error_type: str = Field("error", description="Type of error")
    timestamp: str = Field(..., description="Error timestamp")


class HealthCheckResponse(BaseModel):
    """Health check response."""

    status: Literal["healthy", "degraded", "unhealthy"] = Field(
        ..., description="Service health status"
    )
    version: str = Field(..., description="API version")
    timestamp: str = Field(..., description="Check timestamp")
    uptime_seconds: float = Field(..., description="Service uptime in seconds")
    active_sessions: int = Field(0, description="Number of active sessions")


class MetricsResponse(BaseModel):
    """Metrics response."""

    total_sessions: int = Field(0, description="Total number of sessions")
    active_sessions: int = Field(0, description="Currently active sessions")
    completed_sessions: int = Field(0, description="Completed sessions")
    failed_sessions: int = Field(0, description="Failed sessions")
    average_completion_time: Optional[float] = Field(
        None, description="Average completion time in seconds"
    )
    total_cost: float = Field(0.0, description="Total API cost in USD")
    total_api_calls: int = Field(0, description="Total number of API calls")
    budget: Dict[str, Any] = Field(default_factory=dict, description="Budget metrics")


class ResearchSource(BaseModel):
    """Research source from Exa search."""

    title: str = Field(..., description="Source title")
    url: str = Field(..., description="Source URL")
    summary: str = Field(..., description="Content summary")
    relevance: float = Field(0.0, ge=0.0, le=1.0, description="Relevance score")
    published_date: Optional[str] = Field(None, description="Publication date")


class ResearchSourcesResponse(BaseModel):
    """Research sources response."""

    sources: List[ResearchSource] = Field(default_factory=list)
    query: str = Field(..., description="Original search query")
    total: int = Field(0, description="Number of sources")
    cached: bool = Field(False, description="Whether results were cached")


class AgentMessage(BaseModel):
    """Message from an agent."""

    agent_name: str = Field(..., description="Name of the sender agent")
    message: str = Field(..., description="Message content")
    timestamp: str = Field(..., description="Message timestamp")


class ConversationHistoryResponse(BaseModel):
    """Conversation history response."""

    messages: List[AgentMessage] = Field(default_factory=list)
    session_id: str = Field(..., description="Session identifier")
    total_messages: int = Field(0)


class ComplianceIssue(BaseModel):
    """Compliance issue found in proposal."""

    severity: Literal["error", "warning", "info"] = Field(
        ..., description="Issue severity"
    )
    category: str = Field(..., description="Issue category")
    message: str = Field(..., description="Issue description")
    section: Optional[str] = Field(None, description="Affected section")
    suggestion: Optional[str] = Field(None, description="Suggested fix")


class ComplianceCheckRequest(BaseModel):
    """Request to check proposal compliance."""

    proposal_text: str = Field(..., description="Full proposal text")
    agency: str = Field(..., description="Funding agency name (e.g., NIH, NSF, DOE)")
    grant_type: Optional[str] = Field(None, description="Grant type (e.g., R01, R21)")
    sections: Dict[str, str] = Field(
        default_factory=dict, description="Proposal sections"
    )


class ComplianceCheckResponse(BaseModel):
    """Compliance check response."""

    compliant: bool = Field(..., description="Whether proposal is compliant")
    score: float = Field(..., ge=0.0, le=100.0, description="Compliance score (0-100)")
    issues: List[ComplianceIssue] = Field(default_factory=list)
    page_limits: Dict[str, Any] = Field(default_factory=dict)
    content_requirements: List[str] = Field(default_factory=list)


class CriterionScore(BaseModel):
    """Score for a single evaluation criterion."""

    criterion: str = Field(..., description="Criterion name")
    score: float = Field(..., ge=0.0, le=10.0, description="Score (0-10)")
    weight: float = Field(1.0, description="Criterion weight")
    comments: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)


class QualityAssessment(BaseModel):
    """Complete quality assessment."""

    overall_score: float = Field(
        ..., ge=0.0, le=10.0, description="Overall score (0-10)"
    )
    criterion_scores: List[CriterionScore] = Field(default_factory=list)
    summary: str = Field(..., description="Assessment summary")
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    estimated_success_rate: float = Field(
        ..., ge=0.0, le=100.0, description="Success percentage"
    )


class QualityAssessRequest(BaseModel):
    """Request to assess proposal quality."""

    proposal_text: str = Field(..., description="Full proposal text")
    agency: str = Field(..., description="Funding agency name")
    sections: Dict[str, str] = Field(
        default_factory=dict, description="Proposal sections"
    )


class TemplateInfo(BaseModel):
    """Template information."""

    id: str = Field(..., description="Template ID")
    name: str = Field(..., description="Template name")
    agency: str = Field(..., description="Funding agency")
    grant_type: str = Field(..., description="Grant type")
    description: str = Field(..., description="Template description")
    sections: List[str] = Field(default_factory=list)
    page_limit: Optional[int] = Field(None, description="Page limit")
    word_limit: Optional[int] = Field(None, description="Word limit")
    file_formats: List[str] = Field(default_factory=list)


class TemplatesResponse(BaseModel):
    """Templates list response."""

    templates: List[TemplateInfo] = Field(default_factory=list)


class TemplateDetailResponse(BaseModel):
    """Detailed template information."""

    template: TemplateInfo
    structure: Dict[str, Any] = Field(default_factory=dict)
    guidelines: List[str] = Field(default_factory=list)
    tips: List[str] = Field(default_factory=list)


class ExportRequest(BaseModel):
    """Request to export proposal."""

    session_id: str = Field(..., description="Session ID")
    format: Literal["pdf", "docx", "latex", "markdown"] = Field(
        ..., description="Export format"
    )
    template_id: Optional[str] = Field(None, description="Template ID to use")


class ExportResponse(BaseModel):
    """Export response."""

    format: str = Field(..., description="Format used")
    download_url: str = Field(..., description="Download URL")
    filename: str = Field(..., description="Generated filename")
    file_size: int = Field(..., description="File size in bytes")
    expires_at: str = Field(..., description="Expiration timestamp")
