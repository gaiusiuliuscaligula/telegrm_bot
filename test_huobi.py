import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import ccxt

# Установите токен вашего бота
bot_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'

# Создаем объект бота
bot = telepot.Bot(bot_token)

# Установите свои API-ключи Huobi
huobi_api_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'
huobi_api_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'

# Создаем объект Huobi
huobi_exchange = ccxt.huobipro({
    'apiKey': huobi_api_key,
    'secret': huobi_api_secret,
})

# Получаем список доступных символов (валютных пар) с Huobi
huobi_symbols = huobi_exchange.fetch_markets()
huobi_currency_pairs = [{'symbol': symbol['symbol'], 'name': symbol['symbol'].replace('/', '')} for symbol in huobi_symbols]

# Список валютных пар
currency_pairs = [
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

# Обработчик команды /start
def handle_start_command(chat_id):
    # Создаем меню с кнопками для выбора валютной пары
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=pair['name'], callback_data=f'pair_{pair["symbol"]}')] for pair in currency_pairs
    ])

    # Отправляем приветственное сообщение с меню выбора валютной пары
    bot.sendMessage(chat_id, 'Привет! Выберите валютную пару:', reply_markup=keyboard)

# Обработчик команды /get_price
def handle_get_price_command(chat_id, symbol):
    # Получение цены валютной пары с Huobi
    def get_huobi_price(symbol):
        ticker = huobi_exchange.fetch_ticker(symbol)
        if ticker is not None:
            huobi_price = ticker['last']
            return huobi_price
        return None

    # Получение цены валютной пары с Binance
    # ... (ваш код для получения цены с Binance)

    # Отправляем ответ пользователю
    huobi_price = get_huobi_price(symbol)
    if huobi_price is not None:
        bot.sendMessage(chat_id, f'Цена {symbol} на Huobi: {huobi_price}')
    else:
        bot.sendMessage(chat_id, f'Не удалось получить цену {symbol} на Huobi')

# Обработчик входящих сообщений
def handle_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        command = msg['text']

        if command == '/start':
            handle_start_command(chat_id)
        elif command.startswith('/get_price'):
            symbol = command.split(' ')[1].upper()
            handle_get_price_command(chat_id, symbol)

# Обработчик входящих callback-запросов
def handle_callback_query(msg):
    query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
    symbol = query_data.split('_')[1]

    handle_get_price_command(chat_id, symbol)

# Регистрируем обработчики
MessageLoop(bot, {
    'chat': handle_message,
    'callback_query': handle_callback_query
}).run_as_thread()

# Запускаем бесконечный цикл для обработки входящих сообщений
while True:
    pass