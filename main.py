from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="AI-RPCT",
    version="7.0"
)

app.include_router(router)

@app.get("/")
def root():
    return {
        "service": "AI-RPCT",
        "status": "online"
    }
