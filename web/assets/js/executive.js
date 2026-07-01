async function executiveApiGet(endpoint) {
    const response = await fetch(endpoint);

    if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
    }

    return await response.json();
}

function executiveFormatDate(value) {
    if (!value) return "";

    const date = new Date(value);

    if (Number.isNaN(date.getTime())) {
        return value;
    }

    return date.toLocaleString("de-DE", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
    });
}

function executiveFormatConfidence(value) {
    const num = Number(value);

    if (Number.isNaN(num)) {
        return value ?? "";
    }

    return `${Math.round(num * 100)}%`;
}

function executiveForecastInterpretation(forecast) {
    const summary = forecast.summary || {};
    const watchCount = Number(summary.watch_count || 0);
    const monitorCount = Number(summary.monitor_count || 0);
    const providerCount = Number(summary.provider_count || 0);
    const entityCount = Number(summary.entity_count || 0);
    const latestClass = summary.latest_forecast_class || "-";
    const latestSignal = summary.latest_signal || "-";

    if (watchCount > 0) {
        return `
            <p>
                <strong>Executive Interpretation:</strong>
                Forecast intelligence currently shows ${watchCount} watch signal(s)
                across ${providerCount} provider(s) and ${entityCount} entity/entities.
                Latest forecast class is <strong>${latestClass}</strong> with signal
                <strong>${latestSignal}</strong>.
            </p>
            <p>
                Recommended executive action: monitor capacity-sensitive providers
                and keep procurement readiness active.
            </p>
        `;
    }

    return `
        <p>
            <strong>Executive Interpretation:</strong>
            Forecast intelligence currently shows ${monitorCount} monitor-only signal(s)
            across ${providerCount} provider(s) and ${entityCount} entity/entities.
            Latest forecast class is <strong>${latestClass}</strong>.
        </p>
        <p>
            Recommended executive action: continue monitoring. No immediate escalation
            is indicated by the current forecast layer.
        </p>
    `;
}

async function loadExecutiveDecision() {
    const data = await executiveApiGet("/copilot/decision");
    const card = document.getElementById("decision-card");

    if (!card) return;

    if (data.status) {
        card.innerHTML = `<h3>${data.status}</h3>`;
        return;
    }

    card.innerHTML = `
        <h3>${data.decision}</h3>
        <p><strong>Topic:</strong> ${data.topic}</p>
        <p><strong>Confidence:</strong> ${executiveFormatConfidence(data.confidence)}</p>
        <p><strong>Generated:</strong><br>${executiveFormatDate(data.generated_at)}</p>
    `;
}

async function loadExecutiveStatus() {
    const status = await executiveApiGet("/copilot/status");
    const card = document.getElementById("health-card");

    if (!card) return;

    card.innerHTML = `
        <h3>🟢 ${status.platform_status}</h3>
        <p><strong>Pipeline:</strong> ${status.pipeline}</p>
        <p><strong>Decision Engine:</strong> ${status.decision_engine}</p>
        <p><strong>Forecast:</strong> ${status.forecast}</p>
    `;
}

async function loadExecutiveSummary() {
    const summary = await executiveApiGet("/copilot/summary");
    const card = document.getElementById("summary-card");

    if (!card) return;

    if (summary.status) {
        card.innerHTML = `<p>${summary.status}</p>`;
        return;
    }

    card.innerHTML = `
        <p>${summary.summary ?? "No summary available."}</p>
        <p><strong>Market:</strong> ${summary.market_status ?? ""}</p>
        <p><strong>Capacity Risk:</strong> ${summary.capacity_risk ?? ""}</p>
    `;
}

function calculateExecutiveHealthScore(recommendation, status, risk, forecast) {
    let score = 100;

    const confidence = Number(recommendation.confidence || 0);
    const riskScore = Number(risk.summary?.risk_score || 0);
    const watchCount = Number(forecast.summary?.watch_count || 0);

    if (confidence < 0.8) {
        score -= 10;
    }

    if (riskScore >= 70) {
        score -= 20;
    } else if (riskScore >= 40) {
        score -= 10;
    }

    if (watchCount > 0) {
        score -= 10;
    }

    if (
        status.platform_status &&
        status.platform_status.toLowerCase() !== "healthy"
    ) {
        score -= 10;
    }

    return Math.max(score, 0);
}

