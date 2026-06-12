from google import genai
import os
from dotenv import load_dotenv
import warnings
import subprocess
from sys import platform
from pydantic import BaseModel, Field
from typing import List, Optional
import json

warnings.simplefilter("ignore", UserWarning)

number_of_emails: int = 3

class Company(BaseModel):
    company_name: str = Field(description="Name of the company.")
    email: str = Field(description="Contact email.")
    description: Optional[int] = Field(description="Description of the company.")

def clear():
  if platform == "win32":
    subprocess.call("cls", shell=True)
  else:
    subprocess.call("clear", shell=True)

def create_dotenv():
  print("No .env file found. Starting setup.")
  with open(".env", "a") as f:
    f.write(f'API_KEY="{input("Enter Google AI API key: ")}"\n')
    f.write(f'PROMPT="{input("Enter prompt: ")}"\n')
    f.write('ALREADY_EMAILED=[]\n')

def save_new_company_to_dotenv(company: str):
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

load_dotenv() # a correct env should exist by now

already_emailed: List[str] = json.loads(os.getenv("ALREADY_EMAILED", "[]"))

client = genai.Client(api_key=os.getenv("API_KEY"))

interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input=f"Find companies that align with the goal of the attached outreach campaign. '{os.getenv("PROMPT")}'",
    tools=[{"type": "google_search"}],
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": Company.model_json_schema()
    }
)

company = Company.model_validate_json(interaction.output_text)
already_emailed.append()
print(company)