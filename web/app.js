const API = window.location.origin;

let marketShareChart = null;
let gpuTrendChart = null;
let activeApiKey = localStorage.getItem("airpct_api_key") || "";

Chart.defaults.color = "#94a3b8";
Chart.defaults.borderColor = "rgba(148, 163, 184, 0.1)";

async function getJson(path, apiKey = "") {
  const headers = {};
  if (apiKey) {
    headers["x-api-key"] = apiKey;
  }

  const res = await fetch(API + path, { headers });
  if (!res.ok) {
    throw new Error(`Request failed: ${path}`);
  }
  return res.json();
}

function value(data, key, fallback = "n/a") {
  if (!data || data[key] === undefined || data[key] === null || data[key] === "") {
    return fallback;
  }
  return data[key];
}

function number(value, digits = 2) {
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) {
    return "n/a";
  }
  return parsed.toFixed(digits).replace(/\.00$/, "");
}

function money(value) {
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) {
    return "n/a";
  }
  return `$${parsed.toFixed(2)}`;
}

function setText(id, text) {
  const el = document.getElementById(id);
  if (el) {
    el.textContent = text;
  }
}

function setTable(selector, rows, columns, emptyText = "No data") {
  const tbody = document.querySelector(`${selector} tbody`);
  if (!tbody) {
    return;
  }

  if (!rows || rows.length === 0) {
    tbody.innerHTML = `<tr><td colspan="${columns.length}" class="text-center text-slate-500 py-6">${emptyText}</td></tr>`;
    return;
  }

  tbody.innerHTML = rows.map((row) => `
    <tr>
      ${columns.map((column) => `<td>${column.render ? column.render(row) : value(row, column.key)}</td>`).join("")}
    </tr>
  `).join("");
}

function statusBadge(status) {
  const online = String(status).toLowerCase() === "online";
  const classes = online ? "status-operational" : "status-warning";
  return `<span class="status-indicator ${classes}">${online ? "online" : value({status}, "status")}</span>`;
}

function renderAlerts(alerts) {
  const el = document.getElementById("alertsList");
  if (!el) {
    return;
  }

  if (!alerts || alerts.length === 0) {
    el.innerHTML = `<div class="text-sm text-slate-500">No alerts</div>`;
    return;
  }

  el.innerHTML = alerts.map((alert) => {
    const severity = String(value(alert, "severity", "low")).toLowerCase();
    const color = severity === "high" ? "text-red-300 border-red-500/30 bg-red-500/10" :
      severity === "medium" ? "text-amber-300 border-amber-500/30 bg-amber-500/10" :
      "text-emerald-300 border-emerald-500/30 bg-emerald-500/10";

    return `
      <div class="rounded-lg border ${color} p-3">
        <div class="text-xs uppercase tracking-wider">${value(alert, "type", "alert")} / ${severity}</div>
        <div class="text-sm mt-1">${value(alert, "message", "No alert message")}</div>
      </div>
    `;
  }).join("");
}

function severityClasses(severity) {
  const normalized = String(severity || "low").toLowerCase();
  if (normalized === "high") {
    return "border-red-500/30 bg-red-500/10 text-red-200";
  }
  if (normalized === "medium") {
    return "border-amber-500/30 bg-amber-500/10 text-amber-200";
  }
  return "border-emerald-500/30 bg-emerald-500/10 text-emerald-200";
}

function renderSignals(signals) {
  const el = document.getElementById("signalsGrid");
  if (!el) {
    return;
  }

  if (!signals || signals.length === 0) {
    el.innerHTML = `<div class="text-sm text-slate-500">No decision signals available.</div>`;
    return;
  }

  el.innerHTML = signals.slice(0, 6).map((signal) => {
    const evidence = signal.evidence || {};
    const evidenceText = Object.entries(evidence)
      .slice(0, 3)
      .map(([key, val]) => `${key}: ${Array.isArray(val) ? val.join(", ") : val}`)
      .join(" | ");

    return `
      <div class="rounded-lg border ${severityClasses(signal.severity)} p-4">
        <div class="flex items-center justify-between gap-3">
          <div class="text-xs uppercase tracking-wider">${value(signal, "type", "signal")}</div>
          <div class="text-xs uppercase">${value(signal, "severity", "low")}</div>
        </div>
        <div class="text-sm font-semibold text-slate-100 mt-3">${value(signal, "title", "Untitled signal")}</div>
        <div class="text-sm text-slate-300 mt-2">${value(signal, "message", "")}</div>
        <div class="text-xs text-slate-400 mt-3">${evidenceText}</div>
      </div>
    `;
  }).join("");
}