function describeExecutiveHealth(score) {
    if (score >= 90) {
        return {
            label: "Excellent",
            action: "System operating normally. Continue monitoring executive signals.",
        };
    }

    if (score >= 75) {
        return {
            label: "Good",
            action: "Platform is stable. Monitor forecast watch signals and risk movement.",
        };
    }

    if (score >= 50) {
        return {
            label: "Attention",
            action: "Executive attention recommended. Review risk, forecast watch signals, and capacity exposure.",
        };
    }

    return {
        label: "Critical",
        action: "Immediate executive review recommended. Risk and forecast signals require escalation.",
    };
}

function renderExecutivePriorityMatrix(status, risk, forecast, recommendation) {
    const watchCount = Number(forecast.summary?.watch_count || 0);
    const riskScore = risk.summary?.risk_score ?? "-";

    const forecastMessage = watchCount > 0
        ? `${watchCount} watch signal(s) require monitoring`
        : "No watch signal currently active";

    return `
        <div style="margin-top:30px;">
            <h3>Executive Priority Matrix</h3>

            <div class="analytics-grid">
                <div class="analytics-kpi">
                    <div class="analytics-label">Platform</div>
                    <div class="analytics-value">${status.platform_status ?? "-"}</div>
                </div>

                <div class="analytics-kpi">
                    <div class="analytics-label">Forecast</div>
                    <div class="analytics-value">${watchCount}</div>
                </div>

                <div class="analytics-kpi">
                    <div class="analytics-label">Risk</div>
                    <div class="analytics-value">${riskScore}</div>
                </div>

                <div class="analytics-kpi">
                    <div class="analytics-label">Priority</div>
                    <div class="analytics-value">${recommendation.priority ?? "-"}</div>
                </div>
            </div>

            <p>
                <strong>Platform Status</strong><br>
                ${status.platform_status ?? "-"}
            </p>

            <p>
                <strong>Forecast</strong><br>
                ${forecastMessage}
            </p>

            <p>
                <strong>Risk</strong><br>
                Current risk score: ${riskScore}
            </p>

            <p>
                <strong>Recommendation</strong><br>
                ${recommendation.priority_reason ?? recommendation.decision ?? "-"}
            </p>
        </div>
    `;
}

async function loadExecutiveKPIs() {
    const [
        recommendation,
        timeline,
        status,
        risk,
        forecast,
    ] = await Promise.all([
        executiveApiGet("/copilot/recommendation"),
        executiveApiGet("/copilot/timeline"),
        executiveApiGet("/copilot/status"),
        executiveApiGet("/copilot/risk-intelligence"),
        executiveApiGet("/copilot/forecast-intelligence"),
    ]);

    const card = document.getElementById("kpi-card");

    if (!card) return;

    const healthScore = calculateExecutiveHealthScore(
        recommendation,
        status,
        risk,
        forecast
    );

    const health = describeExecutiveHealth(healthScore);

    card.innerHTML = `
        <div class="analytics-grid">
            <div class="analytics-kpi">
                <div class="analytics-label">Executive Health</div>
                <div class="analytics-value">${healthScore}%</div>
            </div>

            <div class="analytics-kpi">
                <div class="analytics-label">Health Status</div>
                <div class="analytics-value">${health.label}</div>
            </div>

            <div class="analytics-kpi">
                <div class="analytics-label">Confidence</div>
                <div class="analytics-value">${executiveFormatConfidence(recommendation.confidence)}</div>
            </div>

            <div class="analytics-kpi">
                <div class="analytics-label">Priority</div>
                <div class="analytics-value">${recommendation.priority ?? "-"}</div>
            </div>

            <div class="analytics-kpi">
                <div class="analytics-label">Risk Score</div>
                <div class="analytics-value">${risk.summary?.risk_score ?? "-"}</div>
            </div>

            <div class="analytics-kpi">
                <div class="analytics-label">Forecast Watch</div>
                <div class="analytics-value">${forecast.summary?.watch_count ?? 0}</div>
            </div>
        </div>

        <hr>

        <p>
            <strong>Executive Action</strong><br>
            ${health.action}
        </p>

        ${renderExecutivePriorityMatrix(
            status,
            risk,
            forecast,
            recommendation
        )}
    `;
}

