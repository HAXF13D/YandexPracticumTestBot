from telegram import ReplyKeyboardMarkup, KeyboardButton


get_photo_btn = KeyboardButton("Посмотреть фото")
get_interests_btn = KeyboardButton("Главное увлечение")
get_love_story_btn = KeyboardButton("История первой любви❤️")
help_btn = KeyboardButton("Помощь")

get_photo_1_btn = KeyboardButton("Последнее сделанное селфи")
get_photo_2_btn = KeyboardButton("Фотография со старшей школы")
back_btn = KeyboardButton("Назад")

main_kb = ReplyKeyboardMarkup(keyboard=[
    [get_photo_btn],
    [get_interests_btn],
    [get_love_story_btn],
    [help_btn]
], resize_keyboard=True, is_persistent=True)

photo_keyboard = ReplyKeyboardMarkup([
    [get_photo_1_btn],
    [get_photo_2_btn],
    [back_btn]
], resize_keyboard=True, is_persistent=True)
