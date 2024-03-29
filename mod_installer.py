import os
import sys
import msvcrt
from dotenv import load_dotenv
import shutil
import requests
import json
from tqdm import tqdm
import argparse


VERSION = '1.6.6'


def _exit(status, message=''):
    print(message, file=sys.stderr)
    print('\nPress any key to exit...')
    msvcrt.getch()
    sys.exit(status)


print(f'\nSnowRunner/Expeditions mod installer v{VERSION} by equdevel\n')
load_dotenv()
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
GAME_ID = os.getenv('GAME_ID')
USER_PROFILE = os.getenv('USER_PROFILE')
MODS_DIR = os.getenv('MODS_DIR')
CACHE_DIR = f'{MODS_DIR}/../cache'

if None in (ACCESS_TOKEN, GAME_ID, USER_PROFILE, MODS_DIR):
    _exit(1, f'\nFILE NOT FOUND OR INCORRECT SETTINGS: please check .env file')

if GAME_ID not in ('306', '5734'):
    _exit(1, f'\nIncorrect GAME_ID: please check GAME_ID in .env (should be 306 for SnowRunner or 5734 for Expeditions)')

try:
    with open(USER_PROFILE, mode='r', encoding='utf-8') as f:
        user_profile = json.loads(f.read().rstrip('\0'))
except FileNotFoundError:
    _exit(1, f'\nUSER PROFILE NOT FOUND: please check path in .env: {USER_PROFILE}')
finally:
    if not os.path.isdir(MODS_DIR):
        _exit(1, f'\nMODS DIRECTORY NOT FOUND: please check path in .env: {MODS_DIR}')

parser = argparse.ArgumentParser(
    prog='mod_installer',
    description='Downloads mods from mod.io and installs them to SnowRunner/Expeditions'
)
parser.add_argument('-c', '--clear-cache', help='clear mods cache on disk', action='store_true')
parser.add_argument('-u', '--update', help='update mods if new versions exist', action='store_true')
parser.add_argument('-v', '--version', version=VERSION, action='version')
args = parser.parse_args()
update = args.update
if args.clear_cache:
    shutil.rmtree(CACHE_DIR)
    os.mkdir(CACHE_DIR)
    print('\nClearing cache --> OK')

headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'X-Modio-Platform': 'Windows'
}

print('\nChecking subscriptions on mod.io...')
result_offset = 0
r_data = []
while True:
    try:
        r = requests.get(f'https://api.mod.io/v1/me/subscribed?game_id={GAME_ID}&_offset={result_offset}', headers=headers)
    except requests.RequestException:
        _exit(1, '\nCONNECTION TO mod.io FAILED: please check your Internet connection')
    else:
        if r.status_code == 401:
            _exit(1, f'\nCONNECTION TO mod.io FAILED: please check your access token in .env')
        elif r.status_code != 200:
            _exit(1, f'\nCONNECTION TO mod.io FAILED: status_code={r.status_code}')
    r = r.json()
    if r['result_count'] > 0:
        r_data.extend(r['data'])
        result_offset += 100
    else:
        break

mods_subscribed = []

for data in r_data:
    mod_id = data['id']
    mod_name = data['name']
    mod_version_download = data['modfile']['version']
    mod_dir = f'{MODS_DIR}/{mod_id}'
    mods_subscribed.append(mod_id)
    download = False
    try:
        os.rename(f'{CACHE_DIR}/{mod_id}', f'{MODS_DIR}/{mod_id}')  # Trying to find mod in cache
        print(f'\nSubscribed mod with id={mod_id} "{mod_name}" found in cache, moving from cache to mods directory.')
    except FileNotFoundError:
        pass
    finally:
        try:
            os.mkdir(mod_dir)
        except FileExistsError:
            with open(f'{mod_dir}/modio.json', mode='r', encoding='utf-8') as f:
                mod_version_installed = json.load(f)['modfile']['version']
            if mod_version_installed != mod_version_download:
                if update:
                    shutil.rmtree(mod_dir)
                    os.mkdir(mod_dir)
                    download = True
                else:
                    print(f'\nMod with id={mod_id} "{mod_name}" {mod_version_installed} have new version {mod_version_download}, to update run with --update')
        else:
            download = True
        if download:
            if update:
                print(f'\nUpdating mod with id={mod_id} "{mod_name}" from {mod_version_installed} to {mod_version_download}')
            else:
                print(f'\nDownloading mod with id={mod_id} "{mod_name}" {mod_version_download}')
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

mods_installed = user_profile['UserProfile']['modDependencies']['SslValue']['dependencies']
for mod_id in mods_installed.keys():
    if int(mod_id) not in mods_subscribed:
        os.rename(f'{MODS_DIR}/{mod_id}', f'{CACHE_DIR}/{mod_id}')
        print(f'\nMoving to cache unsubscribed mod with id={mod_id}')
mods_installed.clear()
mods_installed.update({str(mod_id): [] for mod_id in mods_subscribed})

if 'modStateList' in user_profile['UserProfile'].keys():
    mods_enabled = user_profile['UserProfile']['modStateList']
    user_profile['UserProfile'].update({'modStateList': [mod for mod in mods_enabled if mod['modId'] in mods_subscribed]})

with open(USER_PROFILE, mode='w', encoding='utf-8') as f:
    f.write(json.dumps(user_profile, ensure_ascii=False, indent=4) + '\0')
print('\nUpdating user_profile.cfg --> OK')
print('\n\nDONATE: https://www.donationalerts.com/r/equdevel')
_exit(0)
