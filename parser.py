import requests
import json
import pandas as pd
from sqlalchemy import create_engine
import time
import datetime
import operator


def get_domains():
    tmp_domains = open('domains.txt', 'r')
    domains = tmp_domains.read().split('\n')
    domains.remove('')
    return domains


def get_data(post):
    try:
        url = post['attachments'][0]['photo']['photo_604']
    except:
        url = '1'

    try:
        text = post['text']
    except:
        text = ''

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
        tdate = datetime.datetime.fromtimestamp(date)
    except:
        date = 0
        tdate = 0

    data = {
        'image_src': url,
        'description': text,
        'added_at': tdate,
        'likes_count': likes,
        'reposts_count': reposts,
        'factor': likes / (time.time() - date),
        'mode_id': 1
    }

    return data


def pandasql(data):
    frame = pd.DataFrame(data,
                         columns=['image_src', 'description', 'added_at', 'likes_count', 'reposts_count', 'factor',
                                  'mode_id'])
    engine = create_engine('postgresql://postgres:@localhost:5432/membattle')

    frame.to_sql("meme_storage", engine, if_exists='append', index=False)


def main():
    all_posts = []
    domains = get_domains()
    for elem in domains:
        r = requests.get('https://api.vk.com/method/wall.get',
                         params={'type': 'post', 'domain': elem, 'count': 100, 'offset': 1, 'v': 5.68,
                                 'access_token': "REDACTED"})

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
    sorted_posts = sorted(all_posts, key=operator.itemgetter('factor'), reverse=True)
    pandasql(sorted_posts)


if __name__ == "__main__":
    main()
