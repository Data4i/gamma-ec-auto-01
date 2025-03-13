import os
import shutil
import asyncio
import pandas as pd
from pydantic import BaseModel
from fastapi.responses import FileResponse
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
        response = await full_chain.ainvoke(
            {
                "company_name": request.company_name,
                "industry": request.industry,
                "engagement_level": request.engagement_level,
                "objection": request.objections,
                "insurance_company_name": request.insurance_company_name,
                "sender_name": request.sender_name,
                "recipient_email": request.recipient_email,
                "recipient_phone": request.recipient_phone,
            }
        )
        return response
    except Exception as e:
        return {"error": str(e)}


@app.post("/generate_batch")
async def upload_file(file: UploadFile = File(...)):
    """
    API to handle file uploads, parse company info, and return automated responses.
    """
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    output_file = os.path.join(UPLOAD_DIR, "batch_response.xlsx")

    try:
        # Save the uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract company data
        company_data = get_company_info(file_path)
        if not company_data:
            raise HTTPException(
                status_code=400, detail="Invalid file format or missing columns."
            )

        # Generate responses
        responses = await retry_abatch(company_data)

        # Convert responses to DataFrame
        df = pd.DataFrame(responses)

        # Ensure required columns exist
        if not {"company_name", "advise"}.issubset(df.columns):
            raise HTTPException(
                status_code=500, detail="Missing required columns in the response."
            )

        df = df[["company_name", "advise"]]

        # Save as Excel
        df.to_excel(output_file, index=False, engine="openpyxl")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    finally:
        # Clean up uploaded file after processing
        if os.path.exists(file_path):
            os.remove(file_path)

    # Return the generated Excel file
    return FileResponse(
        output_file,
        filename="batch_response.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@app.get("/")
async def root():
    return {"message": "Welcome to the ChainWorkflow API!😶‍🌫️"}
