from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.routes import router
from api.auth_routes import router as auth_router
from api.billing_routes import router as billing_router
from api.organization_routes import router as organization_router
from api.forecast_routes import router as forecast_router
from api.provider_routes import router as provider_router
from api.live_data_routes import router as live_data_router
from api.market_routes import router as market_router
from api.enterprise_routes import router as enterprise_router
from api.executive_intelligence_routes import router as executive_intelligence_router
from api.entitlement_routes import router as entitlement_router
from api.intelligence_routes import router as intelligence_router
from api.dashboard_routes import router as dashboard_router

app = FastAPI(
    title="AI-RPCT",
    version="63.0"
)

app.include_router(router)
app.include_router(auth_router)
app.include_router(billing_router)
app.include_router(organization_router)
app.include_router(forecast_router)
app.include_router(provider_router)
app.include_router(live_data_router)
app.include_router(market_router)
app.include_router(enterprise_router)
app.include_router(executive_intelligence_router)
app.include_router(entitlement_router)
app.include_router(intelligence_router)
app.include_router(dashboard_router)

app.mount("/web", StaticFiles(directory="web", html=True), name="web")

@app.get("/")
def root():
    return {
        "service": "AI-RPCT",
        "status": "online",
        "version": "63.0",
        "terminal": "/web"
    }
