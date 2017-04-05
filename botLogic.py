import wgAPI
import telebot
import config
from loggerFunc import log


def polling():
    bot = telebot.TeleBot(config.telegramToken)

    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        bot.send_message(message.chat.id, "Здарова, танкист! Давай, пиши ник своего товарища...")
        log("Новый пользователь - " + str(message.chat.id))

    @bot.message_handler(func=lambda message: True, content_types=['text'])
    def echo_msg(message):
        log("Пользователь - " + str(message.chat.id) + " ищет " + message.text)
        bot.send_message(message.chat.id, "Поиск досье...")
        dossier = wgAPI.getUserDossier(message.text)
        if len(dossier) == 0:
            bot.send_message(message.chat.id, "Досье не найдено. Увы!")
        else:
            bot.send_message(message.chat.id, dossier)

    global isPolling
    while 1:
        try:
            log('Стартуем бота')
            isPolling = 'ok'
            bot.polling(none_stop=True, interval=1)
        except:
            log("Exception (polling)")