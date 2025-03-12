from fastapi import FastAPI
from pydantic import BaseModel
from ChainWorkflow.chain import full_chain

app = FastAPI()

class AutomationRequest(BaseModel):
    company_name: str
    industry: str
    engagement_level: str
    objections: str
    insurance_company_name: str
    sender_name: str
    sender_email: str
    recipient_email: str
    recipient_phone: str

@app.post("/generate_email")
async def automate(request: AutomationRequest):
    try:
        response = full_chain.invoke({
            "company_name": request.company_name,
            "industry": request.industry,
            "engagement_level": request.engagement_level,
            "objection": request.objections,
            "insurance_company_name": request.insurance_company_name,
            "sender_name": request.sender_name,
            "sender_email": request.sender_email,
            "recipient_email": request.recipient_email,
            "recipient_phone": request.recipient_phone
        })
        return response
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)