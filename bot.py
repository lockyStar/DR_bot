# -*- coding: utf-8 -*-

import requests
import datetime
from time import sleep
import json

if datetime.datetime.today().month > 9 or datetime.datetime.today().month == 9 and datetime.datetime.today().day > 27:
    B_DAY = datetime.date(year=datetime.datetime.today().year + 1, month=9, day=27)
else:
    B_DAY = datetime.date(year=datetime.datetime.today().year, month=9, day=27)

url = "https://api.telegram.org/bot724587745:AAGuLtig6J5Kb6-3mTeDiFFvu26xNEdR9V0/"


def get_updates_json(request):
    response = requests.get(request + 'getUpdates')
    return response.json()


def get_chat_id(update):
    _chat_id = update['message']['chat']['id']
    if _chat_id not in chats:
        update_chats(_chat_id)
    return _chat_id


def last_update(req):
    results = req['result']

    total_updates = len(results) - 1
    try:
        upd_id = results[total_updates]['update_id']
        print(upd_id)
    except IndexError as e:
        upd_id = 0
    return upd_id


def get_updates(req):
    data = get_updates_json(req)
    results = data['result']
    update_log(results)
    for result in results:
        chats.append(get_chat_id(result))


def send_mess(chat, text):
    params = {'chat_id': chat, 'text': text}
    response = requests.post(url + 'sendMessage', data=params)
    return response


def update_log(updates):
    f = open("messages.log", "a+")
    for update in updates:
        f.write("\n" + json.dumps(update))


def get_chats():
    return set([int(line.rstrip('\n')) for line in open('chats.txt')])


def update_chats(_chat_id):
    f = open("chats.txt", "a+")
    f.write("\n" + str(_chat_id))


def get_chats_from_update(req):
    data = get_updates_json(req)
    results = data['result']
    update_log(results)
    new_chats = set()
    for result in results:
        chats.add(get_chat_id(result))
        new_chats.add(get_chat_id(result))
    return new_chats

# print(requests.get(url + 'getMe'))
chats = get_chats()
# get_updates(url)
# for chat in chats:
#     send_mess(chat, 'ДО САМОГО КРУТОГО ДНЯ РОЖДЕНИЯ ОСТАЛОСЬ ВСЕГО {} ДНЕЙ!!!'.format(str((B_DAY - datetime.date.today()).days)))


def main():
    last_push_date = datetime.date.today() - datetime.timedelta(days=1)
    update_id = last_update(get_updates_json(url))
    while True:
        if last_push_date != datetime.date.today():
            for chat in chats:
                send_mess(chat, 'ДО САМОГО КРУТОГО ДНЯ РОЖДЕНИЯ ОСТАЛОСЬ ВСЕГО {} ДНЕЙ!!!'.format(str((B_DAY - datetime.date.today()).days)))
            last_push_date = datetime.date.today()
            continue

        if update_id != last_update(get_updates_json(url)) != 0:
            update_id = last_update(get_updates_json(url))
            updated_chats = get_chats_from_update(url)
            for chat in updated_chats:
                send_mess(chat, 'ДО САМОГО ВАЖНОГО ДНЯ РОЖДЕНИЯ ОСТАЛОСЬ ВСЕГО {} ДНЕЙ!!!'.format(str((B_DAY - datetime.date.today()).days)))

        sleep(1)


if __name__ == '__main__':
    main()