async function loadExecutiveAnalytics() {
    const analytics = await executiveApiGet("/copilot/analytics");
    const card = document.getElementById("analytics-card");

    if (!card) return;

    if (analytics.status) {
        card.innerHTML = `<p>${analytics.status}</p>`;
        return;
    }

    card.innerHTML = `
        <div class="analytics-grid">
            <div class="analytics-kpi">
                <div class="analytics-label">Decisions</div>
                <div class="analytics-value">${analytics.decision_count}</div>
            </div>

            <div class="analytics-kpi">
                <div class="analytics-label">Average Confidence</div>
                <div class="analytics-value">${executiveFormatConfidence(analytics.average_confidence)}</div>
            </div>

            <div class="analytics-kpi">
                <div class="analytics-label">Stability Score</div>
                <div class="analytics-value">${executiveFormatConfidence(analytics.decision_stability_score ?? 0)}</div>
            </div>

            <div class="analytics-kpi">
                <div class="analytics-label">Recommendations</div>
                <div class="analytics-value">${analytics.unique_recommendations ?? 0}</div>
            </div>
        </div>

        <hr>

        <p>
            <strong>Current Recommendation</strong><br>
            ${analytics.latest_recommendation ?? "-"}
        </p>

        <p>
            <strong>Most Common Recommendation</strong><br>
            ${analytics.most_common_recommendation ?? "-"}
        </p>

        <div style="margin-top:30px;">
            <h3>Confidence Trend</h3>
            <div id="confidence-chart"></div>
        </div>

        <div style="margin-top:30px;">
            <h3>Recommendation Distribution</h3>
            <div id="recommendation-chart"></div>
        </div>
    `;

    if (window.AiRpctCharts && analytics.confidence_trend) {
        AiRpctCharts.renderConfidenceTrend(
            "confidence-chart",
            analytics.confidence_trend
        );
    }

    if (window.AiRpctCharts && analytics.recommendation_distribution) {
        const items = Object.entries(
            analytics.recommendation_distribution
        ).map(([label, value]) => ({
            label,
            value,
        }));

        AiRpctCharts.renderBar("recommendation-chart", items, {
            labelKey: "label",
            valueKey: "value",
            showValue: false,
        });
    }
}

async function loadExecutiveTrend() {
    const trend = await executiveApiGet("/copilot/executive-trend");
    const card = document.getElementById("trend-card");

    if (!card) return;

    if (trend.status) {
        card.innerHTML = `<p>${trend.status}</p>`;
        return;
    }

    const confidenceHistory = trend.trends?.confidence_history ?? [];
    const riskHistory = trend.trends?.risk_history ?? [];

    const latestConfidence = trend.summary?.latest_confidence;
    const latestRiskScore = trend.summary?.latest_risk_score;
    const forecastWatchCount = trend.summary?.forecast_watch_count ?? 0;

    card.innerHTML = `
        <div class="analytics-grid">
            <div class="analytics-kpi">
                <div class="analytics-label">Decision Points</div>
                <div class="analytics-value">${trend.summary?.decision_points ?? 0}</div>
            </div>

            <div class="analytics-kpi">
                <div class="analytics-label">Risk Points</div>
                <div class="analytics-value">${trend.summary?.risk_points ?? 0}</div>
            </div>

            <div class="analytics-kpi">
                <div class="analytics-label">Latest Confidence</div>
                <div class="analytics-value">${executiveFormatConfidence(latestConfidence)}</div>
            </div>

            <div class="analytics-kpi">
                <div class="analytics-label">Latest Risk</div>
                <div class="analytics-value">${latestRiskScore ?? "-"}</div>
            </div>

            <div class="analytics-kpi">
                <div class="analytics-label">Forecast Watch</div>
                <div class="analytics-value">${forecastWatchCount}</div>
            </div>
        </div>

        <hr>

        <div style="margin-top:30px;">
            <h3>Executive Confidence Trend</h3>
            <div id="executive-confidence-trend-chart"></div>
        </div>

        <div style="margin-top:30px;">
            <h3>Executive Risk Trend</h3>
            <div id="executive-risk-trend-chart"></div>
        </div>
    `;

    if (window.AiRpctCharts && confidenceHistory.length > 0) {
        AiRpctCharts.renderConfidenceTrend(
            "executive-confidence-trend-chart",
            confidenceHistory
        );
    }

    if (window.AiRpctCharts && riskHistory.length > 0) {
        const normalizedRiskHistory = riskHistory.map((point) => ({
            generated_at: point.generated_at,
            confidence: Number(point.risk_score || 0) / 100,
        }));

        AiRpctCharts.renderConfidenceTrend(
            "executive-risk-trend-chart",
            normalizedRiskHistory
        );
    }
}

