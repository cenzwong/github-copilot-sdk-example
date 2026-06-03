from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List

from copilot import CopilotClient

copilot_client = CopilotClient()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await copilot_client.start()
    try:
        yield
    finally:
        await copilot_client.stop()


app = FastAPI(lifespan=lifespan)


class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Dict[str, str]]
    temperature: float = 0.7


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    try:
        session = await copilot_client.create_session(model=request.model)
        last_message = request.messages[-1]["content"]
        copilot_response = await session.send_and_wait(last_message)

        response_text = ""
        if copilot_response is not None:
            response_data = getattr(copilot_response, "data", None)
            response_text = getattr(response_data, "content", "")

        return {
            "id": f"chatcmpl-{session.session_id}",
            "object": "chat.completion",
            "created": 1717415654,
            "model": request.model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response_text,
                    },
                    "finish_reason": "stop",
                }
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
