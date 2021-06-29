from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import telebot
from .constants import BUTTONS, STEP, SETTINGS
from core.models import *
from .services import *

bot = telebot.TeleBot(settings.TOKEN, threaded=True)

@csrf_exempt
def worker(request):
    if request.META['CONTENT_TYPE'] == 'application/json':
        json_data = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_data)
        bot.process_new_updates([update])
        return HttpResponse("")
    else:
        raise PermissionDenied


@bot.message_handler(commands=['start', 'help', 'назад'])
def send_welcome(message):
    try:
        user = Tuser.objects.get(userid=message.from_user.id)
    except Exception:
        user = Tuser.objects.create(userid=message.from_user.id, step=STEP['p_category'])
    user.step = STEP['p_category']
    user.save()
    
    # first message with pic and inline messages 
    pic = open('./static/img/tgmain.jpeg', 'rb')
    text = 'Установка <b>под ключ с гарантией</b>.  \n\nИз Европы и США по <b>низким ценам</b> '
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    b1 = telebot.types.InlineKeyboardButton(text="Открыть сайт", url="unimedtrade.uz")
    b2 = telebot.types.InlineKeyboardButton(text="О компании", url="unimedtrade.uz")
    b3 = telebot.types.InlineKeyboardButton(text="Подробно о рассрочке", url="unimedtrade.uz")
    keyboard.add(b1,b2)
    keyboard.add(b3)
    bot.send_photo(user.userid, pic, text, reply_markup=keyboard, parse_mode='HTML')

    pic.close()
    # second message with line and keybuttons
    text = 'Выберите категорию'
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [telebot.types.KeyboardButton(text=i.name) for i in ParentCategory.objects.all()]
    back = telebot.types.KeyboardButton(text='/start')
    keyboard.add(*buttons)
    keyboard.add(back)
    bot.send_message(user.userid, text, reply_markup=keyboard)
    



# В случае всех не совпадений третим шагом
def unknown_message(message, bot, user):
    bot.send_message(message.from_user.id, 'Нажмите /start')



# Вторым шагом проверяет Состояние пользователя не имеет ли пользователь совпадающее состояние
def all_text_messages_switcher(message, bot, user):
    try:
        switcher = {
            STEP['p_category']: chosenpcategory, 
            STEP['medium_category']: chosenmcategory,
            STEP['product']: product,
            
        }
        func = switcher.get(int(user.step), unknown_message)
        func(message, bot, user)
    except Exception as e:
        print(e)
        unknown_message(message, bot, user)




# Принимает все сообщения // первым шагом определяет не функциональная кнопка ли
@bot.message_handler(content_types=['text', 'contact', 'location', 'photo'])
def buttons_answer(message):
    try:
        user = Tuser.objects.get(userid = message.from_user.id)
        switcher = {
            BUTTONS['menu']: main,
            BUTTONS['back']: back,      
                }
        func = switcher.get(message.text, all_text_messages_switcher)
        func(message, bot, user)
    except Exception as e:
        print(e)
        unknown_message(message, bot, user)

