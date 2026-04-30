import telebot
from telebot import types
from flask import Flask, request
import os

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    print("❌ BOT_TOKEN не найден!")
    exit(1)

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("👤 Биография", callback_data="bio"),
        types.InlineKeyboardButton("🏛 Политическая деятельность", callback_data="politics"),
        types.InlineKeyboardButton("🌟 Общественная деятельность", callback_data="public"),
        types.InlineKeyboardButton("🏆 Награды", callback_data="awards"),
        types.InlineKeyboardButton("🛡 Поддержка СВО", callback_data="svo"),
        types.InlineKeyboardButton("📞 Приёмная", callback_data="contacts"),
        types.InlineKeyboardButton("🌐 Официальный сайт", url="https://smirnov96.ru/"),
        types.InlineKeyboardButton("📢 Telegram-канал", url="https://t.me/vsmirnov96")
    )
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "👋 Здравствуйте!\n\nЯ официальный информационный бот **Владимира Викторовича Смирнова**.\n\nВыберите раздел:",
                     parse_mode='Markdown',
                     reply_markup=main_menu())


@app.route('/webhook', methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '', 200


if __name__ == "__main__":
    print("🚀 Запуск бота...")

    bot.remove_webhook()

    domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")
    if domain:
        webhook_url = f"https://{domain}/webhook"
        bot.set_webhook(url=webhook_url)
        print(f"✅ Webhook установлен → {webhook_url}")
    else:
        print("⚠️ RAILWAY_PUBLIC_DOMAIN не найден. Сгенерируйте домен в Settings → Domains!")

    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
