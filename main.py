import os

import telebot
from dotenv import load_dotenv
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()

bot = telebot.TeleBot(token=os.getenv("API_TOKEN"))
print("Bot is running.....")

chat_users = []

button1 = InlineKeyboardButton(text="Button1", callback_data="btn1")
button2 = InlineKeyboardButton(text="Button2", callback_data="btn2")
inline_board = InlineKeyboardMarkup(row_width=2)
inline_board.add(button1, button2)


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


@bot.message_handler(commands=["chat"])
def chat(message):
    bot.send_message(message.chat.id, "Please enter your name:")
    bot.register_next_step_handler(message, process_name)


def process_name(message):
    name = message.text
    bot.send_message(message.chat.id, f"Hi {name}!\n How old are you?")
    bot.register_next_step_handler(message, process_age)


def process_age(message):
    age = message.text
    bot.send_message(message.chat.id, f"You are {age} years old.\nThank you.")


@bot.message_handler(commands=["subscribe"])
def subscribe(message):
    if message.chat.id not in chat_users:
        chat_users.append(message.chat.id)

    bot.send_message(message.chat.id, "Thank you for subscribing.")


@bot.message_handler(commands=["broadcast"])
def broadcast(message):
    for id in chat_users:
        bot.send_message(id, "A new product is now available.")


@bot.message_handler(commands=["actions"])
def actions(message):
    bot.send_message(message.chat.id, "Welcome to Bot!", reply_markup=inline_board)


@bot.callback_query_handler(func=lambda call: True)
def check_button(call):
    if call.data == "btn1":
        bot.answer_callback_query(call.id, "btn1 is pressed", show_alert=True)
    elif call.data == "btn2":
        bot.answer_callback_query(call.id, "btn2 is pressed")


# This handlers should come last
@bot.message_handler(func=lambda message: True)
def reply_func(message):
    bot.reply_to(message, text="We received your message!")


bot.polling()
