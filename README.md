## Mods installer from mod.io website to SnowRunner

### Instructions:
1. Download the latest version [SnowRunner_mod_installer.zip](https://github.com/equdevel/SnowRunner_mod_installer/releases/latest)
2. Register on mod.io website
3. Create a token in your profile https://mod.io/me/access (you must first confirm the API Access Terms). The token name can be anything.
4. Rename .env_example file to .env, then add the token to it, edit path to the mods folder and user_profile.cfg file:
   - mod folder: C:/Users/USERNAME/Documents/My Games/SnowRunner/base/Mods/.modio/mods
   - Steam profile: C:/Users/Public/Documents/Steam/CODEX/1465360/remote/user_profile.cfg
   - EGS profile: C:/Users/USER_NAME/Documents/My Games/SnowRunner/base/storage/0/user_profile.dat
5. Block the game's access to the Internet through Windows firewall: press Win + R and run wf.msc, create a rule for outgoing connections, select "For program", specify path to the game (you can specify a shortcut on the desktop), select "Block connection ".
6. Replace file C:/Users/Public/Documents/Steam/CODEX/1465360/remote/user_profile.cfg (or C:/Users/USER_NAME/Documents/My Games/SnowRunner/base/storage/0/user_profile.dat) to a file from the archive.
7. Subscribe (or unsubscribe) to the desired mods on mod.io
8. Run mod_installer.exe, wait until all the mods you subscribed to are downloaded.
9. Start the game, go to “Load”, exit back (needed to activate the “View modifications” item)
10. Go to “View Modifications” and enable the necessary mods. The cars will become available in the store. Polygons are also available. Pictures of mods in the menu are also displayed.

After new subscriptions or unsubscribes on the mod.io website, repeat everything from step 7. After unsubscribing and launching the installer, the mod is deactivated and removed from the list of modifications. However, the folder with mod files remains on the disk (in the cache C:/Users/USERNAME/Documents/My Games/SnowRunner/base/Mods/.modio/cache), and if you subscribe to the mod again, then after running the installer the mod will not exist download again, and will move from the cache to the mods folder, but you will need to manually turn it on again in the game in “View modifications.”

If you need to remove all mods from the cache, run the installer with --clear-cache switch

If you need to download new versions of mods, run the installer with --update key (without the key, a message will simply appear about the release of new versions of mods)
