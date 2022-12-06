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

r = requests.get('https://api.mod.io/v1/me/subscribed', headers=headers, json=data)

with open(USER_PROFILE, mode='r', encoding='utf-8') as f:
    user_profile = json.loads(f.read().rstrip('\0'))

mods_subscribed = []

for data in r.json()['data']:
    mod_id = data['id']
    mod_name = data['name']
    mod_dir = f'{MODS_DIR}/{mod_id}'
    mods_subscribed.append(mod_id)
    try:
        os.mkdir(mod_dir)
    except FileExistsError:
        pass
    else:
        print(f'\nDownloading mod "{mod_name}" (id={mod_id})')
        for res in ('320x180', '640x360'):
            url = data['logo'][f'thumb_{res}']
            logo_path = f'{mod_dir}/logo_{res}.png'
            data['logo'][f'thumb_{res}'] = f'file:///{logo_path}'
            d = requests.get(url)
            with open(logo_path, mode='wb') as f:
                f.write(d.content)
        print('--> Downloading thumbs --> OK')
        with open(f'{mod_dir}/modio.json', mode='w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print('--> Creating modio.json --> OK')
        mod_url = data['modfile']['download']['binary_url']
        mod_filename = data['modfile']['filename']
        mod_fullpath = f'{mod_dir}/{mod_filename}'
        print(f'--> Downloading {mod_filename}')
        response = requests.get(mod_url, stream=True)
        with open(mod_fullpath, mode='wb') as f:
            for chunk in tqdm(response.iter_content(chunk_size=1024**2), unit=' Mb'):
                f.write(chunk)
        print('--> OK')
        print(f'--> Unpacking {mod_filename} --> ', end='')
        shutil.unpack_archive(mod_fullpath, mod_dir, 'zip')
        os.remove(mod_fullpath)
        print('OK')

user_profile['UserProfile']['modDependencies']['SslValue']['dependencies'] = {str(mod_id): [] for mod_id in mods_subscribed}
if 'modStateList' in user_profile['UserProfile'].keys():
    user_profile['UserProfile']['modStateList'] = [mod for mod in user_profile['UserProfile']['modStateList'] if mod['modId'] in mods_subscribed]

with open(USER_PROFILE, mode='w', encoding='utf-8') as f:
    f.write(json.dumps(user_profile, ensure_ascii=False, indent=4) + '\0')
print('\nUpdating user_profile.cfg --> OK')
