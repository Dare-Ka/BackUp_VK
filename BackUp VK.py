import json
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from tqdm import tqdm
class VK:

   def __init__(self, access_token, user_id, version='5.131'):
       self.token = access_token
       self.id = user_id
       self.version = version
       self.params = {'access_token': self.token,
                      'v': self.version}

   def users_info(self):
       url = 'https://api.vk.com/method/users.get'
       params = {'user_ids': self.id}
       response = requests.get(url, params={**self.params, **params})
       return response.json()

   def get_user_photos(self):
       url = 'https://api.vk.com/method/'
       photos_get_url = url + 'photos.get'
       params = {'owner_id': user_id,
                 'album_id': 'profile',
                 'rev': 0,
                 'extended': 1,
                 'photo_sizes': 1,
                 'count': 50}

       response = requests.get(photos_get_url, params={**self.params, **params})
       data = response.json()

       photos_links = []
       info_list = []
       names = []
       size_types = []
       for item in data['response']['items']:
           if item['likes']['count'] not in names:
               names.append(item['likes']['count'])
           else:
               names.append(f'{item["likes"]["count"]}_{datetime.utcfromtimestamp(item["date"]).strftime("%Y-%m-%d")}')
           photos_links.append(item['sizes'][-1]['url'])
           size_types.append(item['sizes'][-1]['type'])
       global links
       links = list(zip(names, size_types, photos_links))
       for name, size_type, link in links:
           name_dict = {'file_name': f'{name}.jpg', 'size': size_type}
           info_list.append(name_dict)
       info_file = json.dumps(info_list)
       if not os.path.exists('images_json'):
           os.mkdir('images_json')
       with open('images_json/%s' % 'JSON_DATA.json', 'w') as file:
           file.write(info_file)
       return f'Скачано {len(names)} фотографий из ВК'

class Yandex:

    def __init__(self, token):
        self.token = token_Yandex

    def upload_files(self, path, replace=False):
       URL = 'https://cloud-api.yandex.net/v1/disk/resources'
       self.headers = {'Content-Type': 'application/json',
                       'Accept': 'application/json',
                       'Authorization': f'OAuth {self.token}'}
       requests.put(f'{URL}?path={path}', headers=self.headers)
       count = 0
       with tqdm(range(len(links))) as progress:
           for name, size_type, link in links:
               self.headers = {'Content-Type': 'application/json',
                           'Accept': 'application/json',
                           'Authorization': f'OAuth {self.token}'}
               self.params = {'path': f'{path}/{name}',
                          'overwrite': 'true'}
               response = requests.get(f'{URL}/upload', headers=self.headers, params=self.params)
               href = response.json().get('href')
               requests.put(href, data=requests.get(link).content)
               count +=1
               progress.update()
       return f'Загружено {count} фотографий на Яндекс Диск'

load_dotenv()
access_token = os.getenv('access_token')
token_Yandex = os.getenv('token_Yandex')
user_id = str(input('Введите ID VK: '))
vk = VK(access_token, user_id)
yandex = Yandex(token_Yandex)
print(vk.get_user_photos())
print(yandex.upload_files(str(input('Введите название папки: '))))



