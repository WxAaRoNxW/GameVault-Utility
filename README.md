## Disclaimer
GameVault clients not launched as administrator will keep track of playtime based on .exe name alone, if all games contain this tool it will increment all their playtime and last played ("don't ask again" option fixes this).

To completely avoid this, either tell each user to launch GameVault as admin or rename the `GVU.exe` to something else for each game, I append mine with `_Game Name`

## Preview
![Preview](https://i.imgur.com/uA90zEA.png)

## Features

* **Save Preservation**
  Prevents save files from being overwritten, by moving it outside of game folders and using symlink. This is meant for games that store their saves in their game folders, since GameVault overwrites the entire game directory when updating a game.

* **Change Modification Setup**
  Provides initial setup assistance for specific modified versions of games, helping players who are unfamiliar with the required configuration.

  Supported setup types can include:

  - **Goldberg** - Interactive setup for configuring the account name and preferred SteamID.
  - **OnlineFix** - Assists with the initial setup, including semi-automatically adding Spacewar to the Steam library.
  - **Other modifications**
  - **No modification**

* **Game Version Switching**
  Switch between different versions or configurations of a game. ex. Switching from a Steam version to a modified version of it.

* **Share Game Versions**
  Can be used independently of GameVault to prepare and send this tool (along with modifications) to friends who obtained the game elsewhere, allowing everyone to use the same game version.
  - Usually meant for players that own the steam version but would like to play with others using a modified version, like OnlineFix.

> **Note:** Different modified versions must be added manually. This project does not provide or distribute modified game files or modifications themselves.

## How to Use

This tool is intended for **GameVault server owners**. It must be bundled individually with each game that you want to provide with this Utility tool.

### Preparing a Game

1. **Extract the release file's contents** into the game's directory.
3. **Configure the tool** by modifying `gvu_config_copy_DO_NOT_DELETE.ini` and set the configuration values appropriate for the game.
3. **Compress the game directory content** and upload it to your GameVault server.

### Change Version Setup

If you want to provide the **Change Version Setup** feature for a game, additional files must be included before compressing the game.

Place the necessary files inside:

```text
_GVU/
└── GVU config/
    ├── original files/
    └── cracked files/
```

Place the appropriate files in either `original files` or `cracked files` depending on which version they belong to. `original file` is optional and can be disabled in config, disabling this will also make `cracked files` optional.

These files are used by the utility to perform the initial setup for the corresponding modification. **You must provide the necessary files yourself; this project does not provide or distribute modified game files.**

> **Note:** When a friend uses this outside of GameVault the tool will backup their original files that the cracked files may overwrite.

## Building

To build, run:

```bash
python build.py
```

If you'd like to modify:
  - The build internals' output directory.
  - Default account name for certain types of games. (players are still prompted if they'd like to change the default name)

Edit the file, `config/config.py` and modify `APP_NAME` and `gv_account_name` values respectively.