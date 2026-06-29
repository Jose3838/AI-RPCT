const REMOTE_API = "https://ai-rpct-production.up.railway.app";

let marketChart = null;

async function get(path) {
    const res = await fetch(REMOTE_API + path);
    return await res.json();
}

async function apiGet(endpoint) {
    const response = await fetch(endpoint);

    if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
    }

    return await response.json();
}

function formatDate(value) {
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

function formatConfidence(value) {
    const num = Number(value);

    if (Number.isNaN(num)) {
        return value ?? "";
    }

    return `${Math.round(num * 100)}%`;
}

function table(el, rows, cols) {
    if (!el) return;

    if (!rows || rows.length === 0) {
        el.innerHTML = "<tr><td>No data</td></tr>";
        return;
    }

    el.innerHTML =
        "<tr>" + cols.map(c => `<th>${c}</th>`).join("") + "</tr>" +
        rows.map(r =>
            "<tr>" + cols.map(c => `<td>${r[c] ?? ""}</td>`).join("") + "</tr>"
        ).join("");
}

async function loadLegacyDashboard() {
    const aiIndex = document.getElementById("aiIndex");

    if (!aiIndex) return;

    try {
        const snap = await get("/dashboard-snapshot");

        document.getElementById("aiIndex").innerText = snap.terminal.ai_infrastructure_index;
        document.getElementById("gpuPrice").innerText = snap.terminal.gpu_price_index;
        document.getElementById("riskScore").innerText = snap.risk.terminal_risk_score;
        document.getElementById("gpuTrend").innerText = snap.terminal.gpu_price_trend;
        document.getElementById("providerCount").innerText = snap.market_share.length;
        document.getElementById("quality").innerText = snap.quality.live_data_quality_score + "%";

        if (typeof Chart !== "undefined" && document.getElementById("marketShareChart")) {
            if (marketChart) {
                marketChart.destroy();
            }

            marketChart = new Chart(document.getElementById("marketShareChart"), {
                type: "doughnut",
                data: {
                    labels: snap.market_share.map(x => x.provider),
                    datasets: [{ data: snap.market_share.map(x => x.market_share_pct) }]
                }
            });
        }

        table(
            document.getElementById("providerHealth"),
            snap.provider_health,
            ["provider", "status", "rows", "freshness_hours", "health_score"]
        );

        table(
            document.getElementById("gpuTable"),
            snap.gpu_rankings,
            ["gpu", "offers", "avg_price", "min_price", "max_price"]
        );

        const refreshStatus = document.getElementById("refreshStatus");

        if (refreshStatus) {
            refreshStatus.innerText =
                "Live data refreshed: " + new Date().toLocaleTimeString();
        }
    } catch (err) {
        console.error(err);
    }
}

async function loadCopilotDecision() {
    try {
        const data = await apiGet("/copilot/decision");
        const card = document.getElementById("decision-card");

        if (!card) return;

        if (data.status) {
            card.innerHTML = `<h3>${data.status}</h3>`;
            return;
        }

        card.innerHTML = `
            <h3>${data.decision}</h3>
            <p><strong>Topic:</strong> ${data.topic}</p>
            <p><strong>Confidence:</strong> ${formatConfidence(data.confidence)}</p>
            <p><strong>Generated:</strong><br>${formatDate(data.generated_at)}</p>
        `;
    } catch (err) {
        console.error(err);
    }
}

async function loadExecutiveKPIs() {
    try {
        const recommendation = await apiGet("/copilot/recommendation");
        const timeline = await apiGet("/copilot/timeline");
        const status = await apiGet("/copilot/status");

        const card = document.getElementById("kpi-card");

        if (!card) return;

        card.innerHTML = `
            <table>
                <tr>
                    <td><strong>Confidence</strong></td>
                    <td>${formatConfidence(recommendation.confidence)}</td>
                </tr>

                <tr>
                    <td><strong>Priority</strong></td>
                    <td>${recommendation.priority.toUpperCase()}</td>
                </tr>

                <tr>
                    <td><strong>Timeline Entries</strong></td>
                    <td>${timeline.count}</td>
                </tr>

                <tr>
                    <td><strong>Platform</strong></td>
                    <td>${status.platform_status}</td>
                </tr>
            </table>
        `;
    } catch (err) {
        console.error(err);
    }
}

async function loadExecutiveAnalytics() {
    try {
        const analytics = await apiGet("/copilot/analytics");
        const card = document.getElementById("analytics-card");

        if (!card) return;

        if (analytics.status) {
            card.innerHTML = `<p>${analytics.status}</p>`;
            return;
        }

        card.innerHTML = `
            <table>
                <tr>
                    <td><strong>Decision Count</strong></td>
                    <td>${analytics.decision_count}</td>
                </tr>

                <tr>
                    <td><strong>Average Confidence</strong></td>
                    <td>${formatConfidence(analytics.average_confidence)}</td>
                </tr>

                <tr>
                    <td><strong>Max Confidence</strong></td>
                    <td>${formatConfidence(analytics.max_confidence)}</td>
                </tr>

                <tr>
                    <td><strong>Min Confidence</strong></td>
                    <td>${formatConfidence(analytics.min_confidence)}</td>
                </tr>
            </table>
        `;
    } catch (err) {
        console.error(err);
    }
}

async function loadExecutiveIntelligence() {
    try {
        const [
            decision,
            forecast,
            provider,
            capacity,
        ] = await Promise.all([
            apiGet("/copilot/decision-intelligence"),
            apiGet("/copilot/forecast-intelligence"),
            apiGet("/copilot/provider-intelligence"),
            apiGet("/copilot/capacity-intelligence"),
        ]);

        const card = document.getElementById("intelligence-card");

        if (!card) return;

        card.innerHTML = `
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
                    <td><strong>Provider Intelligence</strong></td>
                    <td>${provider.summary?.status ?? provider.status ?? "Unavailable"}</td>
                </tr>
                <tr>
                    <td><strong>Capacity Intelligence</strong></td>
                    <td>${capacity.summary?.status ?? capacity.status ?? "Unavailable"}</td>
                </tr>
            </table>
        `;
    } catch (err) {
        console.error(err);
    }
}

async function loadExecutiveRisk() {
    try {
        const risk = await apiGet("/copilot/risk-intelligence");
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
    } catch (err) {
        console.error(err);
    }
}

async function loadCopilotStatus() {
    try {
        const status = await apiGet("/copilot/status");
        const card = document.getElementById("health-card");

        if (!card) return;

        card.innerHTML = `
            <h3>🟢 ${status.platform_status}</h3>
            <p><strong>Pipeline:</strong> ${status.pipeline}</p>
            <p><strong>Decision Engine:</strong> ${status.decision_engine}</p>
            <p><strong>Forecast:</strong> ${status.forecast}</p>
        `;
    } catch (err) {
        console.error(err);
    }
}

async function loadCopilotSummary() {
    try {
        const summary = await apiGet("/copilot/summary");
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
    } catch (err) {
        console.error(err);
    }
}

async function loadCopilotTimeline() {
    try {
        const data = await apiGet("/copilot/timeline");
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
                                <td>${formatDate(row.generated_at)}</td>
                                <td>${row.recommendation}</td>
                                <td>${formatConfidence(row.confidence)}</td>
                            </tr>
                        `).join("")}
                    </tbody>
                </table>
            </div>
        `;
    } catch (err) {
        console.error(err);
    }
}

async function loadForecastStatus() {
    try {
        const forecast = await apiGet("/forecast");
        const card = document.getElementById("forecast-card");

        if (!card) return;

        card.innerHTML = `
            <h3>${forecast.length} Forecast Records</h3>
            <p>Forecast engine operational.</p>
        `;
    } catch (err) {
        console.error(err);
    }
}

async function loadRegistryStatus() {
    try {
        const registries = await apiGet("/registries");
        const card = document.getElementById("registry-card");

        if (!card) return;

        card.innerHTML = `
            <h3>${registries.length} Registry Entries</h3>
            <p>Registry metadata successfully loaded.</p>
        `;
    } catch (err) {
        console.error(err);
    }
}

loadLegacyDashboard();
loadCopilotDecision();
loadCopilotStatus();
loadCopilotSummary();
loadExecutiveKPIs();
loadExecutiveAnalytics();
loadExecutiveIntelligence();
loadExecutiveRisk();
loadCopilotTimeline();
loadForecastStatus();
loadRegistryStatus();

if (document.getElementById("aiIndex")) {
    setInterval(loadLegacyDashboard, 60000);
}

console.log("AI-RPCT Web Console loaded");
