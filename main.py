import socket
import wgAPI
import telebot
import config
import threading
import time

bot = telebot.TeleBot(config.telegramToken)
isPolling = 'no'

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
            print('Стартуем бота')
            isPolling = 'ok'
            bot.polling(none_stop=False, interval=1)
        except:
            print("Exception (polling)")

def internetListener():
    global isPolling
    soc = socket.socket()
    soc.bind(config.servers[config.current])
    soc.listen(len(config.servers))

    try:
        while 1:
            try:
                conn, addr = soc.accept()
                conData = str.encode(isPolling)
                conn.send(conData)
            except socket.error as e:
                print(e)
            except:
                print('except')
            finally:
                conn.close()
    finally:
        soc.close()

def serversChecker():
    soc = socket.socket()
    soc.settimeout(5)
    try:
        while 1:
            serversStatus = []

            for key in config.servers.keys():
                if key == config.current:
                    continue
                else:
                    try:
                        conn, addr = soc.connect( config.servers[key] )
                        data = conn.recv()
                        data = data.decode()
                        serversStatus.append(data)
                    except socket.error as e:
                        print(e)
                    except:
                        pass
            isworkServers = False

            for x in serversStatus:
                print(x)
                if x == 'ok':
                    print('Найден работающий бот')
                    workServers = True

            if not isworkServers:
                print('Запущенные боты не обнаружены')
                polling()
            else:
                print("Обнаружен работающий бот. Ожидаем его смерти.")

            time.sleep(20)

    except:
        print('except')

#pollingThread = threading.Thread(target=polling)
listenThread = threading.Thread(target=internetListener)
reciverThread = threading.Thread(target=serversChecker)

if __name__ == '__main__':
    try:
        #pollingThread.run()
        listenThread.start()
        reciverThread.start()

        listenThread.join()
        reciverThread.join()
        pass
    except:
        print("Exception (threads)")