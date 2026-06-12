## Outreach

Outreach is a simple program that should be able to use AI to automate general recearch and outreach for you.

This is meant for continuous opperation. So once it is set up, if you run it again it will remain on the same task. If you want to switch tasks just remove the .env file.

Order of operations:

- Save prompt and API keys in .env
  - Auto detect if not there and run a setup function
- Find new companies to reach out to
  - Make sure we have not already emailed them
- Find contact info
- Draft all emails
- Send all emails using SMTP
