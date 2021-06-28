from django.utils.translation import gettext_lazy as _


class ClientTypeEnum:
    LEGAL_ENTITY = 'legal_entity'
    INDIVIDUAL = 'individual'

    choices = (
        (LEGAL_ENTITY, _('Юридическое лицо')),
        (INDIVIDUAL, _('Физическое лицо')),
    )


class OrderOriginEnum:
    TELEGRAM_BOT = 'order_origin_telegram_bot'
    WEBSITE = 'order_origin_website'

    choices = (
        (TELEGRAM_BOT, _('Telegram чат-бот')),
        (WEBSITE, _('Веб-сайт')),
    )
