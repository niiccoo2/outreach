from google import genai
import os
from dotenv import load_dotenv
import warnings
from sys import platform
from pydantic import BaseModel, Field
from typing import List, Optional
import ast
from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText

warnings.simplefilter("ignore", UserWarning)

number_of_emails: int = 20

class Company(BaseModel):
    name: str = Field(description="Name of the company.")
    email: str = Field(description="Contact email.")
    description: str = Field(description="Description of the company.")

class Email(BaseModel):
    to: str = Field(description="Email address to send to.")
    subject: str = Field(description="Email subject.")
    body: str = Field(description="Body of the email.")

def create_dotenv():
  print("No .env file found. Starting setup.")
  with open(".env", "a") as f:
    f.write(f'API_KEY="{input("Enter Google AI API key: ")}"\n')
    f.write(f'PROMPT="{input("""
            Prompt should include who you are, if you are a person or a company, and any other required info for an email.\n
            Enter prompt: 
                             """)}"\n')
    f.write(f'SMTP_SERVER="{input("Enter SMTP server address: ")}"\n')
    f.write(f'SMTP_SENDER="{input("Enter SMTP sender address (might be same as username): ")}"\n')
    f.write(f'SMTP_USER="{input("Enter SMTP username: ")}"\n')
    f.write(f'SMTP_PASS="{input("Enter SMTP password: ")}"\n')
    f.write('ALREADY_EMAILED=[]\n')

def save_new_company_to_dotenv(company: Company):
  global already_emailed
  already_emailed.append(company.name)

  with open('.env', 'r') as f:
      lines = f.readlines()

  for i, line in enumerate(lines):
    if 'ALREADY_EMAILED' in line:
        lines[i] = f"ALREADY_EMAILED={already_emailed}\n"
        break

  with open('.env', 'w') as f:
      f.writelines(lines)

if not os.path.exists('.env'):
    create_dotenv()

def find_companies():
  print(f"Finding {number_of_emails} companies")
  for i in range(number_of_emails):

    interaction = client.interactions.create(
        model="gemini-3.5-flash",
        input=f"""
              Find companies that align with the goal of the attached outreach campaign. '{os.getenv("PROMPT")}'.
              They must also not already be on this list: '{already_emailed}'.
              """,
        tools=[{"type": "google_search"}],
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": Company.model_json_schema()
        }
    )

    company = Company.model_validate_json(interaction.output_text)
    save_new_company_to_dotenv(company)
    companies.append(company)
    print(f"Found {company.name}")

def draft_emails():
  print(f"Drafting {number_of_emails} emails")
  for company in companies:
    interaction = client.interactions.create(
      model="gemini-3.5-flash",
      input=f"""
            Draft an email for the attached company that aligns with this outreach campaign. Make sure to use \\n to make new lines. '{os.getenv("PROMPT")}'.
            Company: '{company}'.
            """,
      response_format={
          "type": "text",
          "mime_type": "application/json",
          "schema": Email.model_json_schema()
      }
    )
    
    emails.append(Email.model_validate_json(interaction.output_text))
    print(f"Drafted email to {company.name}")

def send_emails():
  print(f"Sending {number_of_emails} emails")
  for email in emails:
    RECIPIENT = "nicosmith873@gmail.com"

    msg = MIMEText(email.body, "plain")
    msg['Subject'] = email.subject
    msg['From'] = SMTP_SENDER
    msg['To'] = RECIPIENT

    conn = SMTP(SMTP_SERVER)
    conn.set_debuglevel(False)
    conn.login(SMTP_USER, SMTP_PASS)
    try:
        conn.sendmail(SMTP_SENDER, RECIPIENT, msg.as_string())
    finally:
        conn.quit()
     

load_dotenv() # a correct env should exist by now
already_emailed: List[str] = ast.literal_eval(os.getenv("ALREADY_EMAILED", "[]"))
SMTP_SERVER = os.getenv("SMTP_SERVER", "")
SMTP_SENDER = os.getenv("SMTP_SENDER", "")
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
companies: List[Company] = []
emails: List[Email] = []

client = genai.Client(api_key=os.getenv("API_KEY"))

find_companies()
draft_emails()
send_emails()

print(f"Done! Sent {number_of_emails} emails!")