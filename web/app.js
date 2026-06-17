const API = "https://ai-rpct-production.up.railway.app";

async function load(id, path) {
  const el = document.getElementById(id);

  try {
    const res = await fetch(API + path);
    const data = await res.json();
    el.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    el.textContent = "Failed to load " + path;
  }
}

async function loadKpis() {
  try {
    const res = await fetch(API + "/terminal-kpis");
    const data = await res.json();

    document.getElementById("kpi-ai").textContent = data.ai_infrastructure_index;
    document.getElementById("kpi-price").textContent = data.gpu_price_index;
    document.getElementById("kpi-trend").textContent = data.gpu_price_trend;
    document.getElementById("kpi-providers").textContent = data.live_providers;
    document.getElementById("kpi-vast").textContent = data.vast_offers;
    document.getElementById("kpi-runpod").textContent = data.runpod_gpu_types;
  } catch (e) {
    console.log(e);
  }
}

loadKpis();
load("summary", "/terminal-summary");
load("providers", "/provider-reliability");
load("rankings", "/gpu-rankings");
load("brief", "/gpu-market-brief");
load("alerts", "/live-gpu-alerts");

setInterval(() => {
  loadKpis();
  load("summary", "/terminal-summary");
  load("providers", "/provider-reliability");
  load("rankings", "/gpu-rankings");
  load("brief", "/gpu-market-brief");
  load("alerts", "/live-gpu-alerts");
}, 60000);
