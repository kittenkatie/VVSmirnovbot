import telebot
from telebot import types
from flask import Flask, request
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

print("🚀 Бот инициализирован")

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
    print(f"✅ Получена команда /start от {message.chat.id}")  # для логов
    bot.send_message(
        message.chat.id,
        "👋 Здравствуйте!\n\nЯ официальный информационный бот **Владимира Викторовича Смирнова**.\n\nВыберите раздел:",
        parse_mode='Markdown',
        reply_markup=main_menu()
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    print(f"✅ Нажата кнопка: {call.data}")  # для отладки
    # ... (тексты BIO, POLITICS и т.д. можешь оставить как раньше)


@app.route('/webhook', methods=['POST'])
def webhook():
    print("📥 Получен update от Telegram")
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '', 200


if __name__ == "__main__":
    print("🔄 Удаляем старый webhook...")
    bot.remove_webhook()

    domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")
    if domain:
        url = f"https://{domain}/webhook"
        bot.set_webhook(url=url)
        print(f"✅ Webhook установлен: {url}")
    else:
        print("❌ RAILWAY_PUBLIC_DOMAIN не найден!")

    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
