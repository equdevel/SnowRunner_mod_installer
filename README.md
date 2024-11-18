## Mod installer from mod.io to SnowRunner/Expeditions

The installer allows you to download mods from mod.io in semi-automatic mode. Once you complete all the steps according to the instructions, you will be able to subscribe to the desired mods, then the installer will do everything himself.

All SnowRunner/Expeditions versions are supported.


### Instructions:
1. Download [the latest version](https://github.com/equdevel/SnowRunner_mod_installer/releases/latest) and unzip it.
2. Register on mods site https://mod.io/g
3. Create a token in your profile https://mod.io/me/access, the token name can be anything. Copy the token and insert it to TOKEN.txt
4. Subscribe (or unsubscribe) to the desired mods on mod.io
5. Run "INSTALL MODS" from SnowRunner or Expeditions folder, wait until all the mods you subscribed to are downloaded.
6. Start the game, go to "LOAD GAME", exit back (needed to activate the "MOD BROWSER"), or wait a few seconds and "MOD BROWSER" will appear by itself.
7. Go to "MOD BROWSER" and enable the necessary mods. The vehicles will become available in the store, the custom maps will become available in "Custom scenarios", polygons are also available.

After new subscriptions or unsubscribes on the mod.io website, repeat everything from step 5.

After unsubscribing and launching the installer, the mod will be deactivated and removed from the list of modifications.
However, the folder with mod files remains on the disk (in the cache), and if you subscribe to the mod again, then after running the installer the mod will not be downloaded again, but will be moved from the cache to the mods folder and will be available in the game.

If you need to remove all mods from the cache, run "Clear cache and install mods" in "Advanced" folder.

If you need to force reinstall one or more mods, specify their IDs separated by spaces in MOD_ID.txt in "Advanced" folder, then run "Reinstall mods".

If you need to force reinstall all mods, run "Reinstall all mods" in "Advanced" folder. Warning! All mods will be deleted from the disk and downloaded again!

[![DONATE](https://github.com/equdevel/equdevel.github.io/blob/main/donate_banner_200px.png)](https://www.donationalerts.com/r/equdevel)
