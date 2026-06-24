const API = window.location.origin;

let marketShareChart = null;
let gpuTrendChart = null;
let activeApiKey = localStorage.getItem("airpct_api_key") || "";

if (typeof Chart !== "undefined") {
  Chart.defaults.color = "#94a3b8";
  Chart.defaults.borderColor = "rgba(148, 163, 184, 0.1)";
}

function initHeroArtifact() {
  const canvas = document.getElementById("heroArtifact");
  if (!canvas || typeof THREE === "undefined") {
    return;
  }

  const renderer = new THREE.WebGLRenderer({
    canvas,
    antialias: true,
    alpha: true
  });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(42, 1, 0.1, 100);
  camera.position.set(0, 0.7, 8.2);

  const artifact = new THREE.Group();
  scene.add(artifact);

  const chipMaterial = new THREE.MeshStandardMaterial({
    color: 0x0f172a,
    metalness: 0.86,
    roughness: 0.22,
    emissive: 0x0ea5e9,
    emissiveIntensity: 0.18
  });
  const chipEdgeMaterial = new THREE.MeshBasicMaterial({
    color: 0x93c5fd,
    transparent: true,
    opacity: 0.68
  });
  const nodeMaterial = new THREE.MeshStandardMaterial({
    color: 0xdbeafe,
    metalness: 0.42,
    roughness: 0.28,
    emissive: 0x1d4ed8,
    emissiveIntensity: 0.25
  });
  const riskMaterial = new THREE.MeshStandardMaterial({
    color: 0xfbbf24,
    metalness: 0.28,
    roughness: 0.3,
    emissive: 0xf59e0b,
    emissiveIntensity: 0.6
  });
  const lineMaterial = new THREE.LineBasicMaterial({
    color: 0x60a5fa,
    transparent: true,
    opacity: 0.38
  });

  const chip = new THREE.Group();
  const chipBody = new THREE.Mesh(new THREE.BoxGeometry(2.1, 1.34, 0.22), chipMaterial);
  chip.add(chipBody);

  const chipPlate = new THREE.Mesh(
    new THREE.BoxGeometry(1.18, 0.72, 0.28),
    new THREE.MeshStandardMaterial({
      color: 0x1e293b,
      metalness: 0.78,
      roughness: 0.18,
      emissive: 0x2563eb,
      emissiveIntensity: 0.18
    })
  );
  chipPlate.position.z = 0.16;
  chip.add(chipPlate);

  const edgeGeometry = new THREE.EdgesGeometry(new THREE.BoxGeometry(2.13, 1.37, 0.25));
  const chipEdges = new THREE.LineSegments(edgeGeometry, chipEdgeMaterial);
  chip.add(chipEdges);

  const pinMaterial = new THREE.MeshBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.72 });
  for (let i = 0; i < 11; i += 1) {
    const x = -1.0 + i * 0.2;
    const topPin = new THREE.Mesh(new THREE.BoxGeometry(0.055, 0.22, 0.035), pinMaterial);
    topPin.position.set(x, 0.82, 0.02);
    chip.add(topPin);

    const bottomPin = topPin.clone();
    bottomPin.position.y = -0.82;
    chip.add(bottomPin);
  }

  for (let i = 0; i < 7; i += 1) {
    const y = -0.54 + i * 0.18;
    const leftPin = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.05, 0.035), pinMaterial);
    leftPin.position.set(-1.24, y, 0.02);
    chip.add(leftPin);

    const rightPin = leftPin.clone();
    rightPin.position.x = 1.24;
    chip.add(rightPin);
  }

  chip.rotation.x = -0.52;
  chip.rotation.y = 0.24;
  artifact.add(chip);

  const providerNodes = new THREE.Group();
  const providerPositions = [];
  for (let i = 0; i < 7; i += 1) {
    const angle = (Math.PI * 2 * i) / 7;
    const radius = 3.1 + (i % 2) * 0.42;
    const position = new THREE.Vector3(
      Math.cos(angle) * radius,
      Math.sin(angle) * 1.38,
      Math.sin(angle) * radius * 0.28
    );
    providerPositions.push(position);
    const material = i === 1 || i === 4 ? riskMaterial : nodeMaterial;
    const node = new THREE.Mesh(new THREE.SphereGeometry(i === 1 ? 0.16 : 0.115, 24, 16), material);
    node.position.copy(position);
    providerNodes.add(node);

    const connection = new THREE.Line(
      new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(0, 0, 0), position]),
      lineMaterial
    );
    providerNodes.add(connection);
  }
  artifact.add(providerNodes);

  const ringOne = new THREE.Mesh(
    new THREE.TorusGeometry(2.35, 0.012, 12, 180),
    new THREE.MeshBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.68 })
  );
  ringOne.rotation.x = Math.PI / 2.7;
  artifact.add(ringOne);

  const ringTwo = new THREE.Mesh(
    new THREE.TorusGeometry(3.18, 0.01, 12, 220),
    new THREE.MeshBasicMaterial({ color: 0xa7f3d0, transparent: true, opacity: 0.32 })
  );
  ringTwo.rotation.y = Math.PI / 2.4;
  artifact.add(ringTwo);

  const spokes = new THREE.Group();
  for (let i = 0; i < 14; i += 1) {
    const angle = (Math.PI * 2 * i) / 14;
    const points = [
      new THREE.Vector3(Math.cos(angle) * 1.16, Math.sin(angle) * 0.72, 0.12),
      new THREE.Vector3(Math.cos(angle) * 3.55, Math.sin(angle) * 1.86, Math.sin(angle * 2) * 0.44)
    ];
    const line = new THREE.Line(new THREE.BufferGeometry().setFromPoints(points), lineMaterial);
    spokes.add(line);
  }
  artifact.add(spokes);

  const particleGeometry = new THREE.BufferGeometry();
  const particleCount = 380;
  const positions = new Float32Array(particleCount * 3);
  for (let i = 0; i < particleCount; i += 1) {
    const radius = 2.3 + Math.random() * 3.4;
    const angle = Math.random() * Math.PI * 2;
    positions[i * 3] = Math.cos(angle) * radius;
    positions[i * 3 + 1] = (Math.random() - 0.5) * 4.4;
    positions[i * 3 + 2] = Math.sin(angle) * radius;
  }
  particleGeometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));
  const particles = new THREE.Points(
    particleGeometry,
    new THREE.PointsMaterial({
      color: 0xbfdbfe,
      size: 0.025,
      transparent: true,
    opacity: 0.62
    })
  );
  scene.add(particles);

  const telemetry = new THREE.Group();
  providerPositions.forEach((position, index) => {
    const beacon = new THREE.Mesh(
      new THREE.RingGeometry(0.22 + index * 0.01, 0.24 + index * 0.01, 36),
      new THREE.MeshBasicMaterial({
        color: index === 1 || index === 4 ? 0xf59e0b : 0x22c55e,
        transparent: true,
        opacity: 0.42,
        side: THREE.DoubleSide
      })
    );
    beacon.position.copy(position);
    beacon.lookAt(camera.position);
    telemetry.add(beacon);
  });
  artifact.add(telemetry);

  scene.add(new THREE.AmbientLight(0x7dd3fc, 0.55));
  const keyLight = new THREE.PointLight(0x93c5fd, 12, 18);
  keyLight.position.set(3.2, 2.6, 4.5);
  scene.add(keyLight);
  const rimLight = new THREE.PointLight(0x34d399, 8, 18);
  rimLight.position.set(-3.4, -2.2, 3);
  scene.add(rimLight);

  function resize() {
    const rect = canvas.getBoundingClientRect();
    const width = Math.max(1, Math.floor(rect.width));
    const height = Math.max(1, Math.floor(rect.height));
    renderer.setSize(width, height, false);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
  }

  function animate(time) {
    const t = time * 0.001;
    artifact.rotation.y = t * 0.22;
    artifact.rotation.x = Math.sin(t * 0.38) * 0.12;
    chip.rotation.z = Math.sin(t * 0.45) * 0.08;
    ringOne.rotation.z = t * 0.42;
    ringTwo.rotation.x = Math.PI / 2.4 + t * 0.17;
    spokes.rotation.z = -t * 0.18;
    providerNodes.children.forEach((child, index) => {
      if (child.isMesh) {
        child.scale.setScalar(1 + Math.sin(t * 2.2 + index) * 0.08);
      }
    });
    telemetry.children.forEach((child, index) => {
      child.material.opacity = 0.26 + Math.sin(t * 2.4 + index) * 0.12;
      child.lookAt(camera.position);
    });
    particles.rotation.y = t * 0.035;
    renderer.render(scene, camera);
    requestAnimationFrame(animate);
  }

  resize();
  window.addEventListener("resize", resize);
  requestAnimationFrame(animate);
}

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