async function loadExecutiveAlerts() {
    const data = await executiveApiGet("/copilot/change-intelligence");
    const card = document.getElementById("alert-card");

    if (!card) return;

    const alerts = data.alerts ?? [];

    if (alerts.length === 0) {
        card.innerHTML = "<p>No executive alerts.</p>";
        return;
    }

    card.innerHTML = alerts.map(alert => `
        <div style="margin-bottom:16px;padding:12px;border-left:6px solid #3b82f6;background:#f8fafc;">
            <strong>${alert.severity.toUpperCase()}</strong><br>
            ${alert.message}
        </div>
    `).join("");
}

async function loadExecutiveInsights() {
    const data = await executiveApiGet("/copilot/executive-insights");
    const card = document.getElementById("insights-card");

    if (!card) return;

    const summary = data.summary ?? {};
    const insights = data.insights ?? [];

    card.innerHTML = `
        <div class="analytics-grid">
            <div class="analytics-kpi">
                <div class="analytics-label">Average Confidence</div>
                <div class="analytics-value">
                    ${executiveFormatConfidence(summary.average_confidence)}
                </div>
            </div>

            <div class="analytics-kpi">
                <div class="analytics-label">Latest Risk</div>
                <div class="analytics-value">
                    ${summary.latest_risk_score ?? "-"}
                </div>
            </div>

            <div class="analytics-kpi">
                <div class="analytics-label">Risk Delta</div>
                <div class="analytics-value">
                    ${summary.risk_delta ?? "-"}
                </div>
            </div>
        </div>

        <hr>

        ${insights.map(item => `
            <p>
                <strong>${item.type}</strong><br>
                ${item.message}
            </p>
        `).join("")}
    `;
}

