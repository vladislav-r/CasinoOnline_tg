import telebot 
from telebot import types
import time
from os import getenv

from check_res import Baraban


bot = telebot.TeleBot(getenv("casinoBotTest_TOKEN"), parse_mode=None)


startKBoard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
baraban = types.KeyboardButton(text="🎰 Крутить барабан")
basket = types.KeyboardButton(text="🏀 Бросить мяч")
startKBoard.add(baraban)

payback = types.InlineKeyboardMarkup()
payback1 = types.InlineKeyboardButton("Заказать выплату", callback_data='payback1')
payback.add(payback1)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}', reply_markup=startKBoard)

@bot.message_handler(commands=['help'])
def send_combinations(message):
    bot.send_message(message.chat.id, str(Baraban.slot_machine_value))

@bot.message_handler(content_types=['text'])
def sendDice(message):
    if message.text == "🎰 Крутить барабан":
        msg = bot.send_dice(message.chat.id, emoji="🎰")
        combination, priz = Baraban.check(msg.dice.value)
        a, b, c = combination
        time.sleep(1.5)
        bot.send_message(message.chat.id, f'Ваша комбинация: {msg.dice.value}\n{a} {b} {c}\nВыигрыш: {priz}', reply_markup=payback)
        
    elif message.text == "🏀 Бросить мяч":
        msg = bot.send_dice(message.chat.id, emoji="🏀")
        time.sleep(2)
        bot.send_message(message.chat.id, f'Ваша комбинация: {msg.dice.value}')


@bot.callback_query_handler(func=lambda call: True)
def on_send(call):
    if call.data == 'payback1':
        bot.send_message(call.message.chat.id, f'Ваш баланс: {Baraban.balance}')

bot.polling(none_stop=True)