from __future__ import annotations

from typing import Any

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


class RiskSummaryModel(BaseModel):
    status: str
    risk_score: int
    risk_severity: str
    recommendation: str


class RiskMetricsModel(BaseModel):
    provider_count: int
    capacity_records: int
    forecast_records: int
    provider_risk: str
    capacity_risk: str
    forecast_risk: str


class RiskInsightModel(BaseModel):
    type: str
    severity: str
    message: str


class RiskIntelligenceResponseModel(BaseModel):
    summary: RiskSummaryModel
    metrics: RiskMetricsModel
    trends: dict[str, Any]
    insights: list[RiskInsightModel]


class ExecutiveDecisionCenterResponseModel(BaseModel):
    summary: ExecutiveSummaryModel
    priority: str
    risk: RiskIntelligenceResponseModel
    recommendation: dict[str, Any]
    changes: dict[str, Any]
    snapshots: dict[str, Any]
    executive_intelligence: dict[str, Any]
