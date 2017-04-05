import socket
import config
import time
import botLogic
from loggerFunc import log

def checkConnection(hostname):
    from os import system as osSystem
    from platform import system as platSystem

    if platSystem() == 'Windows':
        response = osSystem("ping " + hostname + " -n 1")
    else:
        response = osSystem("ping -c 1 " + hostname)

    if response == 0:
        log(str(hostname) + ' is up!')
        return True
    else:
        log(str(hostname) + " is down!")
        return False

def internetListener():
    if len(config.servers) < 2:
        return

    global isPolling
    soc = socket.socket()
    soc.bind(config.servers[config.current])
    soc.listen(len(config.servers))
    log('Слушаем ' + str(config.servers[config.current]))

    try:
        while 1:
            try:
                conn, addr = soc.accept()
                data = str.encode(isPolling)
                conn.send(data)
            except socket.error as e:
                log(e)
            except:
                log('except')
            finally:
                conn.close()
    finally:
        soc.close()


def serversChecker():
    try:
        while 1:
            serversStatus = []

            log('Проверяем сервера по списку')
            for key in config.servers.keys():
                if key == config.current:
                    continue
                else:
                    log('Стучимся в ' + str(config.servers[key] ))
                    try:
                        if not checkConnection(config.servers[key][0]):
                            continue
                        soc = socket.socket()
                        soc.settimeout(10)
                        soc.connect(config.servers[key])
                        data = soc.recv(1024)
                        serversStatus.append(data.decode())
                        soc.close()
                    except socket.error as e:
                        log(e)
                    except socket.herror as e:
                        log(e)
                    except socket.gaierror as e:
                        log(e)
                    except socket.timeout as e:
                        log(e)
                    except:
                        log('except')

            isworkServers = False

            for x in serversStatus:
                if x == 'ok':
                    log('Найден работающий бот')
                    isworkServers = True

            if not isworkServers:
                log('Запущенные боты не обнаружены')
                botLogic.polling()
            else:
                log("Обнаружен работающий бот. Ожидаем его смерти.")

            time.sleep(10)
    except:
        log('except')