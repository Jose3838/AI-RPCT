const API="https://ai-rpct-production.up.railway.app";
let marketChart=null;

async function get(path){
  const res=await fetch(API+path);
  return await res.json();
}

function table(el, rows, cols){
  if(!rows || rows.length===0){
    el.innerHTML="<tr><td>No data</td></tr>";
    return;
  }

  el.innerHTML =
    "<tr>" + cols.map(c=>`<th>${c}</th>`).join("") + "</tr>" +
    rows.map(r =>
      "<tr>" + cols.map(c=>`<td>${r[c]}</td>`).join("") + "</tr>"
    ).join("");
}

async function load(){
  const snap = await get("/dashboard-snapshot");

  document.getElementById("aiIndex").innerText = snap.terminal.ai_infrastructure_index;
  document.getElementById("gpuPrice").innerText = snap.terminal.gpu_price_index;
  document.getElementById("riskScore").innerText = snap.risk.terminal_risk_score;
  document.getElementById("gpuTrend").innerText = snap.terminal.gpu_price_trend;
  document.getElementById("providerCount").innerText = snap.market_share.length;
  document.getElementById("quality").innerText = snap.quality.live_data_quality_score + "%";

  if(marketChart){ marketChart.destroy(); }

  marketChart = new Chart(document.getElementById("marketShareChart"),{
    type:"doughnut",
    data:{
      labels:snap.market_share.map(x=>x.provider),
      datasets:[{data:snap.market_share.map(x=>x.market_share_pct)}]
    }
  });

  table(document.getElementById("providerHealth"), snap.provider_health, ["provider","status","rows","freshness_hours","health_score"]);
  table(document.getElementById("gpuTable"), snap.gpu_rankings, ["gpu","offers","avg_price","min_price","max_price"]);

  document.getElementById("refreshStatus").innerText =
    "Live data refreshed: " + new Date().toLocaleTimeString();
}

load();
setInterval(load,60000);

async function loadTerminalIntelligenceV1() {
  try {
    const res = await fetch("/terminal-intelligence-summary-v1");
    const data = await res.json();

    console.log("Terminal Intelligence V1", data);

    const status = document.getElementById("refreshStatus");
    if (status) {
      status.innerText = "Live intelligence loaded";
    }

  } catch (err) {
    console.error("Terminal Intelligence V1 failed", err);
  }
}

loadTerminalIntelligenceV1();

async function renderTerminalIntelligenceCards() {
  try {
    const res = await fetch("/terminal-intelligence-summary-v1");
    const data = await res.json();

    const breadth = data.market_breadth?.gpu_markets ?? "...";
    const concentration = data.provider_concentration?.largest_provider_share;
    const observations = data.snapshot_integrity?.rows ?? "...";
    const gpuModels = data.snapshot_integrity?.gpu_models ?? "...";

    const marketBreadthEl = document.getElementById("marketBreadth");
    const providerConcentrationEl = document.getElementById("providerConcentration");
    const historicalObservationsEl = document.getElementById("historicalObservations");
    const gpuModelsEl = document.getElementById("gpuModels");

    if (marketBreadthEl) marketBreadthEl.innerText = breadth;
    if (providerConcentrationEl) {
      providerConcentrationEl.innerText =
        concentration !== undefined
          ? Math.round(concentration * 100) + "%"
          : "...";
    }
    if (historicalObservationsEl) historicalObservationsEl.innerText = observations;
    if (gpuModelsEl) gpuModelsEl.innerText = gpuModels;

  } catch (err) {
    console.error("Failed to render intelligence cards", err);
  }
}

renderTerminalIntelligenceCards();

async function renderGpuMarketDepthTable() {
  try {
    const res = await fetch("/terminal-intelligence-summary-v1");
    const data = await res.json();

    const rows = data.gpu_market_depth || [];
    const table = document.getElementById("gpuMarketDepthTable");

    if (!table) return;

    table.innerHTML = `
      <tr>
        <th>GPU</th>
        <th>Offers</th>
        <th>Min $/h</th>
        <th>Avg $/h</th>
        <th>Max $/h</th>
      </tr>
      ${rows.map(r => `
        <tr>
          <td>${r.gpu_model}</td>
          <td>${r.offer_count}</td>
          <td>${r.min_price}</td>
          <td>${r.avg_price}</td>
          <td>${r.max_price}</td>
        </tr>
      `).join("")}
    `;

  } catch (err) {
    console.error("Failed to render GPU market depth", err);
  }
}

renderGpuMarketDepthTable();

