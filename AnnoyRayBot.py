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
    message = (
        'Hi! I\'m a cognitive bias analyzer bot.\n\n'
        'In private chat: Just send me any text to analyze.\n'
        'In groups: Use /analyze followed by your text or reply to a message with /analyze.'
    )
    await update.message.reply_text(message)

async def analyze_text(text: str) -> str:
    """Analyze text using OpenAI API."""
    system_prompt = """
    Analyze the following text for cognitive biases and logical fallacies. 
    Consider common biases such as:
 - Confirmation Bias
            - Anchoring Bias
            - Availability Heuristic
            - Dunning-Kruger Effect
            - Sunk Cost Fallacy
            - Bandwagon Effect
            - Hindsight Bias
            - Self-Serving Bias
            - Optimism Bias
            - Negativity Bias
            - Framing Effect
            - Status Quo Bias
            - Ad Hominem
            - Strawman
            - Appeal to Authority
            - False Dichotomy (False Dilemma)
            - Slippery Slope
            - Circular Reasoning
            - Post Hoc Ergo Propter Hoc
            - Appeal to Emotion
            - Red Herring
            - Hasty Generalization
            - Begging the Question
            - No True Scotsman
            - Appeal to Ignorance
            - False Cause
            - Equivocation
            - Illusory Correlation
            - Actor-Observer Bias
            - Halo Effect
            - Horn Effect
            - Just-World Hypothesis
            - Availability Cascade
            - Ingroup Bias
            - Outgroup Homogeneity Bias
            - Survivorship Bias
            - Choice-Supportive Bias
            - Information Bias
            - Overconfidence Bias
            - Ostrich Effect
            - Loss Aversion
            - Gambler's Fallacy
            - Base Rate Fallacy
            - Reactance
            - Moral Credential Effect
            - Planning Fallacy
            - Status Quo Fallacy
            - Appeal to Nature
            - Appeal to Tradition
            - Texas Sharpshooter Fallacy
            - Nirvana Fallacy
            - Genetic Fallacy
            - Tu Quoque
            - Special Pleading
            - Moving the Goalposts
            - False Equivalence
            - Cherry Picking
            - Appeal to Common Belief
            
    Provide a concise analysis highlighting any identified biases and explain why they are present.
    """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        max_tokens=500,
        temperature=0.7
    )
    
    return response.choices[0].message.content

async def handle_analyze_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /analyze command in groups or private chats."""
    try:
        # Check if this is a reply to another message
        if update.message.reply_to_message:
            text_to_analyze = update.message.reply_to_message.text
        else:
            # Get the text after the /analyze command
            text_to_analyze = ' '.join(context.args)
            
        if not text_to_analyze:
            await update.message.reply_text(
                "Please provide text to analyze after the /analyze command, or reply to a message with /analyze"
            )
            return

        analysis = await analyze_text(text_to_analyze)
        await update.message.reply_text(analysis)
        
    except Exception as e:
        await update.message.reply_text(
            f"Sorry, I encountered an error while analyzing the message: {str(e)}"
        )

async def handle_private_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle messages in private chat."""
    try:
        analysis = await analyze_text(update.message.text)
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
    application.add_handler(CommandHandler("analyze", handle_analyze_command))
    
    # Only handle direct messages in private chats
    private_message_handler = MessageHandler(
        filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE,
        handle_private_message
    )
    application.add_handler(private_message_handler)

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
