# from django.core.management import BaseCommand
# from django.conf import settings
# from django.urls import reverse
# from telegram import KeyboardButton
# from core.models import ParentCategory, ProductManufacturer





# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         import logging

#         from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
#         from telegram.ext import (
#             Updater,
#             CommandHandler,
#             MessageHandler,
#             Filters,
#             ConversationHandler,
#             CallbackContext,
#             PicklePersistence
#         )

#         from core.models import Category, Product, Order
#         from core.constants import OrderOriginEnum

#         # Enable logging
#         logging.basicConfig(
#             format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
#         )

#         logger = logging.getLogger(__name__)

#         CATEGORY, CHILD_CATEGORY, MANUFACTURER, PRODUCT, ORDER, ORDER_DONE = range(6)

#         def start(update: Update, _: CallbackContext) -> int:
#             logger.info('Got start command')
#             categories = [c for c in ParentCategory.objects.all() if c.child_categories.count() > 0]
#             reply_keyboard = []
#             for category in categories:
#                 reply_keyboard.append([category.name])
#             update.message.reply_text(
#                 '''Вас приветствует Компания Unimed Trade!
# Мы являемся поставщиками медицинского оборудования и расходных материалов.
# Мы рады предложить вам широкий ассортимент оборудования из самых разных областей медицины.
# как мы можем помочь вам в решении ваших задач:
# 1-  При помощи БОТа вы можете выбрать нужную вам позицию и получить коммерческое предложения в виде pdf-файла 
# 2-  Напишите ваш вопрос – наши специалисты свяжутся с вами

# Связаться с нами: @ism_mnsr или
# +99897 7620955 Мансур Исмаилов
#                 ''',
#                 reply_markup=ReplyKeyboardMarkup(
#                     reply_keyboard),
#             )
#             return CATEGORY

#         def category(update: Update, _: CallbackContext) -> int:
#             logger.info('Category chosen.')
#             chosen_category_name = update.message.text
#             try:
#                 category = ParentCategory.objects.get(name=chosen_category_name)
#                 _.chat_data['chosen_parent_category'] = chosen_category_name
#             except ParentCategory.DoesNotExist:
#                 categories = [c for c in ParentCategory.objects.all() if c.child_categories.count() > 0]
#                 reply_keyboard = []
#                 for category in categories:
#                     reply_keyboard.append([category.name])
#                 update.message.reply_text(
#                     'Для ознакомления с нашими предложениями, выберите интересующую категорию:',
#                     reply_markup=ReplyKeyboardMarkup(
#                         reply_keyboard, one_time_keyboard=True),
#                 )
#                 return CATEGORY
#             reply_keyboard = []
#             child_categories = Category.objects.filter(parent=category)
#             for child in child_categories:
#                 reply_keyboard.append([child.name])
#             reply_keyboard.append(['Назад ◀'])
#             update.message.reply_text('Выберите категорию из предоставленного списка:',
#                                       reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard,
#                                                                        one_time_keyboard=True))
#             return CHILD_CATEGORY

#         def child_category(update: Update, _: CallbackContext) -> int:
#             if update.message.text == 'Назад ◀':
#                 categories = [c for c in ParentCategory.objects.all() if c.child_categories.count() > 0]
#                 reply_keyboard = []
#                 for category in categories:
#                     reply_keyboard.append([category.name])
#                 update.message.reply_text(
#                     'Для ознакомления с нашими предложениями, выберите интересующее направление:',
#                     reply_markup=ReplyKeyboardMarkup(
#                         reply_keyboard, one_time_keyboard=True),
#                 )
#                 return CATEGORY
#             logger.info('Child category chosen.')
#             chosen_category_name = update.message.text
#             try:
#                 category = Category.objects.get(name=chosen_category_name)
#                 _.chat_data['chosen_category'] = chosen_category_name
#             except Category.DoesNotExist:
#                 categories = [c for c in Category.objects.all() if c.products.count() > 0]
#                 reply_keyboard = []
#                 for category in categories:
#                     reply_keyboard.append([category.name])
#                 update.message.reply_text(
#                     'Для ознакомления с нашими предложениями, выберите интересующую категорию:',
#                     reply_markup=ReplyKeyboardMarkup(
#                         reply_keyboard, one_time_keyboard=True),
#                 )
#                 return CHILD_CATEGORY
#             reply_keyboard = []
#             manufacturers = ProductManufacturer.objects.filter(products__category=category).distinct()
#             for manufacturer in manufacturers:
#                 reply_keyboard.append([manufacturer.name])
#             reply_keyboard.append(['Назад ◀'])
#             update.message.reply_text('Выберите производителя из предоставленного списка:',
#                                       reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard,
#                                                                        one_time_keyboard=True))
#             return MANUFACTURER
        
#         def manufacturer(update: Update, _: CallbackContext) -> int:
#             if update.message.text == 'Назад ◀':
#                 chosen_parent_category = ParentCategory.objects.get(name=_.chat_data.get('chosen_parent_category'))
#                 reply_keyboard = []
#                 child_categories = Category.objects.filter(parent=chosen_parent_category)
#                 for child in child_categories:
#                     reply_keyboard.append([child.name])
#                 reply_keyboard.append(['Назад ◀'])
#                 update.message.reply_text('Выберите категорию из предоставленного списка:',
#                                           reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard,
#                                                                            one_time_keyboard=True))
#                 return CHILD_CATEGORY

