import requests as rq
import time


token = '9ca89b9d328a509fcbba40927549112d4fe72ea75807237f0a8139409b6ee211d76e288e6ba271ea11eca'
v = 5.92


def board_Topics(v, token, group_id):
    return rq.get('https://api.vk.com/method/board.getTopics?',
                  params={
                      'access_token': token,
                      'v': v,
                      'group_id': group_id,
                      'count': 100,
                      'extended': 1,
                      'preview_length': 0
                  }).json()['response']['items']


def board_Comments(v, token, group_id, topic_id, offset):
    while True:
        response = rq.get('https://api.vk.com/method/board.getComments?',
                      params={
                          'access_token': token,
                          'v': v,
                          'group_id': group_id,
                          'topic_id': topic_id,
                          'count': 100,
                          'extended': 1,
                          'offset': offset
                      })
        data = response.json()
        if 'response' in data:
            return data['response']['items']
        else:
            time.sleep(0.5)



group_id = 33374477
id_persons = 7595029


board_comm = []
for i in board_Topics(v, token, group_id):
    for p in range(0, i['comments'], 100):
        for comment in board_Comments(v, token, group_id, i['id'], p):
            if comment['from_id'] == id_persons:
                board_comm.append(comment)
board_comm # Выводит массив, со словарями (каждый словарь - коммент нужного пользователя)