async function loadExecutiveIntelligence() {
    const [
        decision,
        forecast,
        provider,
        capacity,
    ] = await Promise.all([
        executiveApiGet("/copilot/decision-intelligence"),
        executiveApiGet("/copilot/forecast-intelligence"),
        executiveApiGet("/copilot/provider-intelligence"),
        executiveApiGet("/copilot/capacity-intelligence"),
    ]);

    const card = document.getElementById("intelligence-card");

    if (!card) return;

    card.innerHTML = `
        <div class="analytics-grid">
            <div class="analytics-kpi">
                <div class="analytics-label">Forecast Records</div>
                <div class="analytics-value">${forecast.summary?.forecast_count ?? "-"}</div>
            </div>

            <div class="analytics-kpi">
                <div class="analytics-label">Providers</div>
                <div class="analytics-value">${forecast.summary?.provider_count ?? "-"}</div>
            </div>

            <div class="analytics-kpi">
                <div class="analytics-label">Watch Signals</div>
                <div class="analytics-value">${forecast.summary?.watch_count ?? "-"}</div>
            </div>

            <div class="analytics-kpi">
                <div class="analytics-label">Monitor Signals</div>
                <div class="analytics-value">${forecast.summary?.monitor_count ?? "-"}</div>
            </div>
        </div>

        <hr>

        <div style="margin-top:30px;">
            <h3>Forecast Class Distribution</h3>
            <div id="forecast-class-chart"></div>
        </div>

        <div style="margin-top:30px;">
            <h3>Rule-Based Signals</h3>
            <div id="forecast-signal-chart"></div>
        </div>

        <div style="margin-top:30px;">
            <h3>Governance Status</h3>
            <div id="forecast-governance-chart"></div>
        </div>

        <hr>

        ${executiveForecastInterpretation(forecast)}

        <hr>

        <table>
            <tr>
                <td><strong>Decision Intelligence</strong></td>
                <td>${decision.summary?.status ?? decision.status ?? "Unavailable"}</td>
            </tr>

            <tr>
                <td><strong>Forecast Intelligence</strong></td>
                <td>${forecast.summary?.status ?? forecast.status ?? "Unavailable"}</td>
            </tr>

            <tr>
                <td><strong>Latest Forecast Class</strong></td>
                <td>${forecast.summary?.latest_forecast_class ?? "-"}</td>
            </tr>

            <tr>
                <td><strong>Latest Signal</strong></td>
                <td>${forecast.summary?.latest_signal ?? "-"}</td>
            </tr>

            <tr>
                <td><strong>Provider Intelligence</strong></td>
                <td>${provider.summary?.status ?? provider.status ?? "Unavailable"}</td>
            </tr>

            <tr>
                <td><strong>Capacity Intelligence</strong></td>
                <td>${capacity.summary?.status ?? capacity.status ?? "Unavailable"}</td>
            </tr>
        </table>
    `;

    if (window.AiRpctCharts && forecast.metrics?.forecast_classes) {
        const forecastClassItems = Object.entries(
            forecast.metrics.forecast_classes
        ).map(([label, value]) => ({
            label,
            value,
        }));

        AiRpctCharts.renderBar("forecast-class-chart", forecastClassItems, {
            labelKey: "label",
            valueKey: "value",
            showValue: true,
        });
    }

    if (window.AiRpctCharts && forecast.metrics?.rule_based_signals) {
        const signalItems = Object.entries(
            forecast.metrics.rule_based_signals
        ).map(([label, value]) => ({
            label,
            value,
        }));

        AiRpctCharts.renderBar("forecast-signal-chart", signalItems, {
            labelKey: "label",
            valueKey: "value",
            showValue: true,
        });
    }

    if (window.AiRpctCharts && forecast.metrics?.governance_statuses) {
        const governanceItems = Object.entries(
            forecast.metrics.governance_statuses
        ).map(([label, value]) => ({
            label,
            value,
        }));

        AiRpctCharts.renderBar("forecast-governance-chart", governanceItems, {
            labelKey: "label",
            valueKey: "value",
            showValue: true,
        });
    }
}

async function loadExecutiveRisk() {
    const risk = await executiveApiGet("/copilot/risk-intelligence");
    const card = document.getElementById("risk-card");

    if (!card) return;

    if (risk.status) {
        card.innerHTML = `<p>${risk.status}</p>`;
        return;
    }
    card.innerHTML = `
    <div class="analytics-grid">

        <div class="analytics-kpi">
            <div class="analytics-label">Risk Score</div>
            <div class="analytics-value">
                ${risk.summary.risk_score}/100
            </div>
        </div>

        <div class="analytics-kpi">
            <div class="analytics-label">Severity</div>
            <div class="analytics-value">
                ${risk.summary.risk_severity}
            </div>
        </div>

        <div class="analytics-kpi">
            <div class="analytics-label">Provider Score</div>
            <div class="analytics-value">
                ${risk.metrics.provider_risk_score ?? "-"}
            </div>
        </div>

        <div class="analytics-kpi">
            <div class="analytics-label">Capacity Score</div>
            <div class="analytics-value">
                ${risk.metrics.capacity_risk_score ?? "-"}
            </div>
        </div>

        <div class="analytics-kpi">
            <div class="analytics-label">Forecast Score</div>
            <div class="analytics-value">
                ${risk.metrics.forecast_risk_score ?? "-"}
            </div>
        </div>

    </div>

    <hr>

    <p>
        <strong>Recommendation</strong><br>
        ${risk.summary.recommendation}
    </p>

    <p>
        <strong>Risk Explanation</strong><br>
        ${risk.summary.risk_explanation ?? "-"}
    </p>

    <h3>Risk Drivers</h3>

    <ul>
        ${(risk.risk_drivers ?? [])
            .map(driver => `
                <li>
                    <strong>${driver.area}</strong>
                    (${driver.severity}) —
                    ${driver.message}
                </li>
            `)
            .join("")}
    </ul>
`;

}

