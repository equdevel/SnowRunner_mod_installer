import os
from dotenv import load_dotenv
import shutil
from pprint import pprint, pformat
import requests
import json
from tqdm import tqdm


load_dotenv()
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Accept': 'application/json',
    'X-Modio-Platform': 'Windows'
}

data = {
    'game_id': 306
}

r = requests.get('https://api.mod.io/v1/me/subscribed', params={}, headers=headers, json=data)

# pprint(r.json())

for data in r.json()['data']:
    mod_id = data['id']
    mod_name = data['name']
    try:
        os.mkdir(str(mod_id))
    except FileExistsError:
        pass
    else:
        with open(f'{mod_id}/modio.json', mode='w', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=4))
        mod_url = data['modfile']['download']['binary_url']
        mod_filename = data['modfile']['filename']
        mod_path = f'{mod_id}/{mod_filename}'
        print(f'Downloading "{mod_name}" ({mod_filename})')
        response = requests.get(mod_url, stream=True)
        with open(mod_path, mode='wb') as handle:
            for chunk in tqdm(response.iter_content(chunk_size=1024**2), unit=' Mb'):
                handle.write(chunk)
        print(f'Unpacking {mod_filename}...', end='')
        shutil.unpack_archive(mod_path, str(mod_id), 'zip')
        os.remove(mod_path)
        print('OK')
    finally:
        pass
