import os

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, MessageHandler, filters
from keyboards import main_kb, photo_keyboard
from text_constants import WELCOME_TEXT, MY_HOBBY_TEXT, HELP_TEXT

# Определить состояния диалога
MAIN_CONV, PHOTO_CONV = range(2)
chosen_kb = main_kb


# Определение функции запуска, которая вызывается при запуске бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global chosen_kb
    chosen_kb = main_kb
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=WELCOME_TEXT,
        reply_markup=chosen_kb
    )
    return MAIN_CONV


# Определение функции выбора, которая обрабатывает команды пользователя в основном диалоге
async def select(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    command = update.message.text
    global chosen_kb
    if command == "Посмотреть фото":
        chosen_kb = photo_keyboard
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Выберите действие:",
            reply_markup=chosen_kb
        )
        return PHOTO_CONV
    else:
        chosen_kb = main_kb
        if command == "Главное увлечение":
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=MY_HOBBY_TEXT,
                reply_markup=chosen_kb
            )
        # Здесь обрабатываются другие команды (например, «История первой любви❤️» и «Помощь»)
        elif command == "История первой любви❤️":
            await context.bot.send_audio(
                chat_id=update.effective_chat.id,
                audio="./static/love_voice.mp3",
                reply_markup=chosen_kb,
                filename="Моя первая любовь"
            )
        elif command == "Помощь":
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=HELP_TEXT,
                reply_markup=chosen_kb
            )
        return MAIN_CONV


# Определение функции фото, которая обрабатывает команды пользователя в диалоге с фотографиями.
async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    command = update.message.text
    global chosen_kb
    if command == "Назад":
        chosen_kb = main_kb
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Выберите действие:",
            reply_markup=chosen_kb
        )
        return MAIN_CONV
    else:
        chosen_kb = photo_keyboard
        # Здесь обрабатываются различные команды, связанные с фотографиями
        if command == "Последнее сделанное селфи":
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo="./static/me_1.jpg",
                caption="✨Тут я занимаюсь параглайдингом✨",
                reply_markup=chosen_kb
            )
        elif command == "Фотография со старшей школы":
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo="./static/me_2.jpg",
                caption="✨Мое фото со старшей школы✨",
                reply_markup=chosen_kb
            )
        return PHOTO_CONV


# Определение функций для конкретных команд («gpt», «sql», «link» и «help»)
async def gpt_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global chosen_kb
    # Отправка аудио, связанного с информацией GPT
    await context.bot.send_audio(
        chat_id=update.effective_chat.id,
        audio="./static/gpt_voice.mp3",
        reply_markup=chosen_kb,
        filename="GPT для бабушки"
    )


async def sql_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global chosen_kb
    # Отправляем аудио, связанное с информацией SQL
    await context.bot.send_audio(
        chat_id=update.effective_chat.id,
        audio="./static/sql_voice.mp3",
        reply_markup=chosen_kb,
        filename="SQL и NoSQL в двух словах"
    )


async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global chosen_kb
    # Отправьте сообщение с текстом помощи
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=HELP_TEXT,
        reply_markup=chosen_kb
    )


async def link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global chosen_kb
    # Отправьте сообщение со ссылкой на исходный код бота на GitHub
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        parse_mode="MarkdownV2",
        text="Исходный код данного бота находится [тут](https://github.com/HAXF13D?tab=repositories/)\.",
        disable_web_page_preview=True,
        reply_markup=chosen_kb
    )


# Основная часть кода
if __name__ == '__main__':
    # Создание экземпляра ApplicationBuilder и указание токена бота из переменных среды.
    application = ApplicationBuilder().token(os.environ.get("TOKEN")).build()

    # Определение ConversationHandler с точками входа и состояниями
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start)
        ],
        states={
            MAIN_CONV: [
                MessageHandler(filters.ALL, select)
            ],
            PHOTO_CONV: [
                MessageHandler(filters.ALL, photo)
            ]
        },
        fallbacks=[
        ]
    )

    # Определение обработчиков команд для конкретных команд
    gpt_info_handler = CommandHandler('gpt', gpt_info)
    sql_info_handler = CommandHandler('sql', sql_info)
    link_handler = CommandHandler('link', link)
    help_handler = CommandHandler('help', show_help)

    application.add_handler(help_handler)
    application.add_handler(gpt_info_handler)
    application.add_handler(sql_info_handler)
    application.add_handler(link_handler)
    application.add_handler(conv_handler)

    # Начать опрос обновлений из Telegram
    application.run_polling()
