"""
Temporary sample FastAPI app with dummy return to test server startup.
(Safe to delete after testing.)
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Sample Dummy Test API", version="0.1.0")


class DummyRequest(BaseModel):
    amount: float = 50000.0
    type: str = "TRANSFER"


@app.get("/")
def root():
    return {"status": "ONLINE", "message": "Sample FastAPI is working!"}


@app.get("/health")
def health():
    return {"status": "healthy", "mode": "dummy"}


@app.post("/test")
def test_endpoint(payload: DummyRequest):
    return {
        "status": "success",
        "received_amount": payload.amount,
        "received_type": payload.type,
        "dummy_risk_score": 0.12,
        "dummy_action": "ALLOW",
    }


if __name__ == "__main__":
    import uvicorn

    print("Starting Sample Dummy API on http://127.0.0.1:8001/docs ...", flush=True)
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="info")
