import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure API tokens
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI client
client = openai.Client(api_key=OPENAI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        'Hi! I\'m a cognitive bias analyzer bot. Send me any text and I\'ll analyze it for potential biases and logical fallacies.'
    )

async def analyze_bias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Analyze the message for cognitive biases using OpenAI."""
    try:
        user_message = update.message.text
        
        # Create system prompt for bias analysis
        system_prompt = """
        Analyze the following text for cognitive biases and logical fallacies. 
        Consider common biases such as:
        - Confirmation bias
        - Anchoring bias
        - Availability heuristic
        - Bandwagon effect
        - False causality
        - Ad hominem arguments
        - Straw man arguments
        
        Provide a concise analysis highlighting any identified biases and explain why they are present.
        """
        
        # Get response from OpenAI
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        # Send the analysis back to the user
        analysis = response.choices[0].message.content
        await update.message.reply_text(analysis)
        
    except Exception as e:
        await update.message.reply_text(
            f"Sorry, I encountered an error while analyzing the message: {str(e)}"
        )

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, analyze_bias))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()