import telebot
from telebot import types
import random
from config import TOKEN


database = {}
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        touch_line = types.KeyboardButton('Линейные')
        touch_play = types.KeyboardButton('Игры 🎲')
        markup.add(touch_line, touch_play)
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!✋ У тебя проблемы с уравнениями?👎 '
                                          f'Я бот,который может решить твои уравнения!😜 '
                                          f'Порекомендуй меня друзьям,обязательно!', reply_markup=markup)
    except:
        pass


@bot.message_handler(content_types=['text'])
def manager_commands(message):
    try:
        if message.text == 'Линейные':
            answer = bot.send_message(message.chat.id, 'Введите уравнение в одну строку: ',
                                      reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(answer, doing_line)
        elif message.text.split()[0] == 'Игры':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            touch_game1 = types.KeyboardButton('Угадай число!')
            touch_game2 = types.KeyboardButton('Орел и решка!')
            touch_game3 = types.KeyboardButton('Загадай число!')
            markup.add(touch_game1, touch_game2, touch_game3)
            bot.send_message(message.chat.id, 'Выберете игру, в которую хотите поиграть', reply_markup=markup)

        elif message.text == 'Угадай число!' or message.text == 'Угадать еще раз':
            answer = bot.send_message(message.chat.id, 'Угадай мое число от 1 до 10!',
                                      reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(answer, random_num)

        elif message.text == 'Орел и решка!' or message.text == 'Попробовать еще раз':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            touch_eagle = types.KeyboardButton('🦅')
            touch_coin = types.KeyboardButton('🌰')
            markup.add(touch_eagle, touch_coin)
            answer = bot.send_message(message.chat.id, 'Выберете: Орел или Решка?', reply_markup=markup)
            bot.register_next_step_handler(answer, eagle_or_coin_game)

        elif message.text == 'Загадай число!':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            touch_bigger = types.KeyboardButton('Больше')
            touch_smaller = types.KeyboardButton('Меньше')
            touch_yes = types.KeyboardButton('Да')
            touch_back = types.KeyboardButton('На главную')
            markup.add(touch_bigger, touch_smaller, touch_yes, touch_back)
            database[message.chat.id] = '1 1000 1 500'
            answer = bot.send_message(message.chat.id, 'Ваше число 500?', reply_markup=markup)
            bot.register_next_step_handler(answer, binary_search)

        elif message.text == 'На главную':
            send_welcome(message)
    except:
        send_welcome(message)


def random_num(message):
    try:
        pc_digit = random.randint(1, 10)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        touch_replay = types.KeyboardButton('Угадать еще раз')
        touch_back_to_home = types.KeyboardButton('На главную')
        markup.add(touch_replay, touch_back_to_home)
        if int(message.text) == pc_digit:
            bot.send_message(message.chat.id, 'Вы выиграли! Я не ожидал от вас такого результата!', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, f'Вы проиграли! Мое число {pc_digit}', reply_markup=markup)
    except:
        send_welcome(message)


def eagle_or_coin_game(message):
    try:
        pc_choice = random.choice(['🦅', '🌰'])
        if pc_choice == '🦅':
            bot.send_message(message.chat.id, '🪙')
        else:
            bot.send_message(message.chat.id, '🌰')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        touch_replay = types.KeyboardButton('Попробовать еще раз')
        touch_back_to_home = types.KeyboardButton('На главную')
        markup.add(touch_replay, touch_back_to_home)
        if pc_choice == message.text:
            bot.send_message(message.chat.id, 'Поздравляю! Вы выиграли!', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'К сожалению, вы проиграли!', reply_markup=markup)
    except:
        send_welcome(message)


def binary_search(message):
    try:
        if message.text == 'Да':
            bot.send_message(message.chat.id, f'Я угадал Ваше число за {database[message.chat.id].split()[2]} попыток.')
            del database[message.chat.id]
            return send_welcome(message)

        elif message.text == 'Больше':
            foo = database[message.chat.id].split()
            ready = (int(foo[3]) + int(foo[1])) // 2
            database[message.chat.id] = f'{foo[3]} {foo[1]} {int(foo[2]) + 1} {ready}'
            answer = bot.send_message(message.chat.id, f'Ваше число {ready}?')
            bot.register_next_step_handler(answer, binary_search)

        elif message.text == 'Меньше':
            foo = database[message.chat.id].split()
            ready = (int(foo[0]) + int(foo[3])) // 2
            database[message.chat.id] = f'{foo[0]} {foo[3]} {int(foo[2]) + 1} {ready}'
            answer = bot.send_message(message.chat.id, f'Ваше число {ready}?')
            bot.register_next_step_handler(answer, binary_search)

        elif message.text == 'На главную':
            send_welcome(message)

        else:
            answer = bot.send_message(message.chat.id, 'Отвечай кнопками!')
            bot.register_next_step_handler(answer, binary_search)
    except:
        send_welcome(message)


def doing_line(message):
    try:
        first, second = message.text.split('=')
        digits_left = 0
        for i in first.split():
            if i.isdigit():
                if first.split()[first.split().index(i)-1] == '+' or first.split().index(i) == 0:
                    digits_left += int(i)
                elif first.split()[first.split().index(i)-1] == '-':
                    digits_left -= int(i)
        if len(second.split()) > 1:
            digits_right = 0
            for i in second.split():
                if i.isdigit():
                    if second.split()[second.split().index(i) - 1] == '+' or second.split().index(i) == 0:
                        digits_right += int(i)
                    elif second.split()[second.split().index(i) - 1] == '-':
                        digits_right -= int(i)
            ready = digits_right + -digits_left
        else:
            ready = int(second) + -digits_left
        bot.send_message(message.chat.id, f'Ответ: x = {ready}')
    except:
        send_welcome(message)


if __name__ == '__main__':
    bot.polling(non_stop=True)
