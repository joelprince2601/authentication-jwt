from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import jwt
import time

app = FastAPI()

SECRET_KEY = "super_secret_key_123456789"  # Shared secret key

class PayloadModel(BaseModel):
    payload: str
    token: str

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <body>
            <h1>Welcome to the Payload Receiver</h1>
            <form action="/receive-payload" method="get">
                <label for="payload">Payload:</label>
                <input type="text" id="payload" name="payload" required><br><br>
                <label for="token">Token:</label>
                <input type="text" id="token" name="token" required><br><br>
                <input type="submit" value="Send Payload">
            </form>
            <p>Or use this test link:</p>
            <a href="/receive-payload?payload=test&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0In0.UAm6VFLE0BqiVeL1qR9srzABKYbdXOeRomcljkOeDMA">Test Receive Payload</a>
        </body>
    </html>
    """

@app.get("/receive-payload")
def receive_payload_get(payload: str = Query(None), token: str = Query(None)):
    if payload is None or token is None:
        return {"message": "Please provide both 'payload' and 'token' query parameters."}
    return process_payload(payload, token)

@app.post("/receive-payload")
def receive_payload_post(data: PayloadModel):
    return process_payload(data.payload, data.token)

def process_payload(payload: str, token: str):
    try:
        time.sleep(2)
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {
            "message": "Payload received with token",
            "payload": payload,
            "decoded_token": decoded_token
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