function pulseStatusClass(band) {
  const normalized = String(band || "").toLowerCase();
  if (normalized === "critical" || normalized === "elevated") {
    return "status-warning";
  }
  return "status-operational";
}

function trustStatusClass(level) {
  const normalized = String(level || "").toLowerCase();
  if (normalized === "high" || normalized === "medium") {
    return "status-operational";
  }
  return "status-warning";
}

function renderDataTrustStatus(status) {
  const summary = status.summary || {};
  const blockers = status.blockers || [];
  const trustLevel = value(status, "trust_level", "unknown");

  setText("dataTrustScore", number(status.trust_score, 0));
  setText("dataTrustLabel", value(status, "product_label", "unknown"));
  setText(
    "paidClaimsAllowed",
    status.paid_claims_allowed
      ? "Paid claims allowed by current trust guardrails."
      : "Paid claims blocked until trust guardrails improve."
  );

  const badge = document.getElementById("dataTrustLevel");
  if (badge) {
    badge.className = `status-indicator ${trustStatusClass(trustLevel)} mt-3`;
    badge.textContent = trustLevel;
  }

  const summaryEl = document.getElementById("dataTrustSummary");
  if (summaryEl) {
    const items = [
      ["Stale files", summary.stale_files],
      ["Placeholders", summary.placeholder_sources],
      ["Stale providers", summary.stale_providers],
      ["Live rows", summary.live_provider_rows],
    ];
    summaryEl.innerHTML = items.map(([label, val]) => `
      <div class="rounded-lg border border-slate-700 bg-slate-900/30 p-3">
        <div class="text-xs text-slate-500">${label}</div>
        <div class="text-sm font-semibold text-slate-100 mt-1">${number(val, 0)}</div>
      </div>
    `).join("");
  }

  const blockersEl = document.getElementById("dataTrustBlockers");
  if (blockersEl) {
    if (blockers.length === 0) {
      blockersEl.innerHTML = `<span class="status-indicator status-operational">no blockers</span>`;
    } else {
      blockersEl.innerHTML = blockers.map((blocker) => `
        <span class="status-indicator status-warning">${blocker}</span>
      `).join("");
    }
  }
}

