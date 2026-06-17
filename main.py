from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.routes import router
from api.auth_routes import router as auth_router

app = FastAPI(
    title="AI-RPCT",
    version="63.0"
)

app.include_router(router)
app.include_router(auth_router)

app.mount("/web", StaticFiles(directory="web", html=True), name="web")

@app.get("/")
def root():
    return {
        "service": "AI-RPCT",
        "status": "online",
        "version": "63.0",
        "terminal": "/web"
    }
