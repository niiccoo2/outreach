## Outreach

Outreach is a simple program that uses google AI to automate general recearch and outreach for you.

This is meant for continuous opperation. So once it is set up, if you run it again it will remain on the same task. If you want to switch tasks just remove the .env file to restart setup.

[Demo video](https://photos.nicosmith.net/s/outreach_demo)

## How to use

### Prerequisites

Before you run the program, you should make sure you have the following pieces of information:

- Google AI API key (get one [here](https://aistudio.google.com/apikey))
- SMTP login info ([gmail](https://groups.google.com/g/intersystems-public-cache/c/S5yYxP5gJzM?pli=1), [proton](https://account.proton.me/u/1/mail/imap-smtp))
- A prompt. This is telling the AI what outreach you are trying to do, so remember to be specific.

### Running the script

If it doesn't see a .env file, then it should run through the setup process which will ask for all the required information. Then it will start recearching and sending all the emails.

### Options

| Option           | Meaning                                                      |
| ---------------- | ------------------------------------------------------------ |
| `--amount 50`    | Changes the number of emails the program sends               |
| `--send-to-self` | Sends all emails to SMTP sending address, useful for testing |

## What it does

- Saves prompt and API keys in .env
  - Auto detects if not there and run a setup function
- Finds new companies to reach out to
  - Makes sure we have not already emailed them
- Finds contact info
- Drafts all emails
- Sends all emails using SMTP