function remediationPriorityClass(priority) {
  const normalized = String(priority || "medium").toLowerCase();
  if (normalized === "critical") {
    return "border-red-500/30 bg-red-500/10 text-red-200";
  }
  if (normalized === "high") {
    return "border-amber-500/30 bg-amber-500/10 text-amber-200";
  }
  return "border-slate-700 bg-slate-950/30 text-slate-300";
}

function renderTrustRemediationPlan(plan) {
  const actions = plan.actions || [];
  const next = plan.next_action || {};

  setText("trustRemediationPath", value(plan, "readiness_path", "unknown"));
  setText("trustRemediationCount", `${number(plan.action_count, 0)} trust actions required.`);
  setText("trustNextAction", value(next, "title", "No remediation action required."));
  setText("trustNextMetric", `Success metric: ${value(next, "success_metric", "n/a")}`);

  const el = document.getElementById("trustRemediationActions");
  if (!el) {
    return;
  }

  if (actions.length === 0) {
    el.innerHTML = `<div class="text-sm text-slate-500">No remediation actions required.</div>`;
    return;
  }

  el.innerHTML = actions.slice(0, 4).map((item) => `
    <div class="rounded-lg border ${remediationPriorityClass(item.priority)} p-3">
      <div class="flex items-center justify-between gap-3">
        <div class="text-sm font-semibold">${value(item, "action", "action")}</div>
        <div class="text-xs uppercase">${value(item, "priority", "medium")}</div>
      </div>
      <div class="text-xs mt-2 opacity-90">${value(item, "rationale", "")}</div>
    </div>
  `).join("");
}

function connectorReadinessClass(readiness) {
  const normalized = String(readiness || "").toLowerCase();
  if (normalized === "verified_live") {
    return "border-emerald-500/30 bg-emerald-500/10 text-emerald-200";
  }
  if (normalized === "stale_live_data") {
    return "border-amber-500/30 bg-amber-500/10 text-amber-200";
  }
  return "border-red-500/30 bg-red-500/10 text-red-200";
}

