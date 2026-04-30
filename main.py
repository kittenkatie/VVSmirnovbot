import telebot
from telebot import types
import os
import sys

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    print("❌ BOT_TOKEN не найден в Railway!")
    sys.exit(1)

bot = telebot.TeleBot(TOKEN)

# ==================== ТЕКСТЫ ====================
BIO = """👤 Владимир Викторович Смирнов
Депутат Законодательного Собрания Свердловской области VII созыва, заместитель председателя комитета по вопросам законодательства и общественной безопасности.

Родился 27 апреля 1981 года в Свердловске. Окончил с отличием Уральский государственный экономический университет. Служил в Управлении ФСБ России по Свердловской области (подполковник запаса)."""

ACHIEVEMENTS = """📊 Достижения:
- Реконструировал 19 спортивных площадок в рамках проекта "Футбол в каждый двор"
- Помог более 15 000 ветеранам и пенсионерам
- Оснастил школы современным оборудованием на сумму более 3,5 млн рублей
- Президент Федерации кикбоксинга Свердловской области
- Почетный консул Шри-Ланки в Екатеринбурге"""

PROGRAM = """🎯 Предвыборная программа:
1. Поддержка участников СВО и их семей
2. Развитие массового спорта
3. Забота о ветеранах и пожилых
4. Благоустройство территории
5. Поддержка малого бизнеса
6. Общественная безопасность"""

AWARDS = """🏆 Награды:
- Заслуженный предприниматель Свердловской области
- Благодарности Губернатора и Законодательного Собрания
- Медаль "40 лет ликвидации аварии на ЧАЭС" и другие"""

SVO = """🛡 Поддержка СВО
Региональный координатор рабочей группы по вопросам СВО партии "Единая Россия". 
Регулярно помогает бойцам и семьям участников специальной военной операции."""

CONTACTS = """📞 Общественная приемная:
г. Екатеринбург, пр. Космонавтов, 41 (ТРЦ "Омега", 4 этаж)

+7 (343) 200-26-36
+7 (950) 634-97-35

Понедельник и четверг с 14:00 до 19:00
(запись обязательна)"""

# ==================== КЛАВИАТУРА ====================
def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("👤 Биография", callback_data="bio"),
        types.InlineKeyboardButton("📊 Достижения", callback_data="achievements"),
        types.InlineKeyboardButton("🎯 Программа", callback_data="program"),
        types.InlineKeyboardButton("🏆 Награды", callback_data="awards"),
        types.InlineKeyboardButton("🛡 СВО", callback_data="svo"),
        types.InlineKeyboardButton("📞 Приемная", callback_data="contacts")
    )
    return markup


# ==================== ХЕНДЛЕРЫ ====================
@bot.message_handler(commands=['start'])
def start(message):
    text = """Здравствуйте! 👋

Я официальный информационный бот депутата **Владимира Викторовича Смирнова**.

Выберите интересующий раздел:"""
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=main_menu())


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    text = ""
    if call.data == "bio":
        text = BIO
    elif call.data == "achievements":
        text = ACHIEVEMENTS
    elif call.data == "program":
        text = PROGRAM
    elif call.data == "awards":
        text = AWARDS
    elif call.data == "svo":
        text = SVO
    elif call.data == "contacts":
        text = CONTACTS

    back_markup = types.InlineKeyboardMarkup()
    back_markup.add(types.InlineKeyboardButton("← Назад в меню", callback_data="back"))

    try:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            parse_mode='Markdown',
            reply_markup=back_markup
        )
    except:
        pass

    if call.data == "back":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Выберите раздел 👇",
            reply_markup=main_menu()
        )


if __name__ == "__main__":
    print("🚀 Бот Смирнова успешно запущен на Railway!")
    bot.infinity_polling()