function renderRecommendations(recommendations) {
  const el = document.getElementById("recommendationsGrid");
  if (!el) {
    return;
  }

  if (!recommendations || recommendations.length === 0) {
    el.innerHTML = `<div class="text-sm text-slate-500">No recommendations available.</div>`;
    return;
  }

  el.innerHTML = recommendations.slice(0, 6).map((item) => {
    const evidence = item.evidence || {};
    const evidenceText = Object.entries(evidence)
      .slice(0, 4)
      .map(([key, val]) => `${key}: ${Array.isArray(val) ? val.join(", ") : val}`)
      .join(" | ");

    return `
      <div class="rounded-lg border ${severityClasses(item.priority)} bg-slate-900/20 p-4">
        <div class="flex items-center justify-between gap-3">
          <div class="text-xs uppercase tracking-wider">${value(item, "action", "recommendation")}</div>
          <div class="text-xs uppercase">${value(item, "priority", "medium")}</div>
        </div>
        <div class="text-base font-semibold text-slate-100 mt-3">${value(item, "title", "Untitled recommendation")}</div>
        <div class="text-sm text-slate-300 mt-2">${value(item, "rationale", "")}</div>
        <div class="text-xs text-slate-400 mt-3">${evidenceText}</div>
      </div>
    `;
  }).join("");
}

function renderPaidLocked() {
  setText("briefHeadline", "Executive brief requires Pro access");
  setText("briefSummary", "Enter a Pro or Enterprise API key to unlock executive reporting and recommended actions.");
  renderRecommendations([]);
}

function renderCommercialLocked(message = "Enterprise key required.") {
  setText("commercialAccounts", "Locked");
  setText("commercialMrr", "Locked");
  setText("commercialArr", "Locked");
  setText("commercialUsage", "Locked");
  setText("forecastPipeline", "Locked");
  setText("forecastRisk", "Locked");
  setText("forecastExpectedMrr", "Locked");
  setText("forecastExpectedArr", "Locked");

  const el = document.getElementById("commercialAccountsList");
  if (el) {
    el.innerHTML = `<div class="text-sm text-slate-500">${message}</div>`;
  }

  const pipeline = document.getElementById("salesPipelineList");
  if (pipeline) {
    pipeline.innerHTML = `<div class="text-sm text-slate-500">${message}</div>`;
  }

  const admin = document.getElementById("customerAdminList");
  if (admin) {
    admin.innerHTML = `<div class="text-sm text-slate-500">${message}</div>`;
  }

  const audit = document.getElementById("auditLogList");
  if (audit) {
    audit.innerHTML = `<div class="text-sm text-slate-500">${message}</div>`;
  }

  const health = document.getElementById("accountHealthList");
  if (health) {
    health.innerHTML = `<div class="text-sm text-slate-500">${message}</div>`;
  }
}

function renderCommercialSnapshot(snapshot) {
  const summary = snapshot.summary || {};
  const accounts = snapshot.accounts || [];

  setText("commercialAccounts", number(summary.active_accounts, 0));
  setText("commercialMrr", money(summary.mrr_usd));
  setText("commercialArr", money(summary.annual_run_rate_usd));
  setText("commercialUsage", number(summary.usage_total, 0));

  const el = document.getElementById("commercialAccountsList");
  if (!el) {
    return;
  }

  el.innerHTML = accounts.map((account) => {
    const limits = account.limits || {};
    const plan = String(account.plan || "unknown").toUpperCase();
    const usage = account.usage || {};

    return `
      <div class="rounded-lg border border-slate-700 bg-slate-900/30 p-4">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
          <div>
            <div class="text-sm font-semibold text-slate-100">${value(account, "customer_name", "Unknown customer")}</div>
            <div class="text-xs text-slate-500 mt-1">${plan} / ${value(account, "upgrade_signal", "none")}</div>
          </div>
          <div class="text-sm text-slate-300">
            ${money(account.monthly_price_usd)} MRR / ${number(usage.total_calls, 0)} calls
          </div>
        </div>
        <div class="text-xs text-slate-500 mt-3">
          Daily ${number(limits.daily_calls, 0)}/${number((limits.limits || {}).requests_per_day, 0)}
          | Monthly ${number(limits.monthly_calls, 0)}/${number((limits.limits || {}).requests_per_month, 0)}
        </div>
      </div>
    `;
  }).join("");
}

