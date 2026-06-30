from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class CopilotStatusResponseModel(BaseModel):
    platform_status: str
    pipeline: str
    decision_engine: str
    forecast: str
    tests: int


class CopilotSummaryResponseModel(BaseModel):
    brief_id: str
    generated_at: str
    market_status: str
    capacity_risk: str
    procurement_recommendation: str
    forecast_status: str
    platform_health: str
    summary: str


class CopilotRecommendationResponseModel(BaseModel):
    decision: str
    confidence: float
    recommendation_score: int
    priority: str
    priority_reason: str
    topic: str
    generated_at: str


class CopilotDecisionResponseModel(BaseModel):
    decision: str
    confidence: str
    topic: str
    generated_at: str


class CopilotTimelineEntryModel(BaseModel):
    generated_at: str
    topic: str
    recommendation: str
    confidence: str


class CopilotTimelineResponseModel(BaseModel):
    count: int
    returned: int
    timeline: list[CopilotTimelineEntryModel]


class ConfidenceTrendPointModel(BaseModel):
    generated_at: str | None
    confidence: float


class CopilotAnalyticsResponseModel(BaseModel):
    decision_count: int
    average_confidence: float
    max_confidence: float
    min_confidence: float

    unique_recommendations: int | None = None
    most_common_recommendation: str | None = None
    latest_recommendation: str | None = None
    decision_stability_score: float | None = None

    confidence_trend: list[ConfidenceTrendPointModel] = []

    recommendation_distribution: dict[str, int] = {}


class CopilotInsightModel(BaseModel):
    type: str
    severity: str
    message: str


class DecisionIntelligenceSummaryModel(BaseModel):
    status: str
    decision_count: int
    latest_decision: str | None


class DecisionIntelligenceMetricsModel(BaseModel):
    recommendation_count: int
    recommendation_consistency: bool


class DecisionIntelligenceResponseModel(BaseModel):
    summary: DecisionIntelligenceSummaryModel
    metrics: DecisionIntelligenceMetricsModel
    trends: dict[str, Any]
    insights: list[CopilotInsightModel]


class ExecutiveModulesModel(BaseModel):
    summary: CopilotSummaryResponseModel
    analytics: CopilotAnalyticsResponseModel
    decision_intelligence: DecisionIntelligenceResponseModel
    forecast_intelligence: ForecastIntelligenceResponseModel
    provider_intelligence: ProviderIntelligenceResponseModel
    capacity_intelligence: CapacityIntelligenceResponseModel
    risk_intelligence: RiskIntelligenceResponseModel


class ExecutiveIntelligenceResponseModel(BaseModel):
    summary: ExecutiveSummaryModel
    modules: ExecutiveModulesModel


class ExecutiveSnapshotSummaryModel(BaseModel):
    status: str
    snapshot_count: int
    latest_snapshot: ExecutiveSnapshotModel


class ExecutiveSnapshotsResponseModel(BaseModel):
    summary: ExecutiveSnapshotSummaryModel
    snapshots: list[ExecutiveSnapshotModel]


class ChangeIntelligenceSummaryModel(BaseModel):
    status: str
    baseline: str
    snapshot_count: int


class ChangeIntelligenceMetricsModel(BaseModel):
    risk_score: int | None = None
    risk_severity: str | None = None


class ChangeEventModel(BaseModel):
    metric: str
    previous: int | str
    current: int | str
    delta: int | None = None
    severity: str


class ChangeIntelligenceResponseModel(BaseModel):
    summary: ChangeIntelligenceSummaryModel
    metrics: ChangeIntelligenceMetricsModel
    changes: list[ChangeEventModel]
    insights: list[CopilotInsightModel]


class ProviderIntelligenceSummaryModel(BaseModel):
    status: str
    provider_count: int
    active_provider_count: int


class ProviderIntelligenceMetricsModel(BaseModel):
    provider_categories: dict[str, int]


class ProviderIntelligenceResponseModel(BaseModel):
    summary: ProviderIntelligenceSummaryModel
    metrics: ProviderIntelligenceMetricsModel
    trends: dict[str, Any]
    insights: list[CopilotInsightModel]


class CapacityIntelligenceSummaryModel(BaseModel):
    status: str
    capacity_records: int


class CapacityIntelligenceMetricsModel(BaseModel):
    capacity_status: dict[str, int]
    availability_levels: dict[str, int]


class CapacityIntelligenceResponseModel(BaseModel):
    summary: CapacityIntelligenceSummaryModel
    metrics: CapacityIntelligenceMetricsModel
    trends: dict[str, Any]
    insights: list[CopilotInsightModel]


class ForecastIntelligenceSummaryModel(BaseModel):
    status: str
    forecast_count: int


class ForecastIntelligenceResponseModel(BaseModel):
    summary: ForecastIntelligenceSummaryModel
    metrics: dict[str, Any]
    trends: dict[str, Any]
    insights: list[CopilotInsightModel]


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


class ExecutiveDecisionCenterKPIModel(BaseModel):
    snapshot_count: int
    change_events: int
    risk_score: int
    priority: str


class ExecutiveMetadataModel(BaseModel):
    version: str
    module: str
    generated_by: str


class ExecutiveDecisionCenterResponseModel(BaseModel):
    summary: ExecutiveSummaryModel
    metadata: ExecutiveMetadataModel
    priority: str
    kpis: ExecutiveDecisionCenterKPIModel
    risk: RiskIntelligenceResponseModel
    recommendation: dict[str, Any]
    changes: dict[str, Any]
    snapshots: dict[str, Any]
    executive_intelligence: dict[str, Any]
