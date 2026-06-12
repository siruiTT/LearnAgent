from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI, AsyncOpenAI
import json
import asyncio

app = FastAPI()

# 你的配置
OPENAI_API_BASE = "https://api.moonshot.cn/v1"
OPENAI_CHAT_API_KEY = "sk-mQnOyBvhUF3BqfHv2IUogEGu3QS1oPr2tKmmeEsmDz3tWMnD"
OPENAI_CHAT_MODEL = "kimi-k2.6"


class ChatRequest(BaseModel):
    messages: list
    stream: bool = True


@app.post("/chat")
async def chat(request: ChatRequest):
    if not request.stream:
        client = AsyncOpenAI(api_key=OPENAI_CHAT_API_KEY, base_url=OPENAI_API_BASE)
        response = await client.chat.completions.create(
            model=OPENAI_CHAT_MODEL,
            messages=request.messages
        )
        return {"content": response.choices[0].message.content}

    async def generate_stream():
        client = AsyncOpenAI(api_key=OPENAI_CHAT_API_KEY, base_url=OPENAI_API_BASE)

        # stream=True + async client = 异步流式迭代
        response = await client.chat.completions.create(
            model=OPENAI_CHAT_MODEL,
            messages=request.messages,
            stream=True
        )

        # async for 遍历异步流
        async for chunk in response:
            yield f"data: {json.dumps(chunk.model_dump())}\n\n"

    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream"
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)