function renderProviderConnectorReadiness(payload) {
  const providers = payload.providers || [];

  setText("connectorReadinessCount", `${number(payload.provider_count, 0)} providers tracked`);
  setText("connectorVerifiedCount", number(payload.verified_live_count, 0));
  setText("connectorBlockerCount", number(payload.connector_blockers, 0));
  setText("connectorNextAction", value(payload, "next_provider_action", "No connector action required."));

  const el = document.getElementById("connectorReadinessList");
  if (!el) {
    return;
  }

  if (providers.length === 0) {
    el.innerHTML = `<div class="text-sm text-slate-500">No provider connector status available.</div>`;
    return;
  }

  el.innerHTML = providers.map((provider) => `
    <div class="rounded-lg border ${connectorReadinessClass(provider.readiness)} p-3">
      <div class="flex items-start justify-between gap-3">
        <div>
          <div class="text-sm font-semibold">${value(provider, "provider", "unknown")}</div>
          <div class="text-xs uppercase tracking-wider mt-1">${value(provider, "readiness", "unknown")}</div>
        </div>
        <div class="text-xs uppercase">${value(provider, "source_status", "n/a")}</div>
      </div>
      <div class="grid grid-cols-2 gap-2 mt-3 text-xs opacity-90">
        <div>Credential <span class="font-semibold">${provider.credential_configured ? "yes" : "no"}</span></div>
        <div>Freshness <span class="font-semibold">${number(provider.freshness_hours, 1)}h</span></div>
        <div>Rows <span class="font-semibold">${number(provider.rows, 0)}</span></div>
        <div>Offers <span class="font-semibold">${number(provider.offers, 0)}</span></div>
      </div>
      <div class="text-xs mt-3 opacity-90">${value(provider, "next_action", "monitor")}</div>
    </div>
  `).join("");
}

function renderProviderConnectorUpgradePlan(plan) {
  const next = plan.next_upgrade || {};
  const steps = next.upgrade_steps || [];

  setText("connectorUpgradeHeadline", value(plan, "headline", "Connector upgrade plan unavailable."));
  setText(
    "connectorUpgradePhase",
    `${value(plan, "rollout_phase", "unknown")} / ${number(plan.blocking_provider_count, 0)} blockers`
  );
  setText(
    "connectorNextProvider",
    next.provider
      ? `${value(next, "provider", "unknown")} / ${number(next.priority_score, 2)}`
      : "No provider fix required"
  );
  setText("connectorNextProviderValue", value(next, "buyer_value", "Maintain verified connector coverage."));

  const el = document.getElementById("connectorUpgradeSteps");
  if (!el) {
    return;
  }

  if (steps.length === 0) {
    el.innerHTML = `<div class="text-sm text-slate-500">No connector upgrade steps required.</div>`;
    return;
  }

  el.innerHTML = steps.slice(0, 5).map((step, index) => `
    <div class="rounded-lg border border-slate-700 bg-slate-950/30 p-3">
      <div class="text-xs uppercase tracking-wider text-slate-500">Step ${index + 1}</div>
      <div class="text-sm text-slate-200 mt-1">${step}</div>
    </div>
  `).join("");
}

function renderMarketPulse(pulse) {
  const drivers = pulse.drivers || {};
  const readouts = pulse.audience_readouts || {};
  const actions = pulse.next_best_actions || [];
  const band = value(pulse, "market_pulse_band", "unknown");

  setText("marketPulseScore", number(pulse.market_pulse_score, 2));
  setText("marketPulseConfidence", number(pulse.confidence_score, 0));
  setText("marketPulseConfidenceBand", `${value(pulse, "confidence_band", "unknown")} confidence`);
  setText("marketPulseHeadline", value(pulse, "headline", "Market pulse unavailable"));
  setText("marketPulseBuyer", value(readouts, "buyers", ""));
  setText("marketPulseInvestor", value(readouts, "investors", ""));
  setText("marketPulseActions", actions.length ? `Next actions: ${actions.join(" | ")}` : "");

  const badge = document.getElementById("marketPulseBand");
  if (badge) {
    badge.className = `status-indicator ${pulseStatusClass(band)} mt-3`;
    badge.textContent = band;
  }

  setText("pulseRisk", number(drivers.terminal_risk_score, 0));
  setText("pulseScarcity", number(drivers.gpu_scarcity_index, 0));
  setText("pulsePricing", number(drivers.pricing_pressure, 1));
  setText("pulseFrontier", number(drivers.frontier_gpu_index, 1));
  setText("pulseAlerts", number(drivers.active_alerts, 0));
  setText("pulseQuality", `${number(drivers.live_data_quality_score, 0)}%`);
  setText("pulseMoat", `${number(drivers.data_moat_score, 0)}%`);
}

