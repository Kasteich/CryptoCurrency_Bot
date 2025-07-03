from aiogram import Dispatcher
import logging
from .low_high import register_handlers_low_high
from .convert import register_handlers_convert
from .start import register_handlers_start
from .help import register_handlers_help
from .price import register_handlers_price
from .currencies import register_handlers_currencies
from .history import register_handlers_history
from .crypto_currencies import register_handlers_crypto_currencies

logger = logging.getLogger(__name__)

def register_handlers(dp: Dispatcher):
    logger.info("Начинается регистрация обработчиков...")
    register_handlers_start(dp)
    register_handlers_help(dp)
    register_handlers_price(dp)
    register_handlers_currencies(dp)
    register_handlers_convert(dp)
    register_handlers_history(dp)
    register_handlers_crypto_currencies(dp)
    register_handlers_low_high(dp)
    logger.info("Регистрация всех обработчиков завершена!")