function renderSalesPipeline(pipeline) {
  const el = document.getElementById("salesPipelineList");
  if (!el) {
    return;
  }

  const opportunities = pipeline.opportunities || [];
  if (opportunities.length === 0) {
    el.innerHTML = `<div class="text-sm text-slate-500">No sales opportunities yet.</div>`;
    return;
  }

  el.innerHTML = opportunities.map((item) => `
    <div class="rounded-lg border ${severityClasses(item.priority)} bg-slate-900/30 p-4">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
        <div>
          <div class="text-sm font-semibold text-slate-100">${value(item, "customer_name", "Unknown customer")}</div>
          <div class="text-xs text-slate-400 mt-1">${value(item, "opportunity_type", "opportunity")} / ${value(item, "priority", "medium")}</div>
        </div>
        <div class="text-sm text-slate-300">${money(item.estimated_mrr_lift_usd)} estimated MRR lift</div>
      </div>
      <div class="text-sm text-slate-200 mt-3">${value(item, "recommended_action", "")}</div>
      <div class="text-xs text-slate-500 mt-2">${value(item, "rationale", "")}</div>
    </div>
  `).join("");
}

function renderCustomerAdmin(snapshot) {
  const el = document.getElementById("customerAdminList");
  if (!el) {
    return;
  }

  const accounts = snapshot.accounts || [];
  if (accounts.length === 0) {
    el.innerHTML = `<div class="text-sm text-slate-500">No customer accounts.</div>`;
    return;
  }

  el.innerHTML = accounts.map((account) => {
    const usage = account.usage || {};
    const status = value(account, "status", "unknown");
    const statusClass = status === "active" ? "status-operational" : "status-warning";

    return `
      <div class="rounded-lg border border-slate-700 bg-slate-900/30 p-4">
        <div class="flex items-center justify-between gap-3">
          <div>
            <div class="text-sm font-semibold text-slate-100">${value(account, "customer_name", "Unknown customer")}</div>
            <div class="text-xs text-slate-500 mt-1">${value(account, "plan", "unknown")} / ${value(account, "api_key", "n/a")}</div>
          </div>
          <span class="status-indicator ${statusClass}">${status}</span>
        </div>
        <div class="text-xs text-slate-500 mt-3">${number(usage.total_calls, 0)} calls / ${money(account.monthly_price_usd)} MRR</div>
      </div>
    `;
  }).join("");
}

function renderAuditLog(payload) {
  const el = document.getElementById("auditLogList");
  if (!el) {
    return;
  }

  const events = payload.events || [];
  if (events.length === 0) {
    el.innerHTML = `<div class="text-sm text-slate-500">No audit events yet.</div>`;
    return;
  }

  el.innerHTML = events.slice(0, 8).map((event) => `
    <div class="rounded-lg border border-slate-700 bg-slate-900/30 p-4">
      <div class="flex items-center justify-between gap-3">
        <div class="text-sm font-semibold text-slate-100">${value(event, "action", "event")}</div>
        <div class="text-xs text-slate-500">${value(event, "status", "ok")}</div>
      </div>
      <div class="text-xs text-slate-500 mt-2">${value(event, "timestamp", "")}</div>
      <div class="text-xs text-slate-400 mt-2">Target: ${value(event, "target_api_key", "n/a")}</div>
    </div>
  `).join("");
}

