from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests

app = FastAPI()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")


class Message(BaseModel):
    message: str


@app.get("/")
def root():
    return {"status": "EXUVIA backend activo"}


@app.post("/api/aurora")
def aurora(msg: Message):
    user_message = msg.message

    prompt = f"""
Eres Aurora, núcleo conversacional inicial de EXUVIA.

Tu función:
- acompañar
- responder con claridad
- no imponer
- no sobreexplicar
- mantener un tono humano, cercano y simple

Usuario dice:
{user_message}
"""

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json={
            "model": "claude-3-5-sonnet-latest",
            "max_tokens": 300,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )

    data = response.json()

    try:
        reply = data["content"][0]["text"]
    except Exception:
        reply = "No pude responder ahora."

    return {
        "response": reply
    } 
