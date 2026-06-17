const API="https://ai-rpct-production.up.railway.app";

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

  new Chart(document.getElementById("marketShareChart"),{
    type:"doughnut",
    data:{
      labels:snap.market_share.map(x=>x.provider),
      datasets:[{data:snap.market_share.map(x=>x.market_share_pct)}]
    }
  });

  table(
    document.getElementById("providerHealth"),
    snap.provider_health,
    ["provider","status","rows","freshness_hours","health_score"]
  );

  table(
    document.getElementById("gpuTable"),
    snap.gpu_rankings,
    ["gpu","offers","avg_price","min_price","max_price"]
  );
}

load();
setInterval(load,60000);
