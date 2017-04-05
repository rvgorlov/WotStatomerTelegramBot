import threading
import sys

from serverExch import *
from wgAPI import wgServerURL
from loggerFunc import log

isPolling = 'no'

# дескрипторы потоков
listenThread =  threading.Thread(target=internetListener)
reciverThread = threading.Thread(target=serversChecker)

if __name__ == '__main__':

    # Проверка соединения с интернетом
    if not checkConnection("8.8.8.8"):
        log("Нет доступа в интернет. Подключите.")
        sys.exit(1)

    # Проверка соединения с wargaming
    if not checkConnection(wgServerURL):
        log("Нет доступа до Wargaming")
        sys.exit(1)

    # Проверка настроек
    if len(config.servers) < 2:
        try:
            botLogic.polling()
        except:
            log("Бот отвалился")
            sys.exit(1)
    else: # Если настройки есть, запускаем потоки
        try:
            listenThread.start()
            reciverThread.start()

            listenThread.join()
            reciverThread.join()
        except:
            log("Exception (threads)")