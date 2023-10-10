import os
import dotenv
dotenv.load_dotenv()

import telebot
from telebot.types import WebAppInfo
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

WEB_APP_URL = os.getenv('WEB_APP_URL')
bot = telebot.TeleBot(os.getenv('API_TOKEN'), parse_mode="HTML")

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id,
        "<i>Want to scribble your thoughts? 🎨\n\
            \nCheck out the app below! 👇🏻</i>",
                reply_markup=InlineKeyboardMarkup().row(
                    InlineKeyboardButton("Doodle Away! 🎨",web_app= WebAppInfo(WEB_APP_URL))))
    
if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)
