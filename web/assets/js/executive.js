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

async function loadExecutiveKPIs() {
    const recommendation = await executiveApiGet("/copilot/recommendation");
    const timeline = await executiveApiGet("/copilot/timeline");
    const status = await executiveApiGet("/copilot/status");

    const card = document.getElementById("kpi-card");

    if (!card) return;

    card.innerHTML = `
        <div class="analytics-grid">
            <div class="analytics-kpi">
                <div class="analytics-label">Confidence</div>
                <div class="analytics-value">${executiveFormatConfidence(recommendation.confidence)}</div>
            </div>

            <div class="analytics-kpi">
                <div class="analytics-label">Priority</div>
                <div class="analytics-value">${recommendation.priority ?? "-"}</div>
            </div>

            <div class="analytics-kpi">
                <div class="analytics-label">Timeline</div>
                <div class="analytics-value">${timeline.count ?? 0}</div>
            </div>

            <div class="analytics-kpi">
                <div class="analytics-label">Platform</div>
                <div class="analytics-value">${status.platform_status ?? "-"}</div>
            </div>
        </div>
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
        <table>
            <tr>
                <td><strong>Risk Score</strong></td>
                <td>${risk.summary.risk_score}/100</td>
            </tr>
            <tr>
                <td><strong>Risk Severity</strong></td>
                <td>${risk.summary.risk_severity}</td>
            </tr>
            <tr>
                <td><strong>Provider Risk</strong></td>
                <td>${risk.metrics.provider_risk}</td>
            </tr>
            <tr>
                <td><strong>Capacity Risk</strong></td>
                <td>${risk.metrics.capacity_risk}</td>
            </tr>
            <tr>
                <td><strong>Forecast Risk</strong></td>
                <td>${risk.metrics.forecast_risk}</td>
            </tr>
            <tr>
                <td><strong>Recommendation</strong></td>
                <td>${risk.summary.recommendation}</td>
            </tr>
        </table>
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

async function loadExecutiveDashboard() {
    try {
        await Promise.all([
            loadExecutiveDecision(),
            loadExecutiveStatus(),
            loadExecutiveSummary(),
            loadExecutiveKPIs(),
            loadExecutiveAnalytics(),
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