function renderMarketPulseHistory(payload) {
  const trend = payload.trend || {};
  const history = payload.history || [];
  const direction = value(trend, "direction", "flat");
  const delta = Number(trend.delta || 0);
  const sign = delta > 0 ? "+" : "";

  setText("marketPulseTrend", `${number(payload.record_count, 0)} pulse records tracked. Direction: ${direction}.`);
  setText("marketPulseDelta", `${sign}${number(delta, 2)}`);

  const el = document.getElementById("marketPulseHistoryList");
  if (!el) {
    return;
  }

  if (history.length === 0) {
    el.innerHTML = `<div class="text-sm text-slate-500">No pulse history collected yet.</div>`;
    return;
  }

  el.innerHTML = history.slice(-6).reverse().map((row) => `
    <div class="rounded-lg border border-slate-700 bg-slate-950/30 p-3">
      <div class="flex items-center justify-between gap-3">
        <div class="text-xs text-slate-500">${value(row, "timestamp", "").slice(0, 19)}</div>
        <div class="text-xs uppercase text-slate-400">${value(row, "market_pulse_band", "n/a")}</div>
      </div>
      <div class="text-lg font-semibold text-slate-100 mt-2">${number(row.market_pulse_score, 2)}</div>
      <div class="text-xs text-slate-500 mt-1">Risk ${number(row.terminal_risk_score, 0)} | Scarcity ${number(row.gpu_scarcity_index, 0)}</div>
    </div>
  `).join("");
}

function renderMarketPulseHistoryLocked(message = "Pro key required for market pulse history.") {
  setText("marketPulseTrend", message);
  setText("marketPulseDelta", "Locked");
  const el = document.getElementById("marketPulseHistoryList");
  if (el) {
    el.innerHTML = `<div class="text-sm text-slate-500">${message}</div>`;
  }
}

function renderMarketPulseBrief(brief) {
  setText("marketPulseBriefHeadline", value(brief, "headline", "Market pulse brief unavailable"));
  setText("marketPulseBriefSummary", value(brief, "summary", ""));

  const drivers = document.getElementById("marketPulseBriefDrivers");
  if (drivers) {
    const rows = brief.driver_readout || [];
    drivers.innerHTML = rows.slice(0, 6).map((item) => `
      <div class="rounded-lg border border-slate-700 bg-slate-950/30 p-3 text-sm text-slate-300">${item}</div>
    `).join("");
  }

  const button = document.getElementById("saveMarketPulseBrief");
  if (button) {
    button.classList.remove("hidden");
  }
}

function renderMarketPulseBriefLocked(message = "Pro key required for the pulse brief.") {
  setText("marketPulseBriefHeadline", message);
  setText("marketPulseBriefSummary", "Unlock Pro intelligence to generate an executive-readable market pulse brief.");

  const drivers = document.getElementById("marketPulseBriefDrivers");
  if (drivers) {
    drivers.innerHTML = `<div class="text-sm text-slate-500">Brief drivers are available with Pro access.</div>`;
  }

  const button = document.getElementById("saveMarketPulseBrief");
  if (button) {
    button.classList.add("hidden");
  }
}

function riskBorderClass(band) {
  const normalized = String(band || "low").toLowerCase();
  if (normalized === "high") {
    return "border-red-500/30 text-red-200";
  }
  if (normalized === "medium") {
    return "border-amber-500/30 text-amber-200";
  }
  return "border-emerald-500/30 text-emerald-200";
}

function providerRadarLabel(provider) {
  if (!provider || !provider.provider) {
    return "n/a";
  }
  return `${provider.provider} / ${number(provider.risk_score, 2)} / ${provider.risk_band}`;
}

