import os
import base64
import dotenv
dotenv.load_dotenv()

from flask import Flask
from flask import request
from flask import redirect
from flask import render_template

import telebot
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
from telebot.types import InputTextMessageContent
from telebot.types import InlineQueryResultArticle

from telebot.util import parse_web_app_data
from telebot.util import validate_web_app_data


app = Flask(__name__, static_url_path="/static")
bot = telebot.TeleBot(os.getenv("API_TOKEN"), parse_mode="HTML")

@app.errorhandler(404)
def error404(e):
    return render_template("404.html")

@app.route('/')
def index():
    return "A simple Paint Application within Telegram :)"

@app.route('/paint')
def paint():
    return render_template("paint.html")

@app.route('/paintResponse', methods=["POST"])
def paintResponse():
    raw_data = request.json
    imageData = raw_data["imageData"]
    initData = raw_data["initData"]

    isValid = validate_web_app_data(bot.token, initData)

    if isValid:
        web_app_data = parse_web_app_data(bot.token, initData)
        query_id = web_app_data["query_id"]

        bot.send_photo(web_app_data["user"]["id"], base64.b64decode(imageData.split(',')[1]))
        
        bot.answer_web_app_query(query_id, InlineQueryResultArticle(
            id=query_id, title="IMAGE SAVED!",
            input_message_content=InputTextMessageContent(
                f"<i>Image saved! ✅</i>", parse_mode="HTML"),
            reply_markup=InlineKeyboardMarkup().row(
                InlineKeyboardButton("CLICK TO CONTINUE ✅",
                    callback_data=f"confirm-{web_app_data['user']['id']}"))))

    return redirect("/")
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT")))
