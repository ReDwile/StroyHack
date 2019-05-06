import requests as rq
import time


def posts(v, token, id_groups):  # Возвращает массив группы, в котором 100 постов
    while True:
        response = rq.get('https://api.vk.com/method/wall.get?',
                          params={
                              'access_token': token,
                              'v': v,
                              'domain': id_groups,
                              'extended': 1,
                              'count': 100
                          })
        data = response.json()
        if 'response' in data:
            return data['response']['items']
        else:
            time.sleep(0.5)


def true_like(token, v, post, id_persons):
    try:
        return rq.get('https://api.vk.com/method/likes.isLiked?',
                      params={
                          'access_token': token,
                          'v': v,
                          'user_id': id_persons,
                          'type': 'post',
                          'owner_id': post['owner_id'],
                          'item_id': post['id']
                      }).json()['response']['liked']
    except:
        return 0


def true_comments(token, v, owner_id, post_id):
    try:
        a = rq.get('https://api.vk.com/method/wall.getComments?',
                   params={
                       'access_token': token,
                       'v': v,
                       'owner_id': owner_id,
                       'post_id': post_id,
                       'need_likes': 0,
                       'count': 100,
                       'extended': 1
                   }).json()['response']['items']
        return a
    except:
        return []


def id_posts(token, v, id_persons):
    dictionary = rq.get(f'http://35.239.79.112:9999/vk_profile?max=100&id={id_persons}').json()['groups']
    mas = {'likes': [], 'comments': []}
    for i in range(len(dictionary)):
        if dictionary[i]['score'] > 0:
            for post in posts(v, token, dictionary[i]['screen_name']):  # Посты (100 штук)
                if true_like(token, v, post, id_persons) == 1:
                    mas['likes'].append(post)
                for com in true_comments(token, v, post['owner_id'], post['id']):
                    if com['from_id'] == id_persons:
                        mas['comments'].append(post)
    return mas


token = '9ca89b9d328a509fcbba40927549112d4fe72ea75807237f0a8139409b6ee211d76e288e6ba271ea11eca'
v = 5.92
id_persons = 152403417

print(id_posts(token, v, id_persons))  # Выводит {'likes': [Словари с постами, которые человек лайкнул], 'comments': [Словари с постами, которые человек комментировал]}