function renderAccountHealth(payload) {
  const el = document.getElementById("accountHealthList");
  if (!el) {
    return;
  }

  const accounts = payload.accounts || [];
  if (accounts.length === 0) {
    el.innerHTML = `<div class="text-sm text-slate-500">No account health data.</div>`;
    return;
  }

  el.innerHTML = accounts.map((account) => {
    const health = value(account, "health", "watch");
    const color = health === "healthy" ? "border-emerald-500/30 text-emerald-200" :
      health === "watch" ? "border-amber-500/30 text-amber-200" :
      "border-red-500/30 text-red-200";

    return `
      <div class="rounded-lg border ${color} bg-slate-900/30 p-4">
        <div class="flex items-center justify-between gap-3">
          <div>
            <div class="text-sm font-semibold text-slate-100">${value(account, "customer_name", "Unknown customer")}</div>
            <div class="text-xs text-slate-500 mt-1">${value(account, "plan", "unknown")} / ${health}</div>
          </div>
          <div class="text-lg font-semibold">${number(account.health_score, 0)}</div>
        </div>
        <div class="text-xs text-slate-500 mt-3">${(account.reasons || []).join(" | ")}</div>
      </div>
    `;
  }).join("");
}

function renderRevenueForecast(payload) {
  const summary = payload.summary || {};

  setText("forecastPipeline", money(summary.pipeline_mrr_lift_usd));
  setText("forecastRisk", money(summary.at_risk_mrr_usd));
  setText("forecastExpectedMrr", money(summary.expected_mrr_usd));
  setText("forecastExpectedArr", money(summary.expected_arr_usd));
}

function setCustomerReportLink(enabled) {
  const link = document.getElementById("customerReportLink");
  if (link && (!enabled || !activeApiKey)) {
    link.classList.add("hidden");
    link.removeAttribute("href");
    return;
  }

  if (link) {
    link.href = "#";
    link.classList.remove("hidden");
  }

  const boardLink = document.getElementById("commercialBoardReportLink");
  if (!boardLink) {
    return;
  }

  if (!enabled || !activeApiKey) {
    boardLink.classList.add("hidden");
    boardLink.removeAttribute("href");
    return;
  }

  boardLink.href = "#";
  boardLink.classList.remove("hidden");
}

async function openCustomerReport() {
  if (!activeApiKey) {
    return;
  }

  const customerName = encodeURIComponent("AI Infrastructure Buyer");
  const res = await fetch(`${API}/v1/customer-report/html?customer_name=${customerName}`, {
    headers: { "x-api-key": activeApiKey }
  });

  if (!res.ok) {
    throw new Error("Customer report export failed");
  }

  const html = await res.text();
  const blob = new Blob([html], { type: "text/html" });
  window.open(URL.createObjectURL(blob), "_blank", "noopener,noreferrer");
}

async function openCommercialBoardReport() {
  if (!activeApiKey) {
    return;
  }

  const res = await fetch(`${API}/v1/commercial-board-report/html`, {
    headers: { "x-api-key": activeApiKey }
  });

  if (!res.ok) {
    throw new Error("Commercial board report export failed");
  }

  const html = await res.text();
  const blob = new Blob([html], { type: "text/html" });
  window.open(URL.createObjectURL(blob), "_blank", "noopener,noreferrer");
}

function updateAccessPanel(status, usage) {
  const plan = status && status.plan ? status.plan : "none";
  const authenticated = status && status.authenticated;

  setText("accessPlan", authenticated ? plan.toUpperCase() : "Not authenticated");
  setText(
    "accessSummary",
    authenticated
      ? `${(status.allowed_endpoints || []).length} endpoints available for this key.`
      : "Paid intelligence is locked until a valid key is saved."
  );

  const limits = (usage && usage.limits) || (status && status.limits) || null;
  const totalCalls = usage && Number.isFinite(Number(usage.total_calls)) ? usage.total_calls : 0;
  const topEndpoint = usage && usage.by_endpoint && usage.by_endpoint[0]
    ? `${usage.by_endpoint[0].endpoint}: ${usage.by_endpoint[0].calls}`
    : "No tracked paid calls yet";
  const limitText = limits && limits.limits
    ? `Today: ${limits.daily_calls}/${limits.limits.requests_per_day}, month: ${limits.monthly_calls}/${limits.limits.requests_per_month}.`
    : "";

  setText("usageSummary", authenticated ? `Usage: ${totalCalls} calls. ${limitText} ${topEndpoint}` : "");
  setCustomerReportLink(plan === "enterprise");
}

