import os
import requests
from googletrans import Translator
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Telegram Bot Token (replace with your actual token safely)
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Hugging Face Token
HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = "stabilityai/stable-diffusion-2"

translator = Translator()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Namaste! Mujhe likho kya image chahiye (Hindi me).")

async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    translated = translator.translate(user_text, src='hi', dest='en').text

    await update.message.reply_text("⏳ Image bana raha hoon... thoda wait karo!")

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{HF_MODEL}",
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
        json={"inputs": translated}
    )

    if response.status_code == 200:
        image_bytes = response.content
        with open("image.jpg", "wb") as f:
            f.write(image_bytes)
        await update.message.reply_photo(photo=open("image.jpg", "rb"))
    else:
        await update.message.reply_text("😢 Sorry, image generate nahi ho payi.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))

if __name__ == "__main__":
    print("Bot is running...")
    app.run_polling()