async function renderGpuLeadersTable() {

  try {

    const res = await fetch(
      "/terminal-intelligence-summary-v1"
    )

    const data = await res.json()

    const rows =
      data.gpu_market_leaders || []

    const table =
      document.getElementById(
        "gpuLeadersTable"
      )

    if (!table) return

    table.innerHTML = `
      <tr>
        <th>GPU</th>
        <th>Leader</th>
        <th>Observations</th>
      </tr>
      ${rows.map(r => `
        <tr>
          <td>${r.gpu_model}</td>
          <td>${r.leader}</td>
          <td>${r.observations}</td>
        </tr>
      `).join("")}
    `

  } catch(err) {

    console.error(err)

  }
}

renderGpuLeadersTable()

async function renderDailyAlphaFeed() {
  try {
    const res = await fetch("/terminal-intelligence-summary-v1");
    const data = await res.json();

    const feed = data.daily_alpha_feed || {};
    const opportunities = feed.opportunities || [];
    const risks = feed.risks || [];

    const oppTable = document.getElementById("opportunityFeedTable");
    const riskTable = document.getElementById("riskFeedTable");

    if (oppTable) {
      oppTable.innerHTML = `
        <tr>
          <th>GPU</th>
          <th>Latest Price</th>
          <th>Historical Avg</th>
        </tr>
        ${
          opportunities.length
            ? opportunities.map(r => `
              <tr>
                <td>${r.gpu_model}</td>
                <td>${r.latest_price}</td>
                <td>${r.historical_avg}</td>
              </tr>
            `).join("")
            : `<tr><td colspan="3">No current opportunities detected</td></tr>`
        }
      `;
    }

    if (riskTable) {
      riskTable.innerHTML = `
        <tr>
          <th>GPU</th>
          <th>Latest Supply</th>
          <th>Historical Supply</th>
        </tr>
        ${
          risks.length
            ? risks.map(r => `
              <tr>
                <td>${r.gpu_model}</td>
                <td>${r.latest_supply}</td>
                <td>${r.historical_supply}</td>
              </tr>
            `).join("")
            : `<tr><td colspan="3">No current risks detected</td></tr>`
        }
      `;
    }

  } catch (err) {
    console.error("Failed to render daily alpha feed", err);
  }
}

renderDailyAlphaFeed();

async function renderMarketNarrative() {
  try {
    const res = await fetch("/terminal-market-narrative-v1");
    const data = await res.json();

    const headline = document.getElementById("marketNarrativeHeadline");
    const summary = document.getElementById("marketNarrativeSummary");

    if (headline) headline.innerText = data.headline || "...";
    if (summary) summary.innerText = data.summary || "No narrative available.";

  } catch (err) {
    console.error("Failed to render market narrative", err);
  }
}

renderMarketNarrative();

async function renderInvestorSnapshot() {
  try {
    const res = await fetch("/terminal-investor-snapshot-v1");
    const data = await res.json();

    const positioning = document.getElementById("investorPositioning");
    const readout = document.getElementById("investorCommercialReadout");

    if (positioning) positioning.innerText = data.positioning || "...";
    if (readout) readout.innerText = data.commercial_readout || "...";

  } catch (err) {
    console.error("Failed to render investor snapshot", err);
  }
}

renderInvestorSnapshot();

async function renderDataMoatPanel() {
  try {
    const res = await fetch("/terminal-data-moat-v1");
    const data = await res.json();

    const observations = document.getElementById("moatObservations");
    const assetSize = document.getElementById("moatAssetSize");
    const readout = document.getElementById("moatReadout");

    if (observations) observations.innerText = data.observations ?? "...";

    if (assetSize) {
      const kb = Math.round((data.total_asset_bytes || 0) / 1024);
      assetSize.innerText = kb + " KB";
    }

    if (readout) readout.innerText = data.readout || "...";

  } catch (err) {
    console.error("Failed to render data moat panel", err);
  }
}

renderDataMoatPanel();

async function renderSignalTape() {
  try {
    const res = await fetch("/terminal-signal-tape-v1");
    const data = await res.json();

    const tape = document.getElementById("signalTape");
    if (!tape) return;

    const signals = data.signals || [];

    tape.innerHTML = `
      <div class="signal-tape-inner">
        ${signals.map(s => `
          <span><strong>${s.type}</strong>${s.label}</span>
        `).join("")}
      </div>
    `;

  } catch (err) {
    console.error("Failed to render signal tape", err);
  }
}

renderSignalTape();

async function renderMarketMovers() {

  try {

    const res =
      await fetch(
        "/terminal-market-movers-v1"
      )

    const data =
      await res.json()

    const gainers =
      document.getElementById(
        "gpuGainersTable"
      )

    const losers =
      document.getElementById(
        "gpuLosersTable"
      )

    if(gainers){

      gainers.innerHTML = `
      <tr>
        <th>GPU</th>
        <th>Δ Price</th>
      </tr>
      ${
        (data.gainers || []).map(x => `
        <tr>
          <td>${x.gpu_model}</td>
          <td>+${x.price_change}</td>
        </tr>
        `).join("")
      }
      `
    }

    if(losers){

      losers.innerHTML = `
      <tr>
        <th>GPU</th>
        <th>Δ Price</th>
      </tr>
      ${
        (data.losers || []).map(x => `
        <tr>
          <td>${x.gpu_model}</td>
          <td>${x.price_change}</td>
        </tr>
        `).join("")
      }
      `
    }

  } catch(err){

    console.error(err)

  }
}

