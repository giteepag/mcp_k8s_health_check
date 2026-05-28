from pydantic import BaseModel
from fastapi import APIRouter, Query
from app.mcp.router import route_action
from app.mcp.prompt_mapper import map_prompt_to_action

router = APIRouter()

class AskRequest(BaseModel):
    question: str


@router.get("/mcp")
def mcp(action: str = Query(...)):
    return route_action(action)

# ✅ NEW: Ask endpoint (AI-style)
@router.post("/ask")
def ask(req: AskRequest):
    action = map_prompt_to_action(req.question)
    result = route_action(action)

    return {
        "question": req.question,
        "action": action,
        "result": result
    }