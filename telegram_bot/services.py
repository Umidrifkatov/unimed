from core.models import *
from .constants import *
import telebot
from django.conf import settings

# BUTTONS @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••



def main(message, bot, user):
    print('главная')

def back(message, bot, user):
    print('назад')













# STEPS @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••


def chosenpcategory(message, bot, user):
    user.step = STEP['medium_category']
    user.save()
    text = message.text
    p_category = Category.objects.filter(parent__name=message.text)
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [telebot.types.KeyboardButton(text=i.name) for i in p_category]
    key = telebot.types.KeyboardButton(text='/назад')
    keyboard.add(*buttons)
    keyboard.add(key)
    bot.send_message(user.userid, text, reply_markup=keyboard)
    
    
    


def chosenmcategory(message, bot, user):
    user.step = STEP['product']
    user.save()
    text = message.text
    p_category = Product.objects.filter(category__name=message.text)
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = []
    for i in p_category:
        if i.is_used:
            pr = telebot.types.KeyboardButton(text=f'{i.name} б/у')
        else:
            pr = telebot.types.KeyboardButton(text=f'{i.name} New')
        buttons.append(pr)
    key = telebot.types.KeyboardButton(text='/назад')
    keyboard.add(*buttons)
    keyboard.add(key)
    bot.send_message(user.userid, text, reply_markup=keyboard)


def product(message, bot, user):  
    product = Product.objects.get(name=message.text[:-4])
    text = product.short_description
    text = f'Производитель: <b>{product.manufacturer.name}</b>\n\n' + text
    text = f'<b>{product.name}</b>\n\n' + text
    text = text + f'\n\n<a href="{settings.MAIN_URL}{product.brochure.url}">Подробнее</a>'
    
    pic = product.images.first().image_file.file
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    buttons = telebot.types.InlineKeyboardButton(text="Коммерческое предложение", url=f"{settings.MAIN_URL}{product.commercial_proposal_file.url}")
    
    keyboard.add(buttons)
    
    bot.send_photo(user.userid, pic, text, reply_markup=keyboard, parse_mode='HTML')
