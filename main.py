# main.py — Sentinel AI FastAPI Backend

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import investigate
import uvicorn

# ─────────────────────────────────────────
# Initialize FastAPI App
# ─────────────────────────────────────────
app = FastAPI(
    title="Sentinel AI — Fraud Investigation Agent",
    description="AI-powered fraud investigation for fintech compliance teams",
    version="1.0.0"
)

# ─────────────────────────────────────────
# Request Model
# ─────────────────────────────────────────
class InvestigationRequest(BaseModel):
    transaction_id: str

# ─────────────────────────────────────────
# Response Model
# ─────────────────────────────────────────
class InvestigationResponse(BaseModel):
    transaction_id: str
    status: str
    report: str

# ─────────────────────────────────────────
# Route 1 — Health Check
# ─────────────────────────────────────────
@app.get("/")
def home():
    return {
        "agent"  : "Sentinel AI",
        "status" : "Running ✅",
        "version": "1.0.0"
    }

# ─────────────────────────────────────────
# Route 2 — Investigate Transaction
# ─────────────────────────────────────────
@app.post("/investigate", response_model=InvestigationResponse)
def investigate_transaction(request: InvestigationRequest):
    """
    Accepts a transaction ID and returns
    a full fraud investigation report
    """
    try:
        # Call the AI Agent
        report = investigate(request.transaction_id)

        return InvestigationResponse(
            transaction_id=request.transaction_id,
            status="success",
            report=report
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Investigation failed: {str(e)}"
        )

# ─────────────────────────────────────────
# Route 3 — List All Transactions
# ─────────────────────────────────────────
@app.get("/transactions")
def list_transactions():
    """
    Returns all available transactions for testing
    """
    from data import transactions
    return {
        "total"       : len(transactions),
        "transactions": transactions
    }

# ─────────────────────────────────────────
# Run the Server
# ─────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )