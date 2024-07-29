from telebot import TeleBot, types
import requests
from worker.tasks import handle_request as celery_handle_request
import os
from dotenv import load_dotenv

dotenv_path = '/.env'

load_dotenv()

TOKEN = os.getenv('TOKEN')
API_URL = os.getenv('API_URL')

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    welcome_text = (f"Привет {message.from_user.first_name}! \nЯ - {bot.get_me().first_name}!"
                    f"\nЯ могу предсказать стоимость акций на 5 дней вперед"
                    f"\nДля помощи пиши /help")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button_1 = types.KeyboardButton('Регистрация')
    button_2 = types.KeyboardButton('Войти в аккаунт')
    markup.add(button_1, button_2)

    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, "Доступные команды:\n"
                                      "/start - Начать взаимодействие\n"
                                      "/help - Показать справочную информацию\n")


@bot.message_handler(func=lambda message: message.text == 'Регистрация')
def register_message(message):
    bot.send_message(message.chat.id, "Введите логин")
    bot.register_next_step_handler(message, get_username_register)


def get_username_register(message):
    username = message.text
    bot.send_message(message.chat.id, "Введите пароль")
    bot.register_next_step_handler(message, get_password_register, username)


def get_password_register(message, username):
    password = message.text
    bot.send_message(message.chat.id, "Введите email")
    bot.register_next_step_handler(message, get_email_register, username, password)


def get_email_register(message, username, password):
    email = message.text
    bot.send_message(message.chat.id, "Введите имя")
    bot.register_next_step_handler(message, get_first_register, username, password, email)


def get_first_register(message, username, password, email):
    first_name = message.text
    bot.send_message(message.chat.id, "Введите фамилию")
    bot.register_next_step_handler(message, get_complete_register, username, password, email, first_name)


def get_complete_register(message, username, password, email, first_name):
    last_name = message.text
    json_raw = {
        "username": username,
        "password": password,
        "email": email,
        "first_name": first_name,
        "last_name": last_name
    }
    request = requests.post(url=f"{API_URL}/users/signup/", json=json_raw)
    if request.status_code == 200:
        bot.send_message(message.chat.id, "Вы успешно зарегистрировались!")
    else:
        bot.send_message(message.chat.id, f"Ошибка регистрации: неверный ответ сервера. Status code: {request.status_code}")


@bot.message_handler(func=lambda message: message.text == 'Войти в аккаунт')
def login_message(message):
    bot.send_message(message.chat.id, "Введите почту")
    bot.register_next_step_handler(message, get_username_login)


def get_username_login(message):
    email = message.text
    bot.send_message(message.chat.id, "Введите пароль")
    bot.register_next_step_handler(message, complete_login, email)


def complete_login(message, email):
    password = message.text
    json_raw = {
        "email": email,
        "password": password
    }
    request = requests.post(url=f"{API_URL}/users/signin/", json=json_raw)
    if request.status_code == 200:
        bot.send_message(message.chat.id, "Вы успешно вошли в систему!")

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        button_1 = types.KeyboardButton('Пополнить баланс')
        button_2 = types.KeyboardButton('Посмотреть баланс')
        button_3 = types.KeyboardButton('Сделать запрос')
        button_4 = types.KeyboardButton('История запросов')
        button_5 = types.KeyboardButton('Выйти из профиля')
        markup.add(button_1, button_2, button_3, button_4, button_5)

        bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)

    elif request.status_code == 500:
        bot.send_message(message.chat.id, "Неправильный пользователь или пароль. Попробуйте еще раз.")
    else:
        bot.send_message(message.chat.id, f"Ошибка входа: {request.json().get('detail', 'Ошибка входа')}")


@bot.message_handler(func=lambda message: message.text == "Пополнить баланс")
def add_balance(message):
    bot.send_message(message.chat.id, 'Введите сумму')
    bot.register_next_step_handler(message, add_money)


def add_money(message):
    amount = float(message.text)
    request = requests.post(f"{API_URL}/balances/add_balance?amount={amount}")
    if request.status_code == 200:
        bot.send_message(message.chat.id, "Ваш баланс успешно пополнен!")
    elif request.status_code == 500:
        bot.send_message(message.chat.id, "Вы не авторизованы. Пожалуйста, войдите в аккаунт.")
    else:
        bot.send_message(message.chat.id, f"Ошибка пополнения: {request.json().get('detail', 'Ошибка пополнения')}")


@bot.message_handler(func=lambda message: message.text == "Посмотреть баланс")
def get_balance(message):
    request = requests.get(f"{API_URL}/balances/balance")
    if request.status_code == 200:
        balance = request.json().get('amount')
        bot.send_message(message.chat.id, f'Ваш баланс: {balance}')
    elif request.status_code == 500:
        bot.send_message(message.chat.id, "Вы не авторизованы. Пожалуйста, войдите в аккаунт.")
    else:
        bot.send_message(message.chat.id, f"Ошибка: {request.json().get('detail', 'Ошибка')}")


@bot.message_handler(func=lambda message: message.text == "Сделать запрос")
def insert_data(message):
    bot.send_message(message.chat.id, "Введите дату в формате YYYY-MM-DD")
    bot.register_next_step_handler(message, handle_request)


def handle_request(message):
    data = message.text
    response = requests.get(f"{API_URL}/users/current_user")
    if response.status_code == 200:
        user_data = response.json()
        current_user = user_data.get("username")
    else:
        bot.send_message(message.chat.id, "Вы не авторизованы. Пожалуйста, войдите в аккаунт.")
        return None

    celery_handle_request.apply_async(args=[data, 'prophet_model', current_user])
    bot.send_message(message.chat.id, "Ваш запрос был отправлен на обработку. Вы получите уведомление о завершении.")


def format_prediction(predictions):
    formatted_output = ""
    for prediction in predictions:
        date = prediction.get('ds')
        yhat = prediction.get('yhat')
        yhat_lower = prediction.get('yhat_lower')
        yhat_upper = prediction.get('yhat_upper')
        formatted_output += f"Дата: {date}\n"
        formatted_output += f"Прогноз: {yhat}\n"
        formatted_output += f"Диапазон: [{yhat_lower}, {yhat_upper}]\n\n"
    return formatted_output


@bot.message_handler(func=lambda message: message.text == "История запросов")
def transaction_history(message):
    response = requests.get(url=f"{API_URL}/users/transaction_history")
    if response.status_code == 200:
        transactions = response.json()
        for transaction in transactions:
            bot.send_message(message.chat.id,
                             f"Дата: {transaction['data']}\nПрогноз: {transaction['prediction']}\nПотрачено: {transaction['spent_money']}")
    elif response.status_code == 500:
        bot.send_message(message.chat.id, "Вы не авторизованы. Пожалуйста, войдите в аккаунт.")
    else:
        bot.send_message(message.chat.id,
                         f"Ошибка получения истории: {response.json().get('detail', 'Ошибка получения истории')}")


@bot.message_handler(func=lambda message: message.text == "Выйти из профиля")
def logout(message):
    request = requests.post(url=f"{API_URL}/users/logout")
    if request.status_code == 200:
        bot.send_message(message.chat.id, "Вы успешно вышли из профиля")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        button_1 = types.KeyboardButton('Регистрация')
        button_2 = types.KeyboardButton('Войти в аккаунт')
        markup.add(button_1, button_2)

        bot.send_message(message.chat.id, 'Выберите действие', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Ошибка')


bot.infinity_polling(none_stop=True)
