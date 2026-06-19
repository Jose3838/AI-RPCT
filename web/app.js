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
