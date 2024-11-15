import os
import sys
import msvcrt
from dotenv import load_dotenv
import shutil
import requests
import json
from tqdm import tqdm
import argparse


VERSION = '1.7.1'

GAME_ID = {'snowrunner': 306, 'expeditions': 5734}

print(f'\nSnowRunner/Expeditions mod installer v{VERSION} by EquDevel\n')
parser = argparse.ArgumentParser(
    prog='mod_installer',
    description='Downloads mods from mod.io and installs them to SnowRunner/Expeditions'
)
parser.add_argument('-v', '--version', help='show program\'s version and exit', action='store_true')
parser.add_argument('-u', '--update', help='update mods if new versions exist', action='store_true')
parser.add_argument('-c', '--clear-cache', help='clear mods cache on disk', action='store_true')
parser.add_argument('-r', '--reinstall', help='reinstall all mods', action='store_true')
parser.add_argument('-n', '--no-pause', help='no pause after execution', action='store_true')
args = parser.parse_args()

def _exit(status=0, message=''):
    if message != '':
        print(message)
    if not args.no_pause:
        print('\nPress any key to exit...')
        msvcrt.getch()
    sys.exit(status)

if args.version:
    _exit(0)
update = args.update

load_dotenv()
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN') or None
GAME = os.getenv('GAME') or None
USER_PROFILE = os.getenv('USER_PROFILE') or None
MODS_DIR = os.getenv('MODS_DIR') or None

exit_flag = False

if GAME is None:
    print(f'\nGAME IS NOT DEFINED')
    exit_flag = True
else:
    GAME = GAME.strip()
    if GAME.lower() not in GAME_ID.keys():
        print(f'\nINCORRECT GAME: should be SnowRunner or Expeditions')
        exit_flag = True
    else:
        GAME_ID = GAME_ID[GAME.lower()]

if MODS_DIR is None:
    print(f'\nMODS_DIR IS NOT DEFINED')
    exit_flag = True
else:
    MODS_DIR = MODS_DIR.strip()
    if not os.path.isdir(MODS_DIR):
        print(f'\nMODS DIRECTORY NOT FOUND: please check path {MODS_DIR}')
        exit_flag = True

if USER_PROFILE is None:
    print(f'\nUSER_PROFILE IS NOT DEFINED')
    exit_flag = True
else:
    USER_PROFILE = USER_PROFILE.strip()
    try:
        with open(USER_PROFILE, mode='r', encoding='utf-8') as f:
            user_profile = json.loads(f.read().rstrip('\0'))
    except OSError:
        print(f'\nUSER PROFILE NOT FOUND: please check path {USER_PROFILE}')
        exit_flag = True

if ACCESS_TOKEN is None:
    print(f'\nACCESS_TOKEN IS NOT DEFINED')
    exit_flag = True
else:
    ACCESS_TOKEN = ACCESS_TOKEN.strip()

if exit_flag:
    _exit(1)

print(f'GAME={GAME}')
print(f'MODS_DIR={MODS_DIR}')
print(f'USER_PROFILE={USER_PROFILE}')

CACHE_DIR = f'{MODS_DIR}/../cache'
if args.clear_cache or args.reinstall:
    try:
        shutil.rmtree(CACHE_DIR)
    except FileNotFoundError:
        print(f'\nCACHE DIRECTORY NOT FOUND: please check path {CACHE_DIR}')
        exit_flag = True
    else:
        os.mkdir(CACHE_DIR)
        print('\nClearing cache --> OK')
if args.reinstall:
    try:
        shutil.rmtree(MODS_DIR)
    except FileNotFoundError:
        print(f'\nMODS DIRECTORY NOT FOUND: please check path {MODS_DIR}')
        exit_flag = True
    else:
        os.mkdir(MODS_DIR)
        print('\nDeleting all mods in mods directory --> OK')

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
            _exit(1, f'\nCONNECTION TO mod.io FAILED: please check your access token')
        elif r.status_code != 200:
            _exit(1, f'\nCONNECTION TO mod.io FAILED: status_code={r.status_code}')
    r = r.json()
    if r['result_count'] > 0:
        r_data.extend(r['data'])
        result_offset += 100
    else:
        break

mods_subscribed = []
installed_mods_count = 0

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
                    print(f'\nUpdating mod with id={mod_id} "{mod_name}" from {mod_version_installed} to {mod_version_download}')
                else:
                    print(f'\nMod with id={mod_id} "{mod_name}" {mod_version_installed} has a new version {mod_version_download}, to update run with --update')
        else:
            download = True
            print(f'\nDownloading mod with id={mod_id} "{mod_name}" {mod_version_download}')
        if download:
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
            installed_mods_count += 1

user_profile['UserProfile'].update({'areModsPermitted': 1})
if 'modDependencies' not in user_profile['UserProfile'].keys():
    user_profile['UserProfile'].update({'modDependencies': {'SslType': 'ModDependencies', 'SslValue': {'dependencies': {}}}})

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
print(f'\nTotal mods subscribed = {len(mods_subscribed)}')
print(f'Total new mods installed = {installed_mods_count}')
print('\nFinish!')
# print('\n\nDONATE: https://www.donationalerts.com/r/equdevel')
# print('STMods: https://stmods.org/author/equdevel/')
# print('YouTube: https://www.youtube.com/@truck_mania')
# print('Telegram: https://t.me/truck_mania')
# print('GitHub: https://github.com/equdevel')
_exit(0)
