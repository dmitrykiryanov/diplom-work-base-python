import requests

import json

from pprint import pprint


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


def to_download_photo(download_url, file_name):
    p = requests.get(download_url)
    with open(file_name, "wb") as saved_photo:
        saved_photo.write(p.content)


with open('token.txt', 'r') as file_object:
    token = file_object.read().strip()

if __name__ == '__main__':
    URL = 'https://api.vk.com/method/photos.get'
    params = {
        'owner_id': 552934290,
        'access_token': token,
        'album_id': 'profile',
        'extended': 1,
        'v': '5.131'
    }
    res = requests.get(URL, params=params)
    data_photo = res.json()['response']
    json_file = []
    likes_count_list = []
    for data in data_photo['items']:
        json_dict = {}
        likes_count = data['likes']['count']
        if likes_count in likes_count_list:
            name_photo =f'{likes_count}_{data["date"]}.jpg'
        else:
            likes_count_list.append(likes_count)
            name_photo = f'{likes_count}.jpg'
        to_download_photo(data['sizes'][-1]['url'], name_photo)
        ya = YandexDisk(token="")
        ya.upload_file_to_disk(f"hw_Python/{name_photo}", name_photo)
        json_dict["file_name"] = name_photo
        json_dict["type"] = data['sizes'][-1]['type']
        json_file.append(json_dict)

    with open('file_results.json', 'w') as f:
        json.dump(json_file, f, ensure_ascii=False, indent=2)