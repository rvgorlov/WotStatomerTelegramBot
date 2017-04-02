import socket
import wgAPI
import telebot
import config
import threading
import time

isPolling = 'no'

def polling():
    bot = telebot.TeleBot(config.telegramToken)

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

    global isPolling
    while 1:
        try:
            print('Стартуем бота')
            isPolling = 'ok'
            bot.polling(none_stop=True, interval=1)
        except:
            print("Exception (polling)")

def internetListener():
    if len(config.servers) < 2:
        return

    global isPolling
    soc = socket.socket()
    soc.bind(config.servers[config.current])
    soc.listen(len(config.servers))
    print('Слушаем ' + str(config.servers[config.current]))

    try:
        while 1:
            try:
                conn, addr = soc.accept()
                data = str.encode(isPolling)
                conn.send(data)
            except socket.error as e:
                print(e)
            except:
                print('except')
            finally:
                conn.close()
    finally:
        soc.close()


def serversChecker():

    if len(config.servers) < 2:
        polling()

    try:
        while 1:
            serversStatus = []

            print('Проверяем сервера по списку')
            for key in config.servers.keys():
                if key == config.current:
                    continue
                else:
                    try:

                        soc = socket.socket()
                        soc.settimeout(10)
                        soc.connect(config.servers[key])
                        data = soc.recv(1024)
                        serversStatus.append(data.decode())
                        soc.close()
                    except socket.error as e:
                        print(e)
                    except socket.herror as e:
                        print(e)
                    except socket.gaierror as e:
                        print(e)
                    except socket.timeout as e:
                        print(e)
                    except:
                        print('except')

            isworkServers = False

            for x in serversStatus:
                if x == 'ok':
                    print('Найден работающий бот')
                    isworkServers = True

            if not isworkServers:
                print('Запущенные боты не обнаружены')
                polling()
            else:
                print("Обнаружен работающий бот. Ожидаем его смерти.")

            time.sleep(5)
    except:
        print('except')

listenThread = threading.Thread(target=internetListener)
reciverThread = threading.Thread(target=serversChecker)

if __name__ == '__main__':
    try:
        listenThread.start()
        reciverThread.start()

        listenThread.join()
        reciverThread.join()
        pass
    except:
        print("Exception (threads)")