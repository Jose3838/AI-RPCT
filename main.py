from fastapi import FastAPI
from api.routes import router
from api.auth_routes import router as auth_router

app = FastAPI(
    title="AI-RPCT",
    version="16.3"
)

app.include_router(router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {
        "service": "AI-RPCT",
        "status": "online",
        "version": "16.3"
    }
