from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from bank.payment_processing import verify_payment


app = FastAPI()


class VerificationRequest(BaseModel):
    id: str
    data_hash: str
    value: int


@app.get("/test")
def test_endpoint():
    return {"message": "Bank server is running"}    


@app.post("/verify_payment")
def verify_pin(data: VerificationRequest):
    is_authorized = verify_payment(data.id, data.data_hash, data.value)
    return {"authorized": is_authorized}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
