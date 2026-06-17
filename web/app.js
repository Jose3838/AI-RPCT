const API="https://ai-rpct-production.up.railway.app";

async function loadDashboard(){
  const summary=await fetch(API+"/terminal-summary").then(r=>r.json());
  const risk=await fetch(API+"/terminal-risk").then(r=>r.json());
  const market=await fetch(API+"/live-provider-market-share").then(r=>r.json());
  const history=await fetch(API+"/gpu-price-history").then(r=>r.json());

  document.getElementById("aiIndex").innerText=summary[0].ai_infrastructure_index;
  document.getElementById("gpuPrice").innerText=summary[0].gpu_price_index;
  document.getElementById("riskScore").innerText=risk[0].terminal_risk_score;
  document.getElementById("providerCount").innerText=market.length;

  buildPriceChart(history);
  buildMarketShareChart(market);
}

function buildPriceChart(history){
  new Chart(document.getElementById("priceChart"),{
    type:"line",
    data:{
      labels:history.map(x=>x.timestamp),
      datasets:[{
        label:"GPU Price Index",
        data:history.map(x=>x.gpu_price_index)
      }]
    }
  });
}

function buildMarketShareChart(data){
  new Chart(document.getElementById("marketShareChart"),{
    type:"doughnut",
    data:{
      labels:data.map(x=>x.provider),
      datasets:[{
        data:data.map(x=>x.market_share_pct)
      }]
    }
  });
}

loadDashboard();