renderMarketMovers()

async function renderMarketMovers() {
  try {
    const res = await fetch("/terminal-market-movers-v1");
    const data = await res.json();

    const gainers = document.getElementById("gpuGainersTable");
    const losers = document.getElementById("gpuLosersTable");

    if (gainers) {
      gainers.innerHTML = `
        <tr>
          <th>GPU</th>
          <th>Δ Price</th>
        </tr>
        ${
          (data.gainers || []).length
            ? data.gainers.map(x => `
              <tr>
                <td>${x.gpu_model}</td>
                <td class="good">+${x.price_change}</td>
              </tr>
            `).join("")
            : `<tr><td colspan="2">No price gainers detected yet</td></tr>`
        }
      `;
    }

    if (losers) {
      losers.innerHTML = `
        <tr>
          <th>GPU</th>
          <th>Δ Price</th>
        </tr>
        ${
          (data.losers || []).length
            ? data.losers.map(x => `
              <tr>
                <td>${x.gpu_model}</td>
                <td class="bad">${x.price_change}</td>
              </tr>
            `).join("")
            : `<tr><td colspan="2">No price losers detected yet</td></tr>`
        }
      `;
    }

  } catch (err) {
    console.error("Failed to render market movers", err);
  }
}

renderMarketMovers();

async function renderProviderRiskPanel() {
  try {
    const res = await fetch("/terminal-provider-risk-v1");
    const data = await res.json();

    const headline = document.getElementById("providerRiskHeadline");
    const readout = document.getElementById("providerRiskReadout");

    if (headline) headline.innerText = data.headline || "...";
    if (readout) readout.innerText = data.readout || "...";

  } catch (err) {
    console.error("Failed to render provider risk", err);
  }
}

renderProviderRiskPanel();

async function renderForecastReadiness() {
  try {
    const res = await fetch("/terminal-forecast-readiness-v1");
    const data = await res.json();

    const score = document.getElementById("forecastReadinessScore");
    const readout = document.getElementById("forecastReadinessReadout");

    if (score) score.innerText = data.forecast_readiness_score + "/100";
    if (readout) readout.innerText = data.readout || "...";

  } catch (err) {
    console.error("Failed to render forecast readiness", err);
  }
}

renderForecastReadiness();

async function renderSystemHealthStrip() {
  try {
    const res = await fetch("/terminal-system-health-v1");
    const data = await res.json();

    const el = document.getElementById("systemHealthStrip");
    if (!el) return;

    el.innerText =
      `System ${data.status.toUpperCase()} · ${data.rows} observations · ${data.providers} providers · ${data.gpu_models} GPU markets`;

  } catch (err) {
    console.error("Failed to render system health strip", err);
  }
}

renderSystemHealthStrip();

async function renderDemoWarning() {
  try {
    const res = await fetch("/terminal-demo-warning-v1");
    const data = await res.json();

    const el = document.getElementById("demoWarning");
    if (!el) return;

    el.innerText = data.readout || "...";

    if (!data.demo_mode) {
      el.innerText = "All configured providers are live-ready.";
      el.style.color = "var(--green)";
      el.style.borderColor = "rgba(65,226,138,.35)";
      el.style.background = "rgba(65,226,138,.08)";
    }

  } catch (err) {
    console.error("Failed to render demo warning", err);
  }
}

renderDemoWarning();

function setTerminalLastUpdated() {
  const el = document.getElementById("terminalLastUpdated");
  if (!el) return;
  el.innerText = "Last updated: " + new Date().toLocaleString();
}

setTerminalLastUpdated();

setInterval(() => {
  renderSystemHealthStrip?.();
  renderSignalTape?.();
  renderTerminalIntelligenceCards?.();
  renderGpuMarketDepthTable?.();
  renderGpuLeadersTable?.();
  renderDailyAlphaFeed?.();
  renderMarketNarrative?.();
  renderInvestorSnapshot?.();
  renderDataMoatPanel?.();
  renderMarketMovers?.();
  renderProviderRiskPanel?.();
  renderForecastReadiness?.();
  renderDemoWarning?.();
  setTerminalLastUpdated();
}, 60000);


async function renderExecutiveSummary() {

  try {

    const res =
      await fetch(
        "/terminal-executive-summary-v1"
      )

    const data =
      await res.json()

    document.getElementById(
      "execObservations"
    ).innerText =
      data.observations

    document.getElementById(
      "execProviders"
    ).innerText =
      data.providers

    document.getElementById(
      "execGpuMarkets"
    ).innerText =
      data.gpu_models

    document.getElementById(
      "execForecast"
    ).innerText =
      data.forecast_readiness +
      "/100"

  } catch(err){

    console.error(err)

  }

}

