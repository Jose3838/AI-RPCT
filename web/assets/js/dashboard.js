function renderExecutiveDashboard(payload) {
  const dashboard = payload.dashboard || payload;
  const kpis = dashboard.kpis || {};
  const sections = dashboard.sections || {};
  const pipeline = sections.pipeline || {};

  AiRpctUi.setText("pipelineHealth", `${AiRpctUi.format(kpis.pipeline_health, 0)}%`);
  AiRpctUi.setStatus("pipelineStatus", kpis.pipeline_status);
  AiRpctUi.setText("riskScore", kpis.risk_score);
  AiRpctUi.setStatus("riskSeverity", kpis.risk_severity);
  AiRpctUi.setText("recommendation", kpis.recommendation);
  AiRpctUi.setStatus("forecastStatus", kpis.forecast_status);
  AiRpctUi.setText("providerCount", kpis.provider_count);
  AiRpctUi.setText("activeProviderCount", kpis.active_provider_count);
  AiRpctUi.setText("capacityRecords", kpis.capacity_records);

  AiRpctUi.setText("passedSteps", pipeline.passed);
  AiRpctUi.setText("totalSteps", pipeline.total);
  AiRpctUi.setText("duration", `${AiRpctUi.format(pipeline.total_duration, 0)}s`);
  AiRpctUi.setText("slowestStep", pipeline.slowest_step);

  AiRpctUi.setText(
    "executiveInsight",
    "AI-RPCT combines infrastructure risk, forecast signals, provider intelligence, capacity records and pipeline health into one executive operating view."
  );

  AiRpctUi.setText("lastUpdated", `Live API connected · ${new Date().toLocaleString()}`);
}

function renderProviderRankingChart(rows) {
  const chartRows = rows.slice(0, 8).map((row) => ({
    provider: row.provider,
    score: Number(row.score || 0).toFixed(2),
  }));

  AiRpctCharts.renderBar("providerRankingChart", chartRows, {
    labelKey: "provider",
    valueKey: "score",
  });
}

function renderProviderMarketShare(rows) {
  AiRpctCharts.renderDonut("providerMarketShareChart", rows, {
    labelKey: "provider",
    valueKey: "market_share",
  });
}

function renderActivityFeed(rows) {
  const container = document.getElementById("activityFeed");

  if (!container) return;

  const recentRows = rows.slice(-6).reverse();

  container.innerHTML = recentRows.map((row) => `
    <div class="activity-item">
      <div>
        <strong>Pipeline ${AiRpctUi.format(row.status)}</strong>
        <p>${AiRpctUi.format(row.timestamp)}</p>
      </div>
      <span>${AiRpctUi.format(row.passed)}/${AiRpctUi.format(row.total)}</span>
    </div>
  `).join("");
}

async function loadDashboard() {
  try {
    const dashboardPayload = await AiRpctApi.getDashboard();
    const providerRankings = await AiRpctApi.getProviderRankings();
    const providerMarketShare = await AiRpctApi.getProviderMarketShare();
    const pipelineHistory = await AiRpctApi.getPipelineHistory();

    renderExecutiveDashboard(dashboardPayload);
    renderProviderRankingChart(providerRankings);
    renderProviderMarketShare(providerMarketShare);
    renderActivityFeed(pipelineHistory);
  } catch (error) {
    console.error(error);
    AiRpctUi.setText("lastUpdated", "Dashboard API unavailable");
    AiRpctUi.setText("executiveInsight", "Start the API with: uvicorn api.main:app --reload");
  }
}

loadDashboard();
setInterval(loadDashboard, 30000);
