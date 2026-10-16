import telebot
from dotenv import load_dotenv
import os

load_dotenv()

bot = telebot.TeleBot(token=os.getenv("API_TOKEN"))
print("Bot is running.....")


## Helper function
def separate_csv_file(m):
    return (
        m.document.file_name and m.document.file_name.lower().endswith(".csv")
    ) or m.document.mime_type in [
        "text/csv",
        "application/vnd.ms-excel",
        "application/csv",
    ]


@bot.message_handler(commands=["start"])
def welcome(message):
    welcome_text = f"Hi {message.from_user.last_name}, welcome to the Bot!"
    bot.send_message(message.chat.id, welcome_text)


@bot.message_handler(commands=["contact"])
def contact(message):
    contact_text = """
    Contact us at:
    -------------
    Email : softiomanagement@gmail.com
    Phone : +880 1580-625257
    """
    bot.send_message(message.chat.id, contact_text)


@bot.message_handler(regexp="2024")
def handle_message(message):
    bot.reply_to(message, "2024 is too old")


@bot.message_handler(content_types=["document"], func=separate_csv_file)
def handle_csv_doc(message):
    bot.reply_to(message, "Your CSV data would be processed, thanks.")


@bot.message_handler(content_types=["audio", "document"])
def handle_audio_doc(message):
    if message.audio:
        bot.reply_to(message, "Audio is not allowed.")
    elif message.document:
        bot.reply_to(message, "Your document would be processed.")


# This handlers should come last
@bot.message_handler(func=lambda message: True)
def reply_func(message):
    bot.reply_to(message, text="We received your message!")


bot.polling()
