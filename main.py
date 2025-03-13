import os
import shutil
import asyncio
from pydantic import BaseModel
from ChainWorkflow.chain import full_chain
from ChainWorkflow.chain import full_chain
from ChainWorkflow.utils.parse_info import get_company_info  # Importing your functions
from fastapi import FastAPI, UploadFile, File, HTTPException


app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True) 

class AutomationRequest(BaseModel):
    company_name: str
    industry: str
    engagement_level: str
    objections: str
    insurance_company_name: str
    sender_name: str
    recipient_email: str
    recipient_phone: str

async def retry_abatch(data, retries=3, delay=5):
    for i in range(retries):
        try:
            return await full_chain.abatch(data)
        except Exception as e:
            if "rate limit" in str(e).lower():
                print(f"Rate limited. Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                raise e
    raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")


@app.post("/generate_email")
async def automate(request: AutomationRequest):
    try:
        response = await full_chain.ainvoke({
            "company_name": request.company_name,
            "industry": request.industry,
            "engagement_level": request.engagement_level,
            "objection": request.objections,
            "insurance_company_name": request.insurance_company_name,
            "sender_name": request.sender_name,
            "recipient_email": request.recipient_email,
            "recipient_phone": request.recipient_phone
        })
        return {'response': response}
    except Exception as e:
        return {"error": str(e)}
    
@app.post("/generate_batch")
async def upload_file(file: UploadFile = File(...)):
    """
    API to handle file uploads, parse company info, and return automated responses.
    """
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    company_data = get_company_info(file_path)
    if company_data is None:
        raise HTTPException(status_code=400, detail="Invalid file format or missing columns.")

    responses = await retry_abatch(company_data)

    os.remove(file_path)

    return {"responses": responses}

@app.get("/")
async def root():
    return {"message": "Welcome to the ChainWorkflow API!😶‍🌫️"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)