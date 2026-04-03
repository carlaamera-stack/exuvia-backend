@app.get("/test-claude")
def test_claude():
    if not ANTHROPIC_API_KEY:
        return {"response": "ERROR: ANTHROPIC_API_KEY no configurada"}

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json={
            "model": "claude-3-5-sonnet-latest",
            "max_tokens": 100,
            "messages": [
                {"role": "user", "content": "Hola. Responde solo: conexión exitosa."}
            ]
        },
        timeout=30
    )

    try:
        return response.json()
    except Exception as e:
        return {
            "response": f"ERROR JSON: {str(e)}",
            "status_code": response.status_code,
            "raw": response.text[:500]
        }
