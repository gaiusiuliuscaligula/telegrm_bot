import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from binance.client import Client
import ccxt

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


# Получаем список доступных символов (валютных пар) с Binance
binance_symbols = binance_client.get_exchange_info()['symbols']
binance_currency_pairs = [{'symbol': symbol['symbol'], 'name': symbol['symbol'].replace('/', '')} for symbol in binance_symbols]


# Обработчик команды /start
def handle_start_command(chat_id):
    # Создаем меню с кнопками выбора биржи
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Binance', callback_data='binance')],
        [InlineKeyboardButton(text='Huobi', callback_data='huobi')],
    ])

    # Отправляем приветственное сообщение с меню выбора биржи
    bot.sendMessage(chat_id, 'Привет! Выберите биржу:', reply_markup=keyboard)


# Обработчик входящих callback-запросов
def handle_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

    if query_data == 'binance':
        # Создаем таблицу с кнопками валютных пар Binance
        buttons = create_currency_pair_buttons(binance_currency_pairs, 'binance')

        # Создаем клавиатуру с кнопками валютных пар Binance
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

        # Отправляем клавиатуру с кнопками валютных пар Binance
        bot.sendMessage(from_id, 'Выберите валютную пару Binance:', reply_markup=keyboard)

    elif query_data == 'huobi':
        # Создаем таблицу с кнопками валютных пар Huobi
        buttons = create_currency_pair_buttons(huobi_currency_pairs, 'huobi')

        # Создаем клавиатуру с кнопками валютных пар Huobi
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

        # Отправляем клавиатуру с кнопками валютных пар Huobi
        bot.sendMessage(from_id, 'Выберите валютную пару Huobi:', reply_markup=keyboard)

    elif query_data.startswith('pair:'):
        # Извлекаем символ валютной пары из callback_data
        symbol = query_data.split(':')[1]

        if query_data.startswith('pair:binance:'):
            # Получаем цену валютной пары с Binance
            price = get_binance_price(symbol)

        elif query_data.startswith('pair:huobi:'):
            # Получаем цену валютной пары с Huobi
            price = get_huobi_price(symbol)

        # Отправляем цену валютной пары
        bot.sendMessage(from_id, f'Цена валютной пары {symbol}: {price}')

    elif query_data.startswith('next:'):
        # Извлекаем данные из callback_data
        exchange, offset = query_data.split(':')[1:]

        if exchange == 'binance':
            # Получаем следующие 10 валютных пар Binance
            buttons = create_currency_pair_buttons(binance_currency_pairs[int(offset):int(offset) + 10], exchange)

        elif exchange == 'huobi':
            # Получаем следующие 10 валютных пар Huobi
            buttons = create_currency_pair_buttons(huobi_currency_pairs[int(offset):int(offset) + 10], exchange)

        # Создаем клавиатуру с кнопками следующих валютных пар
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

        # Отправляем клавиатуру с кнопками следующих валютных пар
        bot.sendMessage(from_id, f'Выберите валютную пару {exchange.capitalize()}:', reply_markup=keyboard)


# Функция для создания кнопок с валютными парами
def create_currency_pair_buttons(currency_pairs, exchange):
    buttons = []

    for i in range(0, len(currency_pairs), 5):
        row = []

        for pair in currency_pairs[i:i + 5]:
            callback_data = f'pair:{exchange}:{pair["symbol"]}'
            button = InlineKeyboardButton(text=pair['name'], callback_data=callback_data)
            row.append(button)

        buttons.append(row)

    # Добавляем кнопку "Продолжить" для получения следующих валютных пар
    offset = len(currency_pairs)
    next_button = InlineKeyboardButton(text='Продолжить', callback_data=f'next:{exchange}:{offset}')
    buttons.append([next_button])

    return buttons


# Функция для получения цены валютной пары с Binance
def get_binance_price(symbol):
    ticker = binance_client.get_symbol_ticker(symbol=symbol)
    price = ticker['price']
    return price


# Функция для получения цены валютной пары с Huobi
def get_huobi_price(symbol):
    ticker = huobi_exchange.fetch_ticker(symbol)
    price = ticker['last']
    return price


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