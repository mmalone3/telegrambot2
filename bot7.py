import os
import tempfile
import traceback
import logging
import asyncio
import openai
import speech_recognition as sr
from pydub import AudioSegment
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import json
from pathlib import Path

# Load API keys from config.json
# Adjust the relative path as needed
config_path = Path(__file__).resolve().parent.parent / 'config' / 'config.json'
if not config_path.is_file():
    print(f"Error: config.json file not found at {config_path}")
    exit(1)

with open(config_path, 'r') as config_file:
    config = json.load(config_file)

api_key = config.get('OPENAI_API_KEY')
telegram_key = config.get('TELEGRAM_BOT_TOKEN')

# Debug prints to verify API keys
print(f"OPENAI_API_KEY: {api_key}")
print(f"TELEGRAM_BOT_TOKEN: {telegram_key}")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in config.json")
if not telegram_key:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in config.json")

openai.api_key = api_key

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def start(update: Update, context):
    await update.message.reply_text("Hello! I am an AI assistant. How can I help you today?")
    await update.message.reply_text("Please type your message below and I will respond to you as soon as possible.")

async def text_message(update: Update, context):
    try:
        message = update.message.text
        
        # Wrap potentially blocking operations in asyncio.to_thread
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(None, lambda: openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": message}]))
        
        await update.message.reply_text(response.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

async def test_connection(update: Update, context):
    try:
        await update.message.reply_text("Testing connection...")
        bot_info = await application.bot.get_me()
        await update.message.reply_text(f"Connected successfully. Bot name: {bot_info.username}")
    except Exception as e:
        await update.message.reply_text(f"Connection test failed: {str(e)}")

async def voice_message(update: Update, context):
    try:
        audio_file = await update.message.voice.get_file()
        # Download the audio file
        temp_dir = tempfile.mkdtemp()
        ogg_path = os.path.join(temp_dir, 'input.ogg')
        wav_path = os.path.join(temp_dir, 'output.wav')
        await audio_file.download_to_drive(ogg_path)
        # Try to convert OGG to WAV using pydub
        try:
            sound = AudioSegment.from_ogg(ogg_path)
            sound.export(wav_path, format="wav")
        except Exception as e:
            logger.error(f"Failed to convert OGG to WAV: {e}")
            await update.message.reply_text("Sorry, I couldn't process your voice message due to a technical issue.")
            return
        # Recognize speech
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio = recognizer.record(source)
        transcript = recognizer.recognize_google(audio)
        # Clean up temporary files
        os.remove(ogg_path)
        os.remove(wav_path)
        os.rmdir(temp_dir)
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": transcript}
        ]
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        await update.message.reply_text(response.choices[0].message.content)
        await add_to_conversation_history(transcript, response.choices[0].message.content)
    except Exception as e:
        logger.error(f"Error in voice_message: {repr(e)}\n{traceback.format_exc()}")
        await update.message.reply_text("An unexpected error occurred while processing your voice message.")

async def add_to_conversation_history(user_message, bot_response):
    # This is a placeholder function. Implement your logic to save the conversation history.
    logger.info(f"User: {user_message}")
    logger.info(f"Bot: {bot_response}")

application = Application.builder().token(telegram_key).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message))
application.add_handler(MessageHandler(filters.VOICE, voice_message))
application.add_handler(CommandHandler("test", test_connection))

# Start the bot
def main():
    global application
    
    try:
        logger.info("Initializing Telegram bot...")
        application.run_polling()
    except Exception as e:
        logger.error(f"Error initializing Telegram bot: {str(e)}", exc_info=True)

if __name__ == '__main__':
    logger.info("Starting Telegram bot...")
    main()
    logger.info("Bot stopped.")
