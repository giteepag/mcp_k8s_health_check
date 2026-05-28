from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="MCP K8s Health Platform")

app.include_router(router)