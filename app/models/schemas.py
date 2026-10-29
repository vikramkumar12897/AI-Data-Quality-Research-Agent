from __future__ import annotations
from typing import List
from pydantic import BaseModel, Field

class ResearchSource(BaseModel):
    title: str
    url: str

class ResearchFinding(BaseModel):
    finding_id: str
    normalized_value: str
    interpretation: str
    confidence: float = Field(ge=0, le=1)
    sources: List[ResearchSource] = []

class VerificationResult(BaseModel):
    accepted_finding_ids: List[str] = []
    rejected_finding_ids: List[str] = []
    downgraded_finding_ids: List[str] = []
    reviewer_notes: List[str] = []

class AgentReport(BaseModel):
    executive_summary: str
    risk_level: str
    recommendations: List[str] = []
    research_notes: List[str] = []
