import os
import logging
from dotenv import load_dotenv  # Import the new library
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from transformers import pipeline
import torch

# --- SECURE CONFIGURATION ---
# Load environment variables from the .env file
load_dotenv()

# Get the token safely
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Safety check: Stop the program if the token is missing
if not TELEGRAM_TOKEN:
    raise ValueError("Error: TELEGRAM_TOKEN not found. Make sure you have a .env file.")

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# --- 1. LOAD THE LLM (The "Brain") ---
print("Loading TinyLlama... this might take a minute.")
# We use 'pipeline' for simplicity. 
# device_map="auto" tries to use GPU if available, otherwise CPU.
pipe = pipeline(
    "text-generation", 
    model=MODEL_NAME, 
    torch_dtype=torch.bfloat16, 
    device_map="auto" 
)

# --- 2. DEFINE BOT FUNCTIONS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responds to the /start command"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Hello! I am your AI Assistant running locally. Ask me about animals!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    1. Receives user message.
    2. Feeds it to TinyLlama.
    3. Sends the answer back.
    """
    user_input = update.message.text
    chat_id = update.effective_chat.id
    
    print(f"Received: {user_input}") # For debugging
    
    # Send a "typing..." status so the user knows we are thinking
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    # --- INFERENCE STEP ---
    # We format the prompt so TinyLlama understands it's a chat
    prompt = f"<|user|>\n{user_input}</s>\n<|assistant|>\n"
    
    # Generate response (max_new_tokens limits length to save time)
    sequences = pipe(
        prompt, 
        max_new_tokens=100, 
        do_sample=True, 
        temperature=0.7, 
        top_k=50, 
        top_p=0.95
    )
    
    # Extract just the answer text
    generated_text = sequences[0]['generated_text']
    # Clean up the tags to show only the bot's reply
    answer = generated_text.split("<|assistant|>\n")[-1]

    # Send back to Telegram
    await context.bot.send_message(chat_id=chat_id, text=answer)

# --- 3. RUN THE APPLICATION ---

if __name__ == '__main__':
    # Build the application
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Add handlers
    start_handler = CommandHandler('start', start)
    msg_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    
    application.add_handler(start_handler)
    application.add_handler(msg_handler)
    
    print("Bot is polling...")
    # Run the bot
    application.run_polling()