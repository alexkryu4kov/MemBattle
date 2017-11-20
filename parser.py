import requests
import json
import pandas as pd
from sqlalchemy import create_engine
import time


def get_domains():
    tmp_domains = open('domains.txt', 'r')
    domains = tmp_domains.read().split('\n')
    domains.remove('')
    return domains


def get_data(post):
    try:
        group_id = post['owner_id']
    except:
        group_id = '0'

    try:
        link = "https://vk.com/wall" + str(post['owner_id']) \
               + '_' + str(post['id'])
    except:
        link = '0'

    try:
        url = post['attachments'][0]['photo']['photo_604']
    except:
        url = '0'

    try:
        likes = post['likes']['count']
    except:
        likes = 0

    try:
        reposts = post['reposts']['count']
    except:
        reposts = 0

    try:
        date = post['date']
    except:
        date = 0

    data = {
        'group_id': group_id,
        'link': link,
        'url': url,
        'likes': likes,
        'reposts': reposts,
        'date': date,
        'value': likes / (time.time() - date)
    }

    return data


def pandasql(data):
    frame = pd.DataFrame(data, columns=['group_id', 'link', 'url', 'likes', 'reposts', 'date', 'value'])
    engine = create_engine('postgresql://memking:rofl@localhost:5432/membattle')

    frame.to_sql("membattle", engine, if_exists='replace')


def main():
    all_posts = []
    domains = get_domains()
    for elem in domains:
        r = requests.get('https://api.vk.com/method/wall.get',
                         params={'type': 'post', 'domain': elem, 'count': 100, 'offset': 1, 'v': 5.68,
                                 'access_token': "e6b967bce6b967bce6b967bc57e6e59d60ee6b9e6b967bcbf56031045e35bc30ab16dd9"})

        for post in range(100):
            data = r.json()['response']['items'][post]
            print(data)
            ads_flag = data['marked_as_ads']
            text_flag = data['text']

            try:
                type_flag = data['attachments'][0]['type']
            except:
                type_flag = '0'
            if ads_flag == 0 and type_flag == 'photo' and len(text_flag) < 30:
                all_posts.append(get_data(data))
    pandasql(all_posts)


if __name__ == "__main__":
    main()
