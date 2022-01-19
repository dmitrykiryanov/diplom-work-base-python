import requests

import json

from pprint import pprint

# создаем класс для работы с Яндекс.Диском
class YandexDisk:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "false"}
        response = requests.get(upload_url, headers=headers, params=params)
        pprint(response.json())
        return response.json()

    def upload_file_to_disk(self, disk_file_path, filename):
        href = self._get_upload_link(disk_file_path=disk_file_path).get("href", "")
        response = requests.put(href, data=open(filename, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print("Success")
# добавлем функцию создания новой папки на Яндекс.Диске для загрузки в нее фотографий с профиля
    def make_folder (self, name_folder):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        params = {"path": name_folder}
        response = requests.put(upload_url, headers=headers, params=params)
        response.raise_for_status()
        if response.status_code == 201:
            print("Success")


# добавляем функцию для загрузки фото с профиля вк
def to_download_photo(download_url, file_name):
    p = requests.get(download_url)
    with open(file_name, "wb") as saved_photo:
        saved_photo.write(p.content)


with open('token_vk.txt', 'r') as file_object:
    token_vk = file_object.read().strip()
with open('token_ya.txt', 'r') as file_object:
    token_ya = file_object.read().strip()

if __name__ == '__main__':
    name_folder = input('Введите название новой папки для загрузки фотографий на Яндекс.Диск:')
    URL = 'https://api.vk.com/method/photos.get'
    params = {
        'owner_id': 552934290,
        'access_token': token_vk,
        'album_id': 'profile',
        'extended': 1,
        'v': '5.131'
    }
    res = requests.get(URL, params=params)
    data_photo = res.json()['response']
    json_file = []
    likes_count_list = []
    ya = YandexDisk(token=token_ya)
    ya.make_folder(name_folder)
    for data in data_photo['items']:
        json_dict = {}
        likes_count = data['likes']['count']
        if likes_count in likes_count_list:
            name_photo = f'{likes_count}_{data["date"]}.jpg'
        else:
            likes_count_list.append(likes_count)
            name_photo = f'{likes_count}.jpg'
        to_download_photo(data['sizes'][-1]['url'], name_photo)
        ya = YandexDisk(token=token_ya)
        ya.upload_file_to_disk(f"{name_folder}/{name_photo}", name_photo)
        json_dict["file_name"] = name_photo
        json_dict["type"] = data['sizes'][-1]['type']
        json_file.append(json_dict)
# записываем json-файл с информацией по загруженным фото
    with open('file_results.json', 'w') as f:
        json.dump(json_file, f, ensure_ascii=False, indent=2)