async function loadExecutiveTimeline() {
    const data = await executiveApiGet("/copilot/timeline");
    const card = document.getElementById("timeline-card");

    if (!card) return;

    if (data.status) {
        card.innerHTML = `<p>${data.status}</p>`;
        return;
    }

    const rows = data.timeline.slice().reverse();

    card.innerHTML = `
        <p><strong>Total decisions:</strong> ${data.count}</p>
        <div class="table-wrap">
            <table>
                <thead>
                    <tr>
                        <th>Generated</th>
                        <th>Recommendation</th>
                        <th>Confidence</th>
                    </tr>
                </thead>
                <tbody>
                    ${rows.map(row => `
                        <tr>
                            <td>${executiveFormatDate(row.generated_at)}</td>
                            <td>${row.recommendation}</td>
                            <td>${executiveFormatConfidence(row.confidence)}</td>
                        </tr>
                    `).join("")}
                </tbody>
            </table>
        </div>
    `;
}

async function loadExecutiveForecastStatus() {
    const forecast = await executiveApiGet("/forecast");
    const card = document.getElementById("forecast-card");

    if (!card) return;

    card.innerHTML = `
        <h3>${forecast.length} Forecast Records</h3>
        <p>Forecast engine operational.</p>
    `;
}

async function loadExecutiveRegistryStatus() {
    const registries = await executiveApiGet("/registries");
    const card = document.getElementById("registry-card");

    if (!card) return;

    card.innerHTML = `
        <h3>${registries.length} Registry Entries</h3>
        <p>Registry metadata successfully loaded.</p>
    `;
}

async function loadExecutiveDecisionCenter() {
    const center = await executiveApiGet("/copilot/executive-decision-center");

    const card = document.getElementById("decision-center-card");

    if (!card) return;

    const health = center.executive_health || {};
    const kpis = center.kpis || {};

    card.innerHTML = `
        <div class="analytics-grid">
            <div class="analytics-kpi">
                <div class="analytics-label">Executive Health</div>
                <div class="analytics-value">${health.score ?? "-"}</div>
            </div>

            <div class="analytics-kpi">
                <div class="analytics-label">Risk Score</div>
                <div class="analytics-value">${kpis.risk_score ?? "-"}</div>
            </div>

            <div class="analytics-kpi">
                <div class="analytics-label">Forecast Watch</div>
                <div class="analytics-value">${kpis.forecast_watch_count ?? "-"}</div>
            </div>

            <div class="analytics-kpi">
                <div class="analytics-label">Priority</div>
                <div class="analytics-value">${center.priority ?? "-"}</div>
            </div>
        </div>

        <hr>

        <p>
            <strong>Overall Recommendation</strong><br>
            ${center.summary?.overall_recommendation ?? "-"}
        </p>

        <p>
            <strong>Executive Action</strong><br>
            ${health.action ?? "-"}
        </p>

        <p>
            <strong>Platform Status</strong><br>
            ${health.platform_status ?? "-"}
        </p>

        <p>
            <strong>Decision Center Version</strong><br>
            ${center.metadata?.version ?? "-"}
        </p>
    `;
}

async function loadExecutiveDashboard() {
    try {
        await Promise.all([
            loadExecutiveDecisionCenter(),
            loadExecutiveDecision(),
            loadExecutiveStatus(),
            loadExecutiveSummary(),
            loadExecutiveKPIs(),
            loadExecutiveAnalytics(),
            loadExecutiveTrend(),
            loadExecutiveAlerts(),
            loadExecutiveInsights(),
            loadExecutiveIntelligence(),
            loadExecutiveRisk(),
            loadExecutiveTimeline(),
            loadExecutiveForecastStatus(),
            loadExecutiveRegistryStatus(),
        ]);

        console.log("AI-RPCT Executive Dashboard loaded");
    } catch (err) {
        console.error(err);
    }
}

loadExecutiveDashboard();