#             chosen_manufacturer_name = update.message.text
#             try:
#                 chosen_manufacturer = ProductManufacturer.objects.get(name=chosen_manufacturer_name)
#                 _.chat_data['chosen_manufacturer_name'] = chosen_manufacturer_name
#             except ProductManufacturer.DoesNotExist:
#                 update.message.reply_text('Такого производителя не существует')
#                 return category(update, _)

#             chosen_category_name = _.chat_data.get('chosen_category')
#             chosen_category = Category.objects.get(name=chosen_category_name)
#             reply_keyboard = []
#             products = Product.objects.filter(category=chosen_category, manufacturer=chosen_manufacturer)
#             for p in products:
#                 reply_keyboard.append([p.name])
#             reply_keyboard.append(['Назад ◀'])
#             update.message.reply_text('Выберите продукт из предоставленного списка:',
#                                       reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard,
#                                                                        one_time_keyboard=True))
#             return PRODUCT

#         def product(update: Update, _: CallbackContext) -> int:
#             if update.message.text == 'Назад ◀':
#                 chosen_category = Category.objects.get(name=_.chat_data.get('chosen_category'))
#                 reply_keyboard = []
#                 manufacturers = ProductManufacturer.objects.filter(products__category=chosen_category).distinct()
#                 for manufacturer in manufacturers:
#                     reply_keyboard.append([manufacturer.name])
#                 reply_keyboard.append(['Назад ◀'])
#                 update.message.reply_text('Выберите производителя из предоставленного списка:',
#                                             reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard,
#                                                                             one_time_keyboard=True))
#                 return MANUFACTURER
#             logger.info('Product chosen')
#             chosen_product_name = update.message.text
#             try:
#                 chosen_product = Product.objects.get(name=chosen_product_name)
#                 _.chat_data['chosen_product'] = chosen_product_name
#             except Product.DoesNotExist:
#                 update.message.reply_text('Такого продукта не существует, выберите продукт из предоставленного списка!')
#                 return category(update, _)

#             update.message.reply_text(
#                 f'''Вы выбрали {chosen_product.name}.
#                 Просмотрите подробнее информацию по этой ссылке:
#                  {settings.TELEGRAM_BOT_WEBSITE_BASE_URL + reverse("product-detail", kwargs={"slug": chosen_product.slug})}''')
#             if chosen_product.images.count() > 0:
#                 update.message.reply_photo(chosen_product.images.first().image_file.file)
#             reply_keyboard = [
#                 [KeyboardButton(text='Да', request_contact=True)],
#                 [KeyboardButton(text='Нет')]
#             ]
#             update.message.reply_text(
#                 'Если хотите получить коммерческое предложение этого продукта нажмите ДА, для отмены нажмите НЕТ.',
#                 reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
#             return ORDER

#         def order(update: Update, _: CallbackContext) -> int:
#             logger.info('Order')

#             if update.message.contact:
#                 try:
#                     chosen_product = Product.objects.get(name=_.chat_data.get('chosen_product'))
#                     Order.objects.create(phone_number=update.message.contact.phone_number,
#                                          origin=OrderOriginEnum.TELEGRAM_BOT, chosen_product=chosen_product)
#                     update.message.reply_text(
#                         '''Спасибо! Высылаю КП для этого продукта. 
# Для уточнения деталей вы можете обратиться к нашему менеджеру @ism_mnsr или
# +998977620955 Мансур Исмаилов.
#                     ''')
#                     update.message.reply_document(chosen_product.commercial_proposal_file.file)
#                     return category(update, _)
#                 except Product.DoesNotExist:
#                     update.message.reply_text('Что-то пошло не так. Этот продукт больше не доступен. Попробуйте позже')
#                     return category(update, _)

#             update.message.reply_text('Отменено. Возвращаю вас в категории.')
#             return category(update, _)

#         def cancel(update: Update, _: CallbackContext) -> int:
#             logger.info('Cancelled')
#             update.message.reply_text('Отменено.')
#             return category(update, _)

#         def main() -> None:
#             logger.info('Creating updater')
#             pp = PicklePersistence(filename='unimed_telegram_bot_persistence')
#             updater = Updater(settings.TELEGRAM_BOT_TOKEN, persistence=pp)

#             dispatcher = updater.dispatcher
#             logger.info('Conversation handler is being set up...')
#             conv_handler = ConversationHandler(
#                 entry_points=[CommandHandler('start', start), MessageHandler(Filters.all, start)],
#                 states={
#                     CATEGORY: [MessageHandler(Filters.text, category)],
#                     CHILD_CATEGORY: [MessageHandler(Filters.text, child_category)],
#                     MANUFACTURER: [MessageHandler(Filters.text, manufacturer)],
#                     PRODUCT: [MessageHandler(Filters.text, product)],
#                     ORDER: [
#                         MessageHandler(Filters.contact, order),
#                         MessageHandler(Filters.text, order)
#                     ],
#                 },
#                 fallbacks=[CommandHandler('cancel', cancel)],
#                 persistent=True,
#                 name='UnimedtradeBotConversation',
#             )

#             logger.info('Added conversation handler to dispatcher')
#             dispatcher.add_handler(conv_handler)
#             logger.info('Starting bot')
#             # updater.start_polling()
#             updater.start_webhook(listen='127.0.0.1', port=8080, url_path='/telegram/',
#                                   webhook_url='https://unimedtrade.uz/telegram/')

#             updater.idle()

#         logger.info('Starting bot')
#         main()
