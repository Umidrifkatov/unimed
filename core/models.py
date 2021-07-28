from django.db import models
from django.utils.translation import gettext_lazy as _
from core import constants
from core.constants import ClientTypeEnum
import random
from django.db.models.signals import pre_save


class ParentCategory(models.Model):
    name = models.CharField(max_length=255, unique=True,
                            verbose_name=_('Название'))
    slug = models.SlugField(verbose_name=_('Человекочитаемый идентификатор'))
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Родительская категория')
        verbose_name_plural = _('Родительские категории')


class Category(models.Model):
    parent = models.ForeignKey(ParentCategory, on_delete=models.CASCADE, related_name='child_categories')
    name = models.CharField(max_length=255, unique=True,
                            verbose_name=_('Название'))
    slug = models.SlugField(verbose_name=_('Человекочитаемый идентификатор'))
    def __str__(self):
        return self.name
    class Meta:

        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')

class ProductManufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_('Название бренда'))
    def __str__(self):
        return self.name

    class Meta:

        verbose_name = _('Производитель')
        verbose_name_plural = _('Производители')


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products',
                                 verbose_name=_('Принадлежит категории'))
    manufacturer = models.ForeignKey(ProductManufacturer, on_delete=models.CASCADE, related_name='products', verbose_name=_('Производитель'))
    name = models.CharField(max_length=255, unique=True,
                            verbose_name=_('Название (короткое)'))
    partner = models.CharField(max_length=25, default='Unimed',
                            verbose_name=_('Партнер'))
    name_search = models.CharField(max_length=400, unique=True, default='Нет',
                            verbose_name=_('Название для поиска (длинное)'))
    slug = models.SlugField(verbose_name=_('Человекочитаемый идентификатор'))
    short_description = models.TextField(verbose_name=_('Короткое описание'), blank=True)
    long_description = models.TextField(verbose_name=_('Общее описание'), blank=True)
    technical_details = models.TextField(
        verbose_name=_('Технические характеристики'), blank=True)
    brochure = models.FileField(
        upload_to='product_brochures', verbose_name=_('Брошюра'), blank=True, null=True)
    standard_of_equipment = models.FileField(upload_to='product_standards_of_equipment',
                                             verbose_name=_('Стандарт оснащения'), blank=True, null=True)
    commercial_proposal_file = models.FileField(
        upload_to='commercial_proposals', verbose_name=_('Файл КП'), blank=True, null=True)
    is_used = models.BooleanField(default=True, verbose_name="БУ")
    

    def __str__(self):
        return self.name

    class Meta:

        verbose_name = _('Товар')
        verbose_name_plural = _('Товары')


class ProductImage(models.Model):
    belongs_to = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images',
                                   verbose_name=_('Принадлежит продукту'))
    image_file = models.ImageField(
        upload_to='product_images', verbose_name=_('Изображение продукта'))

    def __str__(self):
        return self.image_file.name

    class Meta:

        verbose_name = _('Изображение товара')
        verbose_name_plural = _('Изображения товаров')


class Order(models.Model):
    operation_region = models.CharField(max_length=255, verbose_name=_('Регион эксплуатации'), blank=True)
    client_type = models.CharField(max_length=255, choices=ClientTypeEnum.choices, default=ClientTypeEnum.LEGAL_ENTITY,
                                   verbose_name=_('От лица'))
    organization_full_name = models.CharField(max_length=255, verbose_name=_('Полное наименование организации'),
                                              blank=True)
    contact_person = models.CharField(max_length=255, verbose_name=_('Контактное лицо'), blank=True)
    phone_number = models.CharField(
        max_length=255, verbose_name=_('Номер телефона'))
    email = models.EmailField(verbose_name=_('Почта'), blank=True)
    chosen_product = models.ForeignKey(
        Product, on_delete=models.DO_NOTHING, related_name='orders')
    origin = models.CharField(max_length=255, choices=constants.OrderOriginEnum.choices, verbose_name=_('Источник'))
    comments = models.TextField(verbose_name=_('Комментарии'))
    is_handled = models.BooleanField(
        default=False, verbose_name=_('Обработан'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Дата создания'))

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = _('Запрос КП')
        verbose_name_plural = _('Запросы КП')


class FAQ(models.Model):
    question = models.TextField(verbose_name=_('Вопрос'))
    answer = models.TextField(verbose_name=_('Ответ'))
    def __str__(self):
        return self.question

    class Meta:
        
        verbose_name = 'Часто задаваемый вопрос'
        verbose_name_plural = 'Часто задаваемые вопросы'


class Feedback(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Имя клиента'))
    company = models.CharField(max_length=255, verbose_name=_('Фирма'))
    feedback_text = models.TextField(verbose_name=_('Отзыв'))

    def __str__(self):
        return self.name

    class Meta:
        
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class ContactRequest(models.Model):
    phone_number = models.CharField(
        max_length=255, verbose_name=_('Номер телефона'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Дата создания'))
    info = models.TextField(
        max_length=500, verbose_name='Доп инфо', null=True, default=None)

    def __str__(self):
        return self.phone_number

    class Meta:
        
        verbose_name = 'Запрос на контакт'
        verbose_name_plural = 'Запросы на контакт'



def passgenerate():
    keys = '123456789qwertyuipasdfghjklzxcvbnmQWERTYUIPASDFGHJKLZXCVBNM'
    bit = 16
    bit2 = 0
    result = ''
    while bit > bit2:
        bit2 += 1
        result += random.choice(keys)
    return result

class Starter(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название', unique=True, default='Нет')
    key = models.CharField(max_length=16, verbose_name='Ключ', unique=True, default=passgenerate)
    link = models.CharField(max_length=100, verbose_name='Ссылка', unique=True, default=f'https://t.me/UnimedStoreBot?start=')

    def __str__(self):
        self.link = self.link + self.key
        return self.name

    class Meta:
        verbose_name = 'Промоутеры'
        verbose_name_plural = 'Промоутеры'

def create_starter(sender, **kwargs):
    if kwargs['signal']:
        kwargs['instance'].link = str(kwargs['instance'].link) + str(kwargs['instance'].key)
pre_save.connect(create_starter, sender=Starter)


class Tuser(models.Model):
    userid = models.CharField(max_length=50, verbose_name='Telegram ID')
    step = models.CharField(max_length=5, verbose_name='Шаг', default=1)
    phone = models.CharField(max_length=14, verbose_name='Телефон', null=True, blank=True)
    prestep = models.CharField(max_length=5, verbose_name='Предыдущее действие', null=True)
    from_starter = models.ForeignKey(Starter, on_delete=models.CASCADE, null=True, verbose_name='Канал / Пришел')

    def __str__(self):
        return self.userid

    class Meta:
        verbose_name = 'Телеграм пользователь'
        verbose_name_plural = 'Телеграм пользователи'




