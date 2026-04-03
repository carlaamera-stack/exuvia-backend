from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests

app = FastAPI()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

SYSTEM = """Eres Aurora, núcleo conversacional de EXUVIA.
Acompañas, no impones. Tono humano, simple, cercano.
Responde en español. Sin listas. Sin sobreexplicar."""

class Message(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "EXUVIA activo"}

@app.get("/health")
def health():
    return {
        "api_key_set": bool(ANTHROPIC_API_KEY),
        "api_key_preview": ANTHROPIC_API_KEY[:12] + "..." if ANTHROPIC_API_KEY else "NO CONFIGURADA"
    }

@app.post("/api/aurora")
def aurora(msg: Message):
    if not ANTHROPIC_API_KEY:
        return {"response": "ERROR: ANTHROPIC_API_KEY no configurada en Railway"}

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json={
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 300,
            "system": SYSTEM,
            "messages": [{"role": "user", "content": msg.message}]
        }
    )

    data = response.json()

    if "error" in data:
        return {"response": f"ERROR Anthropic: {data['error']}"}

    try:
        reply = data["content"][0]["text"]
    except Exception as e:
        return {"response": f"ERROR parsing: {str(e)} | raw: {str(data)[:300]}"}

    return {"response": reply}
# update
