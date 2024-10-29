# Telegram Bot on Pyrogram

This Telegram bot operates using an API client via the Pyrogram library. It provides a feature for verifying the existence of users by sending messages with a provided list of usernames, functioning through the Telegram API.

## Key Features

- **Message Handling**: Receives a list of usernames and returns three messages:
    1. A list of the first 23 valid usernames.
    2. A list of all verified usernames, where non-existent usernames are replaced with `нет`.
    3. A summary showing the number of usernames checked and how many exist.
- After processing, it logs the count of checks into an SQLite database.

## Requirements

- Python 3.8+.
- Pyrogram.
- Telegram API credentials (API ID and API Hash), which can be obtained by creating an app on the official Telegram website.

## Installation

1. Clone the repository:
  
```bash
git clone https://github.com/Pashosi/telegram_bot.git 
cd telegram_bot
```


2. Install the dependencies:
```bash
pip install -r requirements.txt
```
3. Set up environment variables for your API credentials:
```bash
export API_ID=your_api_id 
export API_HASH=your_api_hash
export TOKEN=your_api_hash
```

## Configuration

Create a configuration file (`config.json`) or use environment variables to store your API ID, API Hash, and any other customizable settings for the bot.

Example `config.json`:

 ```json
{ "api_id": "your_api_id", 
 "api_hash": "your_api_hash",
 "bot_token": "your_bot_token" }
```
## Usage

To start the bot, use:

```bash
python client.py
```
The bot will connect to Telegram via Pyrogram and begin processing messages based on the provided usernames list.

### Bot Command Examples

- Send `@<username>`
## Project Structure

- **client.py**: The main file that starts the bot and handles commands and messages.
- **client2.py**: A secondary main file that also starts the bot and handles commands and messages.
- Other files were used for training purposes.

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/NewFeature`).
3. Commit your changes (`git commit -m 'Add NewFeature'`).
4. Push to the branch (`git push origin feature/NewFeature`).
5. Open a Pull Request.
