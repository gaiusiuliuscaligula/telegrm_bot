import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import ccxt
from binance.client import Client

# Установите токен вашего бота
bot_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'

# Установите свои API-ключи Huobi
huobi_api_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'
huobi_api_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'

# Установите свои API-ключи Binance
binance_api_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'
binance_api_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'

# Создаем объект бота
bot = telepot.Bot(bot_token)

# Создаем объект Huobi
huobi_exchange = ccxt.huobipro({
    'apiKey': huobi_api_key,
    'secret': huobi_api_secret,
})

# Создаем объект Binance
binance_client = Client(binance_api_key, binance_api_secret)

# Получаем список доступных символов (валютных пар) с Huobi
huobi_symbols = huobi_exchange.fetch_markets()
huobi_currency_pairs = [{'symbol': symbol['symbol'], 'name': symbol['symbol'].replace('/', '')} for symbol in huobi_symbols]

# Список валютных пар
huobi_currency_pairs = [
    {'symbol': 'btcusdt', 'name': 'BTC/USDT'},
    {'symbol': 'ethusdt', 'name': 'ETH/USDT'},
    {'symbol': 'bnbusdt', 'name': 'BNB/USDT'},
    {'symbol': 'ltcusdt', 'name': 'LTC/USDT'},
    {'symbol': 'xrpusdt', 'name': 'XRP/USDT'},
    {'symbol': 'dogeusdt', 'name': 'DOGE/USDT'},
    {'symbol': 'adausdt', 'name': 'ADA/USDT'},
    {'symbol': 'linkusdt', 'name': 'LINK/USDT'},
    {'symbol': 'dotusdt', 'name': 'DOT/USDT'},
    {'symbol': 'bchusdt', 'name': 'BCH/USDT'},
]

# Получаем список доступных символов (валютных пар) с Binance
binance_symbols = binance_client.get_exchange_info()['symbols']
binance_currency_pairs = [{'symbol': symbol['symbol'], 'name': symbol['symbol'].replace('/', '')} for symbol in binance_symbols]

# Список валютных пар
binance_currency_pairs = [
    {'symbol': 'BTCUSDT', 'name': 'BTC/USDT'},
    {'symbol': 'ETHUSDT', 'name': 'ETH/USDT'},
    {'symbol': 'BNBUSDT', 'name': 'BNB/USDT'},
    {'symbol': 'LTCUSDT', 'name': 'LTC/USDT'},
    {'symbol': 'XRPUSDT', 'name': 'XRP/USDT'},
    {'symbol': 'DOGEUSDT', 'name': 'DOGE/USDT'},
    {'symbol': 'ADAUSDT', 'name': 'ADA/USDT'},
    {'symbol': 'LINKUSDT', 'name': 'LINK/USDT'},
    {'symbol': 'DOTUSDT', 'name': 'DOT/USDT'},
    {'symbol': 'BCHUSDT', 'name': 'BCH/USDT'},
]

# Обработчик команды /start
def handle_start_command(chat_id):
    # Создаем меню с кнопками для выбора валютной пары
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=pair['name'], callback_data=f'{pair["symbol"]}_price')] for pair in huobi_currency_pairs
    ])

    # Отправляем приветственное сообщение с меню выбора валютной пары
    bot.sendMessage(chat_id, 'Привет! Выберите валютную пару:', reply_markup=keyboard)

# Обработчик входящих callback-запросов
def handle_callback_query(msg):
    query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')

    if query_data.endswith('_price'):
        symbol = query_data.replace('_price', '')
        handle_get_price_command(chat_id, symbol)

# Обработчик команды /get_price
def handle_get_price_command(chat_id, symbol):
    # Получение цены валютной пары с Huobi
    huobi_ticker = huobi_exchange.fetch_ticker(symbol)
    huobi_price = huobi_ticker['last'] if huobi_ticker else 'Не удалось получить цену на Huobi'

    # Получение цены валютной пары с Binance
    binance_ticker = binance_client.get_symbol_ticker(symbol=symbol.upper())
    binance_price = binance_ticker['price'] if binance_ticker else 'Не удалось получить цену на Binance'

    # Отправляем сообщение с ценами
    bot.sendMessage(chat_id, f'Цена {symbol} на Huobi: {huobi_price}\nЦена {symbol} на Binance: {binance_price}')

# Обработчик входящих сообщений
def handle_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        command = msg['text']

        if command == '/start':
            handle_start_command(chat_id)

# Регистрируем обработчики
MessageLoop(bot, {
    'chat': handle_message,
    'callback_query': handle_callback_query
}).run_as_thread()

# Запускаем бесконечный цикл для обработки входящих сообщений
while True:
    pass