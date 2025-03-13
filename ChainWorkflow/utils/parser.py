from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser

class EmailAdvise(BaseModel):
    recipient_email: str = Field(description="The **email address of the recipient** (as provided in the input).")
    recipient_phone: str = Field(description="The **phone number of the recipient** (as provided in the input)")
    subject: str = Field(description="A compelling **email subject line** that grabs attention and encourages the recipient to open the email. ")
    email: str = Field(description="A cold email personalized based on the industry, engagement level, and objections.")
    call_script: str = Field(description="A structured cold call script for sales representatives to use.")
    advise: str = Field(description="A strategy to further engage the client based on their industry and previous response.")

parser = JsonOutputParser(pydantic_object=EmailAdvise)
