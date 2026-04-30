import telebot
from telebot import types
import os
import sys

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    print("❌ BOT_TOKEN не найден!")
    sys.exit(1)

bot = telebot.TeleBot(TOKEN)

# ==================== ТЕКСТЫ ====================
BIO = """👤 **Владимир Викторович Смирнов**

Депутат Законодательного Собрания Свердловской области VII созыва, заместитель председателя комитета по вопросам законодательства и общественной безопасности.

Дата рождения: 27.04.1981
Место рождения: г. Свердловск (Орджоникидзевский район)

Образование и служба:
- Окончил с отличием Уральский государственный экономический университет (2003)
- 2003–2008 — служба в Управлении ФСБ России (подполковник запаса)"""

POLITICS = """🏛 Политическая деятельность:
- 2017–2018 — депутат Екатеринбургской городской Думы
- 2019 и 2021 — депутат Заксобрания Свердловской области по округу №11
- Член партии «Единая Россия»"""

PUBLIC = """🌟 Общественная деятельность:
- Проект «Футбол в каждый двор» (19 площадок, более 3 млн руб.)
- Проект «Старшее поколение» (помощь более 15 000 ветеранам)
- Проект «Новая школа» (оснащение школ оборудованием)
- Организация пункта вакцинации (более 14 000 человек)
- Президент Федерации кикбоксинга Свердловской области (2019–2023)
- Почётный консул Шри-Ланки"""

AWARDS = """🏆 Награды:
- Заслуженный предприниматель Свердловской области (2023)
- Благодарственное письмо Губернатора (2024)
- Благодарственное письмо Законодательного Собрания (2021)
- Почётная грамота Администрации Екатеринбурга"""

SVO = """🛡 Поддержка СВО
С марта 2023 года — региональный координатор рабочей группы по вопросам СВО партии «Единая Россия».
Регулярно помогает участникам СВО и их семьям."""

CONTACTS = """📞 Общественная приёмная:
г. Екатеринбург, пр. Космонавтов, 41 (ТРЦ «Омега», 4 этаж)

☎️ +7 (343) 200-26-36
☎️ +7 (950) 634-97-35

🕒 Понедельник и четверг с 14:00 до 19:00
(предварительная запись обязательна)"""

# ==================== МЕНЮ НА РУССКОМ ====================
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


# ==================== ХЕНДЛЕРЫ ====================
@bot.message_handler(commands=['start'])
def start(message):
    text = """👋 Здравствуйте!

Я официальный информационный бот **Владимира Викторовича Смирнова** — депутата Законодательного Собрания Свердловской области.

Выберите нужный раздел:"""
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=main_menu())


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    text = ""
    if call.data == "bio":
        text = BIO
    elif call.data == "politics":
        text = POLITICS
    elif call.data == "public":
        text = PUBLIC
    elif call.data == "awards":
        text = AWARDS
    elif call.data == "svo":
        text = SVO
    elif call.data == "contacts":
        text = CONTACTS

    if text:
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
            text="Выберите нужный раздел 👇",
            reply_markup=main_menu()
        )


if __name__ == "__main__":
    print("🚀 Бот Смирнова запущен (меню на русском)")
    bot.infinity_polling()
