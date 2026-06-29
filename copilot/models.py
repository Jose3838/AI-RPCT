from __future__ import annotations

from pydantic import BaseModel


class ExecutiveSnapshotModel(BaseModel):
    snapshot_id: str
    generated_at: str
    risk_score: int
    risk_severity: str
    recommendation: str
    source: str


class ExecutiveSummaryModel(BaseModel):
    status: str
    generated_at: str
    overall_risk_score: int
    overall_risk_severity: str
    overall_recommendation: str


class ExecutiveRecommendationModel(BaseModel):
    action: str
    reason: str
    owner: str


class ExecutiveRecommendationSummaryModel(BaseModel):
    status: str
    priority: str


class ExecutiveRecommendationResponseModel(BaseModel):
    summary: ExecutiveRecommendationSummaryModel
    recommendation: ExecutiveRecommendationModel
