import telebot
from telebot import types
from flask import Flask, request
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ==================== ТЕКСТЫ ====================
BIO = """👤 **Владимир Викторович Смирнов**

Депутат Законодательного Собрания Свердловской области VII созыва, заместитель председателя комитета по вопросам законодательства и общественной безопасности.

Дата рождения: 27.04.1981
Место рождения: г. Свердловск (Орджоникидзевский район)"""

POLITICS = """🏛 Политическая деятельность:
- 2017–2018 — депутат Екатеринбургской городской Думы
- 2019 и 2021 — депутат Заксобрания Свердловской области по округу №11"""

PUBLIC = """🌟 Общественная деятельность:
- Проект «Футбол в каждый двор»
- Проект «Старшее поколение»
- Оснащение школ
- Президент Федерации кикбоксинга (2019–2023)
- Почётный консул Шри-Ланки"""

AWARDS = """🏆 Награды:
- Заслуженный предприниматель Свердловской области (2023)
- Благодарность Губернатора (2024)"""

SVO = """🛡 Поддержка СВО
Региональный координатор рабочей группы по вопросам СВО партии «Единая Россия»."""

CONTACTS = """📞 Общественная приёмная:
г. Екатеринбург, пр. Космонавтов, 41 (ТРЦ «Омега», 4 этаж)

+7 (343) 200-26-36
+7 (950) 634-97-35

Пн и Чт 14:00–19:00 (запись обязательна)"""

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
    bot.send_message(
        message.chat.id,
        "👋 Здравствуйте!\n\nЯ официальный информационный бот **Владимира Викторовича Смирнова**.\n\nВыберите раздел:",
        parse_mode='Markdown',
        reply_markup=main_menu()
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    text = ""
    if call.data == "bio": text = BIO
    elif call.data == "politics": text = POLITICS
    elif call.data == "public": text = PUBLIC
    elif call.data == "awards": text = AWARDS
    elif call.data == "svo": text = SVO
    elif call.data == "contacts": text = CONTACTS

    if text:
        back = types.InlineKeyboardMarkup()
        back.add(types.InlineKeyboardButton("← Назад в меню", callback_data="back"))
        try:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text,
                parse_mode='Markdown',
                reply_markup=back
            )
        except:
            pass

    if call.data == "back":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Выберите нужный раздел 👇",
            reply_markup=main_menu()
        )

@app.route('/webhook', methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '', 200

if __name__ == "__main__":
    print("🚀 Запуск бота...")

    bot.remove_webhook()
    domain = "worker-production-ed07.up.railway.app"
    bot.set_webhook(url=f"https://{domain}/webhook")
    print(f"✅ Webhook установлен → https://{domain}/webhook")

    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
