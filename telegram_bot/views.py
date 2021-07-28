from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import telebot
from .constants import BUTTONS, STEP
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

    

@bot.message_handler(commands=['start',]) # excluded from main commands handler for 'start', additional parsing data that com with start
def send_welcome(message): # https://t.me/Unimed_test_bot?start=1
    mess = message.text.split()
    starter = None
    
    try:
        if len(mess) == 2 and mess[1]:
            try:
                starter = Starter.objects.get(key=mess[1])
            except Exception as e:
                pass           
         
        try:
            user = Tuser.objects.get(userid=message.from_user.id)
        except Exception as e:
            user = Tuser.objects.create(userid=message.from_user.id, step=STEP['waiting_phone_start'], from_starter=starter )
    except Exception as e:
        print(e)           
    user.step = STEP['waiting_phone_start']
    user.save()

    # second message with line and keybuttons
    text = 'Чтобы продолжить отправьте свой номер телефона далее'
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    connect = telebot.types.KeyboardButton(text='📱 Перезвонить мне', request_contact=True)
    keyboard.add(connect)
    bot.send_message(user.userid, text, reply_markup=keyboard)
    



@bot.message_handler(commands=['help', 'назад',])
def message_start_sc(message):
    user = Tuser.objects.get(userid=message.from_user.id)
    user.step = STEP['p_category']
    user.save()
    # first message with pic and inline messages 
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


# отправка сообщения о нас
@bot.message_handler(commands=['about'])
def connection(message):
    user = Tuser.objects.get(userid=message.from_user.id)
    user.step = STEP['waiting_phone']
    user.save()
    bot.send_location(user.userid, settings.LOC, settings.LOC1)
    text = '<b>Адрес</b> - г.Ташкент. 6-проезд ул.Халкабод 25A\n\n<b>Телефон</b> +998712004404 \n\n\n<b>Нажмите на кнопку "📱 Перезвонить мне" чтобы с вами связались</b>'
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    connect = telebot.types.KeyboardButton(text='📱 Перезвонить мне', request_contact=True)
    back = telebot.types.KeyboardButton(text='/назад')
    keyboard.add(connect)
    keyboard.add(back)
    bot.send_message(user.userid, text, reply_markup=keyboard, parse_mode="HTML")


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
            STEP['waiting_phone']: get_phone,
            STEP['manufacturer']: manufacturer,
            STEP['waiting_phone_start']: phonewaitingstart,

            
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


# отправка сообщения о нас 
@bot.callback_query_handler(func=lambda call: True)
def call_message(message):
    parts = message.data
    if parts == 'call':
        connection(message)












@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(query):
    if not Tuser.objects.filter(userid = query.from_user.id).exists():
        Tuser.objects.create(userid=query.from_user.id)
    kb = telebot.types.InlineKeyboardMarkup(row_width=2)
    first = telebot.types.InlineKeyboardButton(text="Сайт", url="unimedtrade.uz")
    second = telebot.types.InlineKeyboardButton(text="БОТ", url="https://t.me/UnimedStoreBot")
    search = telebot.types.InlineKeyboardButton(text='🔎 Поиск', switch_inline_query_current_chat="кт")
    search1 = telebot.types.InlineKeyboardButton(text='Перезвонить 📲', url="https://t.me/UnimedStoreBot")
    kb.add(first, second)
    kb.add(search, search1)

    products = Product.objects.filter(name_search__icontains=query.query.lower())
    
    results = []
    for prod in products:
        if len(results) < 20:

            msg = telebot.types.InlineQueryResultArticle(
                id=f"{prod.id}", title=f"{prod.manufacturer.name} {prod.name}",
                input_message_content=telebot.types.InputTextMessageContent(message_text=f'{prod.manufacturer.name} {prod.name}\n\n{prod.short_description}\n\nОБОРУДОВАНИЕ В РАССРОЧКУ + TRADE-IN. \nUNIMED TRADE - поставщик нового и восстановленного медицинского оборудования в Узбекистане\n\n +998712004404\n@unimedstorebot'),
                reply_markup=kb,


            )

        
            results.append(msg)
    bot.answer_inline_query(query.id, results, cache_time=0)