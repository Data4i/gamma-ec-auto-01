from decouple import config
from ChainWorkflow.utils.ec import send_email, make_phone_call

ACCOUNT_SID = config("ACCOUNT_SID")
AUTH_TOKEN = config("AUTH_TOKEN")
TWILIO_NUMBER = config("TWILIO_NUMBER")
RECIPIENT_NUMBER = "+2348101116037"
EMAIL_PASSWORD = config("EMAIL_APP_PASSWORD")

def send_cold_email(generated_inputs):
    try:
        send_email(
            subject=generated_inputs['subject'],
            recipient=generated_inputs['recipient_email'],
            body=generated_inputs['email'],
            sender_email="gammainsure@gmail.com",
            sender_password=EMAIL_PASSWORD
        )
        return "Success"
    except Exception as e:
        return "Failure"
    
def send_cold_call(generated_inputs):
    try:
        make_phone_call(
            recipient_phone=generated_inputs['recipient_phone'],
            call_script=generated_inputs['call_script'],
            twilio_number=TWILIO_NUMBER,
            account_sid=ACCOUNT_SID,
            auth_token=AUTH_TOKEN
        )
        return "Success"
    except Exception as e:
        return "Failure"
    
def get_advise(generated_inputs):
    return generated_inputs['advise']