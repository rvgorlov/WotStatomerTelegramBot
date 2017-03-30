import wgAPI
import telebot
import config
import threading

bot = telebot.TeleBot(config.telegramToken)
isPolling = False

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Здарова, танкист! Давай, пиши ник своего товарища...")
    print("Новый пользователь - " + str(message.chat.id))

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_msg(message):
    bot.send_message(message.chat.id, "Поиск досье...")
    dossier = wgAPI.getUserDossier(message.text)
    if len(dossier) == 0:
        bot.send_message(message.chat.id, "Досье не найдено. Увы!")
    else:
        bot.send_message(message.chat.id, dossier)
    print("Пользователь - " + str(message.chat.id) + " ищет " + message.text)

def polling():
    global bot
    global isPolling
    while 1:
        try:
            isPolling = True
            bot.polling(none_stop=False, interval=1)
        except:
            print("Exception")



pollingThread = threading.Thread(target=polling)

if __name__ == '__main__':
    pollingThread.run()