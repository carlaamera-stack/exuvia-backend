from fastapi import FastAPI
from pydantic import BaseModel
import os
from anthropic import Anthropic

app = FastAPI()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = Anthropic(api_key=ANTHROPIC_API_KEY)


class Message(BaseModel):
    message: str


@app.get("/")
def root():
    return {"status": "EXUVIA backend activo"}


@app.post("/api/aurora")
def aurora(msg: Message):
    try:
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

        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        reply = response.content[0].text

        return {
            "response": reply
        }

    except Exception as e:
        return {
            "response": str(e)
        }
# redeploy
