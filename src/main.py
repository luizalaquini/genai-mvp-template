"""Entry point da API — FastAPI."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import anthropic

from src.core.agents.base_agent import BaseAgent
from src.core.guardrails.input_guard import InputValidationError

app = FastAPI(title="GenAI Agent MVP", version="0.1.0")
_client = anthropic.Anthropic()


class AgentRequest(BaseModel):
    task: str
    session_id: str | None = None


class AgentResponse(BaseModel):
    result: str
    session_id: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/agent/run", response_model=AgentResponse)
async def run_agent(req: AgentRequest):
    try:
        agent = BaseAgent(model_client=_client)
        result = agent.run(req.task)
        return AgentResponse(result=result, session_id=req.session_id or "new")
    except InputValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
