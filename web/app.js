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

load("summary", "/terminal-summary");
load("providers", "/provider-reliability");
load("rankings", "/gpu-rankings");
load("brief", "/gpu-market-brief");
load("alerts", "/live-gpu-alerts");
