# Telegram Bot with OpenAI Integration

This project implements a Telegram bot that integrates with OpenAI's GPT-3.5-turbo model to provide AI-powered responses to both text and voice messages. The bot can process text messages, convert voice messages to text, and generate intelligent responses using OpenAI's API [1].

## Features

- Text message processing with GPT-3.5-turbo
- Voice message transcription and processing
- Conversation history logging
- Error handling and connection testing
- Asynchronous message processing [2]

## Prerequisites

- Python 3.7 or higher
- Telegram Bot Token (obtain from @BotFather)
- OpenAI API Key
- Required Python packages (listed in requirements.txt) [1]

## Project Structure
project/ │ ├── config/ │ └── config.json │ ├── bot7/ │ └── bot7.py │ └── README.md

## Installation

1. Clone the repository:

2. Create and activate a virtual environment:

3. Install required packages:

4. Create a config.json file in the config directory:
json { "OPENAI_API_KEY": "your_openai_api_key", "TELEGRAM_BOT_TOKEN": "your_telegram_bot_token" }


## Configuration

1. Create a new Telegram bot using @BotFather and get the bot token
2. Obtain an OpenAI API key from the OpenAI platform
3. Add both keys to config.json [2]

## Usage

1. Navigate to the bot7 directory:

2. Run the bot:

3. Interact with your bot on Telegram:
   - Send text messages to get AI-powered responses
   - Send voice messages for transcription and AI responses
   - Use /start to begin interaction
   - Use /test to verify connection [1]

## Features in Detail

### Text Processing
- Handles text messages using OpenAI's GPT-3.5-turbo model
- Provides contextual responses based on user input

### Voice Processing
- Converts voice messages to text using speech recognition
- Supports OGG to WAV conversion for processing
- Handles multiple audio formats [2]

## Error Handling

The bot includes comprehensive error handling for:
- API connection issues
- Voice message processing errors
- Configuration problems
- General runtime errors [1]

## Dependencies

- python-telegram-bot
- openai
- speech_recognition
- pydub
- pathlib
- logging
- json
- asyncio [2]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request [4].

## Best Practices

- Secure API key management
- Comprehensive error handling
- Structured logging
- Clean code organization
- Asynchronous processing for better performance [2]

## License

This project is licensed under the MIT License - see the LICENSE file for details [1].

## Support

If you encounter any issues or have questions, please open an issue in the repository [4].