renderExecutiveSummary()

async function renderFinalWidgets() {
  try {
    const [regimeRes, coverageRes, forecastRes] = await Promise.all([
      fetch("/terminal-market-regime-v1"),
      fetch("/terminal-live-coverage-v1"),
      fetch("/terminal-forecast-signal-v1")
    ]);

    const regime = await regimeRes.json();
    const coverage = await coverageRes.json();
    const forecast = await forecastRes.json();

    const marketRegime = document.getElementById("marketRegime");
    const marketRegimeReadout = document.getElementById("marketRegimeReadout");
    const liveCoverage = document.getElementById("liveCoverage");
    const liveCoverageReadout = document.getElementById("liveCoverageReadout");
    const forecastSignal = document.getElementById("forecastSignal");
    const forecastSignalReadout = document.getElementById("forecastSignalReadout");

    if (marketRegime) marketRegime.innerText = regime.regime || "...";
    if (marketRegimeReadout) {
      marketRegimeReadout.innerText =
        `${regime.observations} observations across ${regime.gpu_markets} GPU markets. Risk: ${regime.risk}.`;
    }

    if (liveCoverage) {
      liveCoverage.innerText =
        `${coverage.live_ready}/${coverage.total_connectors}`;
    }

    if (liveCoverageReadout) {
      liveCoverageReadout.innerText =
        `${coverage.total_normalized_offers} normalized offers collected in the latest connector cycle.`;
    }

    if (forecastSignal) forecastSignal.innerText = forecast.signal || "...";
    if (forecastSignalReadout) {
      forecastSignalReadout.innerText =
        `Forecast readiness: ${forecast.readiness}/100.`;
    }

  } catch (err) {
    console.error("Failed to render final widgets", err);
  }
}

renderFinalWidgets();

async function renderForecastIntelligence() {
  try {
    const res = await fetch("/terminal-forecast-intelligence-v1");
    const data = await res.json();

    const count = document.getElementById("forecastIntelCount");
    const shock = document.getElementById("forecastSupplyShock");
    const expansion = document.getElementById("forecastExpansionSignal");
    const backtest = document.getElementById("forecastBacktestSummary");

    if (count) count.innerText = data.forecast_count ?? "...";

    if (shock) {
      shock.innerText = data.supply_shock?.supply_shock_risk || "...";
    }

    if (expansion) {
      expansion.innerText = data.provider_expansion?.signal || "...";
    }

    if (backtest) {
      backtest.innerText = data.backtest?.summary || "No forecast backtest available.";
    }

  } catch (err) {
    console.error("Failed to render forecast intelligence", err);
  }
}

renderForecastIntelligence();

async function renderForecastOpportunities() {
  try {
    const res = await fetch("/terminal-forecast-intelligence-v1");
    const data = await res.json();

    const table = document.getElementById("forecastOpportunitiesTable");
    if (!table) return;

    const rows = data.top_opportunities || [];

    table.innerHTML = `
      <tr>
        <th>GPU</th>
        <th>Signal</th>
        <th>Opportunity Score</th>
        <th>Recent Price</th>
        <th>Historical Price</th>
      </tr>
      ${
        rows.length
          ? rows.map(r => `
            <tr>
              <td>${r.gpu_model}</td>
              <td>${r.signal}</td>
              <td>${r.opportunity_score}</td>
              <td>${r.recent_price}</td>
              <td>${r.historical_price}</td>
            </tr>
          `).join("")
          : `<tr><td colspan="5">No forecast opportunities detected yet</td></tr>`
      }
    `;

  } catch (err) {
    console.error("Failed to render forecast opportunities", err);
  }
}

renderForecastOpportunities();

async function renderCoverageActionPlan() {
  try {
    const res = await fetch("/terminal-coverage-action-plan-v1");
    const data = await res.json();

    const table = document.getElementById("coverageActionPlanTable");
    if (!table) return;

    const rows = data.actions || [];

    table.innerHTML = `
      <tr>
        <th>Priority</th>
        <th>Provider</th>
        <th>Current Mode</th>
        <th>Recommended Action</th>
      </tr>
      ${
        rows.length
          ? rows.map(r => `
            <tr>
              <td>${r.priority}</td>
              <td>${r.provider}</td>
              <td>${r.current_mode}</td>
              <td>${r.recommended_action}</td>
            </tr>
          `).join("")
          : `<tr><td colspan="4">All providers are live.</td></tr>`
      }
    `;
  } catch (err) {
    console.error("Failed to render coverage action plan", err);
  }
}

renderCoverageActionPlan();
