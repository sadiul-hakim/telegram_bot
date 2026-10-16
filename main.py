import telebot
from dotenv import load_dotenv
import os

load_dotenv()

bot = telebot.TeleBot(token=os.getenv("API_TOKEN"))


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


# This handlers should come last
@bot.message_handler(func=lambda message: True)
def reply_func(message):
    bot.reply_to(message, text="We received your message!")


bot.polling()