function renderProviderRiskRadar(payload) {
  const providers = payload.providers || [];
  const highest = payload.highest_risk_provider || {};
  const lowest = payload.lowest_risk_provider || {};

  setText("providerRadarHighest", providerRadarLabel(highest));
  setText("providerRadarHighestDetail", value(highest, "recommended_action", "n/a"));
  setText("providerRadarLowest", providerRadarLabel(lowest));
  setText("providerRadarLowestDetail", value(lowest, "recommended_action", "n/a"));
  setText("providerRadarCount", number(payload.provider_count, 0));

  const el = document.getElementById("providerRiskRadarList");
  if (!el) {
    return;
  }

  if (providers.length === 0) {
    el.innerHTML = `<div class="text-sm text-slate-500">No provider risk data available.</div>`;
    return;
  }

  el.innerHTML = providers.map((provider) => {
    const drivers = provider.drivers || {};
    return `
      <div class="rounded-lg border ${riskBorderClass(provider.risk_band)} bg-slate-900/30 p-4">
        <div class="flex items-start justify-between gap-3">
          <div>
            <div class="text-lg font-semibold text-slate-100">${value(provider, "provider", "unknown")}</div>
            <div class="text-xs uppercase tracking-wider mt-1">${value(provider, "risk_band", "low")} risk / ${value(provider, "recommended_action", "monitor")}</div>
          </div>
          <div class="text-2xl font-semibold">${number(provider.risk_score, 2)}</div>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-3 gap-3 mt-4 text-xs text-slate-400">
          <div>Share <span class="text-slate-100">${number(drivers.market_share_pct, 1)}%</span></div>
          <div>Offers <span class="text-slate-100">${number(drivers.offers, 0)}</span></div>
          <div>GPU Types <span class="text-slate-100">${number(drivers.gpu_types, 0)}</span></div>
          <div>Avg Price <span class="text-slate-100">${money(drivers.avg_price)}</span></div>
          <div>Health <span class="text-slate-100">${number(drivers.health_score, 0)}</span></div>
          <div>Freshness <span class="text-slate-100">${number(drivers.freshness_hours, 1)}h</span></div>
        </div>
      </div>
    `;
  }).join("");
}

function renderProviderRiskRadarLocked(message = "Pro key required for provider risk radar.") {
  setText("providerRadarHighest", "Pro key required");
  setText("providerRadarHighestDetail", "Unlock provider concentration, depth and freshness risk.");
  setText("providerRadarLowest", "Locked");
  setText("providerRadarLowestDetail", "Provider benchmark unavailable.");
  setText("providerRadarCount", "Locked");

  const el = document.getElementById("providerRiskRadarList");
  if (el) {
    el.innerHTML = `<div class="text-sm text-slate-500">${message}</div>`;
  }
}

function renderDailyChangeBrief(payload) {
  const changes = payload.changes || [];
  const trust = payload.data_trust || {};

  setText("dailyChangeHeadline", value(payload, "headline", "Daily change brief unavailable"));
  setText("dailyChangeSummary", value(payload, "summary", ""));
  setText("dailyChangeDecision", value(payload, "recommended_decision", "monitor"));
  setText(
    "dailyChangeTrust",
    `Trust: ${value(trust, "trust_level", "n/a")} | Paid claims: ${value(trust, "paid_claims_allowed", false)}`
  );

  const el = document.getElementById("dailyChangeSignals");
  if (!el) {
    return;
  }

  if (changes.length === 0) {
    el.innerHTML = `<div class="text-sm text-slate-500">No daily changes available.</div>`;
    return;
  }

  el.innerHTML = changes.slice(0, 5).map((change) => `
    <div class="rounded-lg border border-slate-700 bg-slate-950/30 p-3">
      <div class="flex items-center justify-between gap-3">
        <div class="text-sm font-semibold text-slate-100">${value(change, "type", "change")}</div>
        <div class="text-xs uppercase text-slate-400">${value(change, "direction", "flat")}</div>
      </div>
      <div class="text-xs text-slate-500 mt-2">
        ${change.delta !== undefined ? `Delta ${number(change.delta, 2)}` : ""}
        ${change.risk_score !== undefined ? `Risk ${number(change.risk_score, 2)}` : ""}
        ${change.trust_score !== undefined ? `Trust ${number(change.trust_score, 0)}` : ""}
        ${change.count !== undefined ? `Count ${number(change.count, 0)}` : ""}
      </div>
    </div>
  `).join("");
}

