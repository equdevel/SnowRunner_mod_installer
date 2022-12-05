import os
from dotenv import load_dotenv
import shutil
import requests
import json
from tqdm import tqdm


load_dotenv()
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
USER_PROFILE = os.getenv('USER_PROFILE')
MODS_DIR = os.getenv('MODS_DIR')

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Accept': 'application/json',
    'X-Modio-Platform': 'Windows'
}

data = {
    'game_id': 306
}

r = requests.get('https://api.mod.io/v1/me/subscribed', params={}, headers=headers, json=data)

with open(USER_PROFILE, mode='r', encoding='utf-8') as f:
    user_profile = json.loads(f.read().rstrip('\0'))

user_profile['UserProfile'].update({'areModsPermitted': 1})
user_profile['UserProfile'].update({'modFilter': {'user0': {'SslType': 'ModBrowserConfigData', 'SslValue': {'isEnabledMode': False, 'tags': [], 'isConsoleForbiddenMode': False, 'isSubscriptionsMode': False, 'isConsoleApprovedMode': False, 'sortIsAsc': False, 'sortField': 'popular'}}}})
user_profile['UserProfile'].update({'modDependencies': {'SslType': 'ModDependencies', 'SslValue': {'dependencies': {}}}})

for data in r.json()['data']:
    mod_id = data['id']
    mod_name = data['name']
    mod_dir = f'{MODS_DIR}/{mod_id}'
    try:
        os.mkdir(mod_dir)
    except FileExistsError:
        pass
    else:
        with open(f'{MODS_DIR}/{mod_id}/modio.json', mode='w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        mod_url = data['modfile']['download']['binary_url']
        mod_filename = data['modfile']['filename']
        mod_fullpath = f'{MODS_DIR}/{mod_id}/{mod_filename}'
        print(f'Downloading "{mod_name}" ({mod_filename})')
        response = requests.get(mod_url, stream=True)
        with open(mod_fullpath, mode='wb') as f:
            for chunk in tqdm(response.iter_content(chunk_size=1024**2), unit=' Mb'):
                f.write(chunk)
        print(f'Unpacking {mod_filename}...', end='')
        shutil.unpack_archive(mod_fullpath, mod_dir, 'zip')
        os.remove(mod_fullpath)
        print('OK')
    finally:
        user_profile['UserProfile']['modDependencies']['SslValue']['dependencies'].update({str(mod_id): []})

with open(USER_PROFILE, mode='w', encoding='utf-8') as f:
    json.dump(user_profile, f, ensure_ascii=False, indent=4)
