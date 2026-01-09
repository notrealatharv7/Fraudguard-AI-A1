from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Explanation AI Service",
    description="Generates explanations for fraud predictions.",
    version="1.0.0"
)

class PredictionDetails(BaseModel):
    transactionAmount: float
    transactionAmountDeviation: float
    timeAnomaly: float
    locationDistance: float
    merchantNovelty: float
    transactionFrequency: float
    isFraud: bool
    riskScore: float

class ExplanationResponse(BaseModel):
    explanation: str

@app.post("/explain", response_model=ExplanationResponse)
async def get_explanation(details: PredictionDetails):
    explanation = create_prompt(details)
    return ExplanationResponse(explanation=explanation)

def create_prompt(details: PredictionDetails) -> str:
    status = "fraudulent" if details.isFraud else "legitimate"

    factors = []
    if details.transactionAmountDeviation > 0.5:
        factors.append("high amount deviation")
    if details.locationDistance > 20:
        factors.append("unusual location")
    if details.merchantNovelty > 0.7:
        factors.append("new merchant")
    if details.timeAnomaly > 0.6:
        factors.append("unusual time")

    factors_text = ", ".join(factors) if factors else "normal transaction patterns"

    return (
        f"This transaction is classified as {status} with a risk score of "
        f"{details.riskScore*100:.0f}%. "
        f"The decision is based on {factors_text}."
    )

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
