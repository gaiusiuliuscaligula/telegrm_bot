import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from binance.client import Client

# Установите токен вашего бота
bot_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'

# Установите свои API-ключи Binance
binance_api_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'
binance_api_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'

# Создаем объект бота
bot = telepot.Bot(bot_token)

# Создаем объект Binance
binance_client = Client(binance_api_key, binance_api_secret)

# Получаем список доступных символов (валютных пар) с Binance
binance_symbols = binance_client.get_exchange_info()['symbols']
binance_currency_pairs = [{'symbol': symbol['symbol'], 'name': symbol['symbol'].replace('/', '')} for symbol in binance_symbols]

# Список валютных пар
currency_pairs = [
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
        [InlineKeyboardButton(text=pair['name'], callback_data=f'pair_{pair["symbol"]}')] for pair in currency_pairs
    ])

    # Отправляем приветственное сообщение с меню выбора валютной пары
    bot.sendMessage(chat_id, 'Привет! Выберите валютную пару:', reply_markup=keyboard)

# Обработчик команды /get_price
def handle_get_price_command(chat_id, symbol):
    # Получение цены валютной пары с Huobi
    # ... (ваш код для получения цены с Huobi)

    # Получение цены валютной пары с Binance
    def get_binance_price(symbol):
        ticker = binance_client.get_symbol_ticker(symbol=symbol)
        if ticker is not None and 'price' in ticker:
            binance_price = ticker['price']
            return binance_price
        return None

    # Отправляем ответ пользователю
    binance_price = get_binance_price(symbol)
    if binance_price is not None:
        bot.sendMessage(chat_id, f'Цена {symbol} на Binance: {binance_price}')
    else:
        bot.sendMessage(chat_id, f'Не удалось получить цену {symbol} на Binance')

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