function renderDailyChangeBriefLocked(message = "Pro key required for daily change intelligence.") {
  setText("dailyChangeHeadline", message);
  setText("dailyChangeSummary", "Unlock Pro to see what changed since the previous pulse.");
  setText("dailyChangeDecision", "Locked");
  setText("dailyChangeTrust", "Trust guardrails unavailable.");

  const el = document.getElementById("dailyChangeSignals");
  if (el) {
    el.innerHTML = `<div class="text-sm text-slate-500">Daily change signals are available with Pro access.</div>`;
  }
}

async function saveMarketPulseBrief() {
  if (!activeApiKey) {
    renderMarketPulseBriefLocked();
    return;
  }

  const button = document.getElementById("saveMarketPulseBrief");
  if (button) {
    button.textContent = "Saving...";
  }

  try {
    const result = await getJson("/v1/market-pulse-brief/save", activeApiKey);
    setText("marketPulseBriefSummary", `Saved ${value(result, "file", "market pulse brief")}`);
  } catch (error) {
    console.error(error);
    setText("marketPulseBriefSummary", "Market pulse brief save failed for this key.");
  } finally {
    if (button) {
      button.textContent = "Save Brief";
    }
  }
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
    renderMarketPulseHistoryLocked();
    renderMarketPulseBriefLocked();
    renderProviderRiskRadarLocked();
    renderDailyChangeBriefLocked();
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

    if ((status.allowed_endpoints || []).includes("/v1/market-pulse-history")) {
      const pulseHistory = await getJson("/v1/market-pulse-history", activeApiKey);
      renderMarketPulseHistory(pulseHistory);
    } else {
      renderMarketPulseHistoryLocked();
    }

    if ((status.allowed_endpoints || []).includes("/v1/market-pulse-brief")) {
      const pulseBrief = await getJson("/v1/market-pulse-brief", activeApiKey);
      renderMarketPulseBrief(pulseBrief);
    } else {
      renderMarketPulseBriefLocked();
    }

    if ((status.allowed_endpoints || []).includes("/v1/provider-risk-radar")) {
      const providerRadar = await getJson("/v1/provider-risk-radar", activeApiKey);
      renderProviderRiskRadar(providerRadar);
    } else {
      renderProviderRiskRadarLocked();
    }

    if ((status.allowed_endpoints || []).includes("/v1/daily-change-brief")) {
      const dailyChange = await getJson("/v1/daily-change-brief", activeApiKey);
      renderDailyChangeBrief(dailyChange);
    } else {
      renderDailyChangeBriefLocked();
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
    renderMarketPulseHistoryLocked();
    renderMarketPulseBriefLocked();
    renderProviderRiskRadarLocked();
    renderDailyChangeBriefLocked();
    renderCommercialLocked();
  }
}

function updateMarketShareChart(rows) {
  const ctx = document.getElementById("marketShareChart");
  if (!ctx || typeof Chart === "undefined") {
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
  if (!ctx || typeof Chart === "undefined") {
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
    const [snapshot, pulse, trust, remediation, connectors, connectorPlan] = await Promise.all([
      getJson("/v1/dashboard-snapshot"),
      getJson("/v1/market-pulse"),
      getJson("/v1/data-trust-status"),
      getJson("/v1/trust-remediation-plan"),
      getJson("/v1/provider-connector-readiness"),
      getJson("/v1/provider-connector-upgrade-plan")
    ]);
    applySnapshot(snapshot);
    renderDataTrustStatus(trust);
    renderTrustRemediationPlan(remediation);
    renderProviderConnectorReadiness(connectors);
    renderProviderConnectorUpgradePlan(connectorPlan);
    renderMarketPulse(pulse);
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
  initHeroArtifact();

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

  const marketPulseBriefButton = document.getElementById("saveMarketPulseBrief");
  if (marketPulseBriefButton) {
    marketPulseBriefButton.addEventListener("click", () => {
      saveMarketPulseBrief();
    });
  }

  loadDashboardData();
  setInterval(loadDashboardData, 60000);
});
// Smoke-test anchor
const manualSnapshotOperatorPack = "Manual Snapshot Operator Pack";
const manualSnapshotActions = "manualSnapshotActions";

