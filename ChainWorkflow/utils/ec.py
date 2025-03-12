import smtplib
from email.message import EmailMessage
import ssl
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

def make_phone_call(recipient_phone, call_script, twilio_number, account_sid, auth_token):
    """
    Makes a phone call to the recipient and speaks the script using Twilio.
    
    Parameters:
        recipent_phone (str): Recipient's phone number in E.164 format (e.g., "+1234567890").
        call_script (str): The text to be spoken during the call.
        twilio_number (str): Your Twilio phone number (E.164 format).
        account_sid (str): Twilio account SID.
        auth_token (str): Twilio authentication token.
    """
    # Initialize Twilio client
    client = Client(account_sid, auth_token)
    
    # Create TwiML (Telephony Markup Language) to define the call behavior
    twiml_response = VoiceResponse()
    twiml_response.say(call_script, voice='alice')  # 'alice' is a natural-sounding voice
    
    try:
        # Initiate the call
        call = client.calls.create(
            twiml=twiml_response.to_xml(),
            from_=twilio_number,
            to=recipient_phone
        )
        print(f"Call initiated! Call SID: {call.sid}")
    except Exception as e:
        print(f"Failed to make call: {e}")
        
        
def send_email(subject, recipient, body, sender_email, sender_password):
    """
    Sends an email using the provided details and SMTP server (e.g., Gmail).
    
    Parameters:
    - subject (str): Email subject
    - recipient (str): Recipient email address
    - body (str): Email body content
    - sender_email (str): Sender's email address (requires SMTP access)
    - sender_password (str): Sender's email password or app-specific password
    """
    # Create the email message
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient

    # Set up SSL context and SMTP server
    context = ssl.create_default_context()
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")