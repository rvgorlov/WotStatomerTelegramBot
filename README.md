### WotStatomerTelegramBot
 The bot shows the statistics of your comrades

Getting started.

For linux:

1. Install:

```terminal
sudo apt-get update
sudo apt-get install python3 python3-pip
sudo pip3 install pyTelegramBotAPI
```

2. Create a file config.py and put it in the folder with the main

```python
telegramToken = ""
wotAPIToken = ""

DEBUG = True

# number of current servers
current = 1
# connectio info for servers
PORT = 9050
servers = {1:('192.168.0.240',PORT), 2:('192.168.0.162', PORT)}
```
