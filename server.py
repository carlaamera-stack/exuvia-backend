from fastapi import FastAPI
from pydantic import BaseModel
import os
import logging
from anthropic import Anthropic

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

SYSTEM = """Eres Aurora, núcleo conversacional de EXUVIA.
Tu función es acompañar, responder con claridad, no imponer, no sobreexplicar.
Tono humano, cercano, simple. Responde en español."""

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

class Message(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "EXUVIA backend activo"}

@app.get("/health")
def health():
    key = os.getenv("ANTHROPIC_API_KEY", "")
    return {
        "status": "ok",
        "api_key_set": bool(key),
        "api_key_prefix": key[:8] + "..." if key else "NOT SET"
    }

@app.post("/api/aurora")
def aurora(msg: Message):
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            system=SYSTEM,
            messages=[{"role": "user", "content": msg.message}]
        )
        return {"response": response.content[0].text}

    except Exception as e:
        logger.error(f"Anthropic error: {e}")
        return {"response": f"ERROR: {str(e)}"}
# update
