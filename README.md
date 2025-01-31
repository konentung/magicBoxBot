# MagicBoxBot

MagicBoxBot is a LINEBot designed to bring fun and utility to its users. This bot includes a variety of small games and features like 1A2B, paper scissosr stone, calendar recording, and magic box AI. Whether you're looking for a fun game to pass the time or need a quick AI assistant, MagicBoxBot has got you covered!

## Features:
- **1A2B Game**: Start the game by typing "1A2B" to the bot. The bot will generate a random number, and you need to guess it.
- **Rock-Paper-Scissors**: Type "rock", "paper", or "scissors" to play against the bot.
- **Calendar Record**: Use the "add event" command followed by the event details to save reminders or events.
- **AI Q&A**: Simply type any question, and the bot will respond with an intelligent answer.

## How to Use:

### Add MagicBoxBot:
You can add MagicBoxBot to your LINE friends list by scanning the QR code below. Once added, you can start using all of the available features directly in your chat!
![544xkvdn](https://github.com/user-attachments/assets/c4877483-03e7-4e10-bbb4-6c27d3bf2fe7)
Link：https://line.me/R/ti/p/@544xkvdn

## Install On Your Local

### Running the Bot:
MagicBoxBot is powered by LINE Messaging API and hosted on a cloud server. To set it up:

1. Clone this repository to your local machine or server.
    ```bash
    git clone https://github.com/konentung/MagicBoxBot.git
    cd MagicBoxBot
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your LINE Messaging API credentials. You will need to create a LINE Developers account and get your channel's API credentials (Channel Secret and Channel Access Token).

4. Set up Ngrok for your computer to be a server link to line platform

5. Configure the bot by setting up the environment variables for the credentials in a `.env` file.(need mongodb_url and openai_api_key)

6. Run the bot with:
    ```bash
    python app.py
    ```

## License:
This project is open source and available under the MIT License.