async function loadPaidData() {
  const input = document.getElementById("apiKeyInput");
  if (input && activeApiKey) {
    input.value = activeApiKey;
  }

  if (!activeApiKey) {
    updateAccessPanel({ authenticated: false, plan: null }, null);
    renderPaidLocked();
    return;
  }

  try {
    const status = await getJson("/v1/access-status", activeApiKey);
    let usage = null;

    try {
      usage = await getJson("/v1/usage-summary", activeApiKey);
    } catch (error) {
      usage = null;
    }

    updateAccessPanel(status, usage);

    if ((status.allowed_endpoints || []).includes("/v1/executive-brief")) {
      const brief = await getJson("/v1/executive-brief", activeApiKey);
      setText("briefHeadline", value(brief, "headline", "Executive brief unavailable"));
      setText("briefSummary", value(brief, "summary", ""));
    } else {
      renderPaidLocked();
    }

    if ((status.allowed_endpoints || []).includes("/v1/recommendations")) {
      const recommendations = await getJson("/v1/recommendations", activeApiKey);
      renderRecommendations(recommendations.recommendations || []);
    }

    if ((status.allowed_endpoints || []).includes("/v1/commercial-snapshot")) {
      const commercial = await getJson("/v1/commercial-snapshot", activeApiKey);
      renderCommercialSnapshot(commercial);
      const pipeline = await getJson("/v1/sales-pipeline", activeApiKey);
      renderSalesPipeline(pipeline);
      const customerAdmin = await getJson("/v1/customer-admin", activeApiKey);
      renderCustomerAdmin(customerAdmin);
      const accountHealth = await getJson("/v1/account-health", activeApiKey);
      renderAccountHealth(accountHealth);
      const revenueForecast = await getJson("/v1/revenue-forecast", activeApiKey);
      renderRevenueForecast(revenueForecast);
      const auditLog = await getJson("/v1/audit-log", activeApiKey);
      renderAuditLog(auditLog);
    } else {
      renderCommercialLocked("Enterprise key required for commercial metrics.");
    }
  } catch (error) {
    console.error(error);
    localStorage.removeItem("airpct_api_key");
    activeApiKey = "";
    updateAccessPanel({ authenticated: false, plan: null }, null);
    renderPaidLocked();
    renderCommercialLocked();
  }
}

function updateMarketShareChart(rows) {
  const ctx = document.getElementById("marketShareChart");
  if (!ctx) {
    return;
  }

  if (marketShareChart) {
    marketShareChart.destroy();
  }

  marketShareChart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: (rows || []).map((row) => value(row, "provider")),
      datasets: [{
        data: (rows || []).map((row) => Number(value(row, "market_share_pct", 0))),
        backgroundColor: ["#3b82f6", "#10b981", "#f59e0b", "#06b6d4", "#6366f1", "#94a3b8"],
        borderColor: "#1e293b",
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "bottom",
          labels: { color: "#cbd5e1", font: { size: 12 } }
        }
      }
    }
  });
}

function updateGpuTrendChart(watchlist) {
  const ctx = document.getElementById("gpuTrendChart");
  if (!ctx) {
    return;
  }

  if (gpuTrendChart) {
    gpuTrendChart.destroy();
  }

  const rows = (watchlist || []).slice(0, 8);

  gpuTrendChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: rows.map((row) => value(row, "gpu")),
      datasets: [{
        label: "Average price per hour",
        data: rows.map((row) => Number(value(row, "avg_price", 0))),
        backgroundColor: "rgba(59, 130, 246, 0.55)",
        borderColor: "#60a5fa",
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: "#cbd5e1" } }
      },
      scales: {
        y: { grid: { color: "rgba(148, 163, 184, 0.1)" }, ticks: { color: "#94a3b8" } },
        x: { grid: { display: false }, ticks: { color: "#94a3b8" } }
      }
    }
  });
}

function updateTimestamp() {
  const now = new Date();
  setText("lastRefresh", now.toISOString().split("T")[1].split(".")[0]);
  const status = document.getElementById("refreshStatus");
  if (status) {
    status.innerHTML = `Updated ${now.toLocaleTimeString()}`;
  }
}

