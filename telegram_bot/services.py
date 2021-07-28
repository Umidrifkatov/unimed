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


def get_phone(message, bot, user):
    got = False
    if message.content_type == 'contact':
        a = message.contact.phone_number
        if a.startswith('+'):
            a = a[1:]
        got = True
    elif len(message.text) == 12 and message.text.isdigit():
        a = message.text
        got = True
    if got:
        user.phone = a
        user.save()
        text = f'Получен запрос на обратный звонок\n\n +{a}'
        bot.send_message(settings.GROUP_ID, text)
        bot.send_message(user.userid, text)
    else:
        bot.send_message(user.userid, text='Введите номер телефона в формате 998987654321 или отправьте контакт')

    



def chosenpcategory(message, bot, user):
    user.step = STEP['medium_category']
    user.save()
    text = message.text
    if ParentCategory.objects.get(name=message.text):

        p_category = Category.objects.filter(parent__name=message.text)
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        buttons = [telebot.types.KeyboardButton(text=i.name) for i in p_category]
        key = telebot.types.KeyboardButton(text='/назад')
        keyboard.add(*buttons)
        keyboard.add(key)
        bot.send_message(user.userid, text, reply_markup=keyboard)
    
    

def chosenmcategory(message, bot, user):
    user.step = STEP['manufacturer']
    category = Category.objects.get(name=message.text)
    user.prestep = category.id
    user.save()
    text = message.text
    manufacturers = []
    all_product = Product.objects.filter(category=category)
    for man in all_product:
        if man.manufacturer not in manufacturers:
            manufacturers.append(man.manufacturer)
    
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = []
    for i in manufacturers:
        buttons.append(telebot.types.KeyboardButton(text=i.name))
    key = telebot.types.KeyboardButton(text='/назад')
    keyboard.add(*buttons)
    keyboard.add(key)
    bot.send_message(user.userid, text, reply_markup=keyboard)


def manufacturer(message, bot, user):
    user.step = STEP['product']
    user.save()
    text = message.text
    p_category = Product.objects.filter(category__id=user.prestep, manufacturer__name=message.text)

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
    text = text + f'\n\n<a href="{settings.MAIN_URL}/products/{product.slug}">Подробнее</a>'
    
    pic = product.images.first().image_file.file
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    buttons = telebot.types.InlineKeyboardButton(text="Коммерческое предложение", url=f"{settings.MAIN_URL}{product.commercial_proposal_file.url}")
    button = telebot.types.InlineKeyboardButton(text="Обратный звонок", callback_data='call')
    keyboard.add(buttons)
    keyboard.add(button)
    
    bot.send_photo(user.userid, pic, text, reply_markup=keyboard, parse_mode='HTML')




#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# SERVICES

def group_notificator(text="test"):
    bot.send_message(settings.GROUP_ID, text, parse_mode="HTML")





def phonewaitingstart(message, bot, user):
    if message.content_type == 'contact':
        contact = message.contact.phone_number
        user.phone = contact
        user.step = STEP['p_category']
        user.save()
        text = f'Новый пользоваетль ждет обработки\nНомер телефона: +{contact}'
        bot.send_message(settings.GROUP_ID, text)

        pic = open('./static/img/tgmain.jpeg', 'rb')
        text = 'Установка <b>под ключ с гарантией</b>.  \n\nИз Европы и США по <b>низким ценам</b> '
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
        b1 = telebot.types.InlineKeyboardButton(text="Открыть сайт", url="unimedtrade.uz")
        b2 = telebot.types.InlineKeyboardButton(text="О компании", url="unimedtrade.uz")
        b3 = telebot.types.InlineKeyboardButton(text="Подробно о рассрочке", url="unimedtrade.uz")
        b4 = telebot.types.InlineKeyboardButton(text='🔎 Поиск', switch_inline_query_current_chat="МРТ")
        keyboard.add(b1,b2)
        keyboard.add(b3)
        keyboard.add(b4)
        bot.send_photo(user.userid, pic, text, reply_markup=keyboard, parse_mode='HTML')
        pic.close()
        # second message with line and keybuttons
        text = 'Выберите категорию'
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        buttons = [telebot.types.KeyboardButton(text=i.name) for i in ParentCategory.objects.all()]
        keyboard.add(*buttons)
        bot.send_message(user.userid, text, reply_markup=keyboard)
    else:
        text = 'Чтобы продолжить отправьте свой номер телефона далее'
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        connect = telebot.types.KeyboardButton(text='📱 Перезвонить мне', request_contact=True)
        keyboard.add(connect)
        bot.send_message(user.userid, text, reply_markup=keyboard)



