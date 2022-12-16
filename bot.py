import telebot
import Config


bot=telebot.TeleBot(Config.token)
weigh=0
norma=0
drinked=0
d=0

def calculation(x):
    return 1500+(x-20)*20


@bot.message_handler(commands=['start'])
def start_command(message):
    """
    функция для обработки комманды start
    """
    sti=open('hi.webp','rb')
    bot.send_sticker(message.chat.id,sti)
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("/help")
    btn2 = telebot.types.KeyboardButton("/info")
    btn3= telebot.types.KeyboardButton('/calculate')
    markup.add(btn1, btn2, btn3)

    bot.send_message(
        message.chat.id,
        "Приветствую! Этот бот поможет тебе соблюдать питьевой режим.\n" +
        "Получить помощь, напишите комманду /help или нажмите на кнопку снизу\n"+
        "Получить информацию, напишите команду /info или нажмите на кнопку снизу.\n"+
        'Для того чтобы начать отслеживать потребление нажмите на кнопку с командой /calcualate',
        reply_markup=markup
    )

@bot.message_handler(commands=['help'])
def help_command(message):
    """
    функция для обработки команды help
    """
    keyboard= telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            'Напишите разработчику', url='https://t.me/icameisawicameisaw'
        )
    )
    bot.send_message(
        message.chat.id,
        'По кнопке ниже можно написать разработчику бота.',
        reply_markup=keyboard
        )


@bot.message_handler(commands=['info'])
def info_command(message):
    """
    функция для обработки команды info
    """
    bot.send_message(
        message.chat.id,
        'Поддержание водного баланса очень важно для человеческого организма.\n'+
        'Вода помогает поддерживать тонус мышц, выводит вредоносные токсины,\n'+
        'Очищает и увлажняет кожу, а также уменьшает риск образования тромбов.\n'+
        'Норма воды рассчитывается по формулe: Норма(мл)=1500+(вес-20)*20',
    )


@bot.message_handler(content_types=['text'])
def start(message):
    """
    функция для обработки сообщений от пользователя после ввода определенных команд
    """
    global norma,drinked
    if message.text=='/calculate':
        bot.send_message(message.from_user.id, "Сколько вы весите?")
        bot.register_next_step_handler(message, calc)
        norma=0
        drinked=0
    if message.text == '/drink':
        bot.send_message(
            message.from_user.id,
            'Напишите в миллитрах сколько вы выпили.'
        )
        bot.register_next_step_handler(message, drinking)


def calc(message):
    """
    функция для расчета нормы воды
    """
    global weigh
    global norma
    while weigh==0:
        try:
            weigh = int(message.text)
        except Exception:
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = telebot.types.KeyboardButton("/calculate")
            markup.add(btn1)
            bot.send_message(
                message.from_user.id,
                'Цифрами, пожалуйста',
                reply_markup=markup,
            )
            break
        else:
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = telebot.types.KeyboardButton("/drink")
            markup.add(btn1)
            bot.send_message(
                message.from_user.id,
                'Вы весите '+ str(weigh)+' киллограмм. Ваша дневная норма '+ str(calculation(weigh)) +' миллитров воды.\n'+
                'Для того чтобы следить за количеством выпитой воды напишите команду /drink или нажмите на кнопку снизу',
                reply_markup=markup
            )
    norma=calculation(weigh)
    weigh=0


def drinking(message):
    """
    функиця для отслеживания количества выпитой воды
    """
    global norma, drinked,d
    try:
        d = int(message.text)
    except Exception:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = telebot.types.KeyboardButton("/drink")
        markup.add(btn1)
        bot.send_message(message.from_user.id, 'Цифрами, пожалуйста',reply_markup=markup)
    else:
        if norma-(drinked+d)>0:
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = telebot.types.KeyboardButton("drink")
            markup.add(btn1)
            bot.send_message(
                message.from_user.id,
                'Вы выпили '+str(d)+' миллитров воды.\n'+
                'Осталось выпить '+str(norma-(drinked+d)),
                reply_markup=markup
            )
        else:
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = telebot.types.KeyboardButton("calculate")
            markup.add(btn1)
            bot.send_message(
                message.from_user.id,
                'За сегодня вы выпили на '+str(abs(norma-(drinked+d)))+' миллитров воды больше нормы.\n'+
                'Превышение нормы может навредить вашему организму.\n'+
                'Нажмите кнопочку calculate, если наступил следующий день.',
                reply_markup=markup
            )
    drinked+=d
    d=0

    
bot.polling(none_stop=True)
"""Фукнция, чтобы бот постоянно спрашивал сервера Telegram на наличие новых сообщений"""