function applySnapshot(snapshot) {
  const terminal = snapshot.terminal || {};
  const risk = snapshot.risk || {};
  const quality = snapshot.quality || {};

  setText("aiIndex", number(value(terminal, "ai_infrastructure_index"), 1));
  setText("gpuPrice", number(value(terminal, "gpu_price_index"), 4));
  setText("riskScore", number(value(risk, "terminal_risk_score"), 0));
  setText("gpuTrend", value(terminal, "gpu_price_trend"));
  setText("providerCount", String((snapshot.provider_health || []).filter((row) => row.status === "online").length));
  setText("quality", `${number(value(quality, "live_data_quality_score"), 0)}%`);
  setText("briefHeadline", value(snapshot.executive_brief, "headline", "Executive brief unavailable"));
  setText("briefSummary", value(snapshot.executive_brief, "summary", ""));

  updateMarketShareChart(snapshot.market_share || []);
  updateGpuTrendChart(snapshot.gpu_watchlist || []);
  renderSignals(snapshot.signals || []);
  renderPaidLocked();
  renderCommercialLocked();
  renderAlerts(snapshot.alerts || []);

  setTable("#providerHealth", snapshot.provider_health || [], [
    { key: "provider" },
    { key: "status", render: (row) => statusBadge(row.status) },
    { key: "rows", render: (row) => number(row.rows, 0) },
    { key: "freshness_hours", render: (row) => `${number(row.freshness_hours, 1)}h` },
    { key: "health_score", render: (row) => number(row.health_score, 0) }
  ]);

  setTable("#gpuTable", snapshot.gpu_rankings || [], [
    { key: "gpu" },
    { key: "offers", render: (row) => number(row.offers, 0) },
    { key: "avg_price", render: (row) => money(row.avg_price) },
    { key: "min_price", render: (row) => money(row.min_price) },
    { key: "max_price", render: (row) => money(row.max_price) }
  ]);

  setTable("#watchlistTable", snapshot.gpu_watchlist || [], [
    { key: "gpu" },
    { key: "category" },
    { key: "offers", render: (row) => number(row.offers, 0) },
    { key: "avg_price", render: (row) => money(row.avg_price) },
    { key: "range", render: (row) => `${money(row.min_price)} - ${money(row.max_price)}` }
  ]);

  setTable("#providerComparison", snapshot.provider_comparison || [], [
    { key: "provider" },
    { key: "offers", render: (row) => number(row.offers, 0) },
    { key: "gpu_types", render: (row) => number(row.gpu_types, 0) },
    { key: "avg_price", render: (row) => money(row.avg_price) }
  ]);

  updateTimestamp();
}

async function loadDashboardData() {
  try {
    const snapshot = await getJson("/v1/dashboard-snapshot");
    applySnapshot(snapshot);
    await loadPaidData();
  } catch (error) {
    console.error(error);
    const status = document.getElementById("refreshStatus");
    if (status) {
      status.textContent = "Data refresh failed";
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("apiKeyInput");
  const button = document.getElementById("saveApiKey");

  if (input && activeApiKey) {
    input.value = activeApiKey;
  }

  if (button && input) {
    button.addEventListener("click", () => {
      activeApiKey = input.value.trim();
      if (activeApiKey) {
        localStorage.setItem("airpct_api_key", activeApiKey);
      } else {
        localStorage.removeItem("airpct_api_key");
      }
      loadPaidData();
    });
  }

  const reportLink = document.getElementById("customerReportLink");
  if (reportLink) {
    reportLink.addEventListener("click", (event) => {
      event.preventDefault();
      openCustomerReport().catch((error) => {
        console.error(error);
        setText("accessSummary", "Customer report export failed for this key.");
      });
    });
  }

  const boardReportLink = document.getElementById("commercialBoardReportLink");
  if (boardReportLink) {
    boardReportLink.addEventListener("click", (event) => {
      event.preventDefault();
      openCommercialBoardReport().catch((error) => {
        console.error(error);
        setText("accessSummary", "Commercial board report export failed for this key.");
      });
    });
  }

  loadDashboardData();
  setInterval(loadDashboardData, 60000);
});
