import requests
import config
from  math import ceil

wgUserListURL = "https://api.worldoftanks.ru/wot/account/list/"
wgUserInfoURL = "https://api.worldoftanks.ru/wot/account/info/"

wgServerURL = "api.worldoftanks.ru"

def getUserNameAndID(userName):
    try:
        UserInfo = {"application_id": config.wotAPIToken,
                    "search": userName,
                    "limit": "1"}
        request = requests.post(wgUserListURL, data=UserInfo)
        result = request.json()

        if result['status'] == 'ok':
            temp = result['data']
            return temp[0]
        else:
            return ''
    except requests.exceptions.RequestException:
        return ''
    except:
        return ''


def getUserStat(userID):
    try:
        UserInfo = {"application_id": config.wotAPIToken,
                    "account_id": userID}
        request = requests.post(wgUserInfoURL, data=UserInfo)
        result = request.json()

        if result['status'] == 'ok':
            temp = result['data']
            temp = temp[str(userID)]
            temp = temp['statistics']
            return temp['all']
        else:
            return ''
    except requests.exceptions.RequestException:
        return ''
    except:
        return ''


def getUserDossier(userName):
    userNameAndID = getUserNameAndID(userName)

    if len(userNameAndID) == 0:
        return ''

    userID = userNameAndID['account_id']
    if userID is '':
        print('\n ERROR - user ID')

    userName = userNameAndID['nickname']
    if userName is '':
        print('\n ERROR - user name')

    userStat = getUserStat(userID)
    if len(userStat) == 0:
        return ''

    userWinProc = userStat['wins'] / (userStat['battles'] / 100)
    userWins = userStat['wins']
    userLosses = userStat['losses']
    userSumBattles = userStat['battles']
    userMaxFrags = userStat['max_frags']

    Dossier = "Досье на " + userName + "\n" + "\n"
    Dossier = Dossier + "Wargaming_ID: " + str(userID) + "\n"
    Dossier = Dossier + "Процент побед: " + str( round(userWinProc, 2) ) + "\n"
    Dossier = Dossier + "Победы: " + str(userWins) + "\n"
    Dossier = Dossier + "Поражения: " + str(userLosses) + "\n"
    Dossier = Dossier + "Всего боёв: " + str(userSumBattles) + "\n"
    Dossier = Dossier + "Максимум сжёг за бой: " + str(userMaxFrags) + "\n\n"

    if userSumBattles < 3000:
        Dossier = Dossier + "Судя по колличеству боев, товарищ ещё совсем зелёный. Не о чём судить ещё. Не показал себя. "
    elif (ceil(userWinProc) < 50) :
        Dossier = Dossier + "Судя по статитстике, Ваш товарищ - рак. Ну, ничего, научится... "
    elif (ceil(userWinProc) >= 50 and ceil(userWinProc) < 54):
        Dossier = Dossier + "Ему есть куда рости... "
    else:
        Dossier = Dossier + "А товарищ Ваш, похоже статист. Два чая ему и кусочек торта. "

    return Dossier