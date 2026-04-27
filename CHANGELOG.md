# Changelog
<details open>
<summary><b>
v5.1.0
</b></summary>

- Added
    - Add LaunchParameter config option.

</details>

<details>
<summary><b>
v5.0.0
</b></summary>

- Added
    - Send to Friend - Easily compresses the game for users to send their copy of GVU to a legitimate user.

- Changed
    - Copy "orig files" to a temp dir before sending to orig files to check if it is a valid clean files.

- Fixed
    - Missing text for GSE instruction.
    - Backup orig files always seeing game folder as clean, potentially making original files contain cracked files.

</details>

<details>
<summary><b>
v4.2.0
</b></summary>

- Added
    - No GameVault Mode
        - Backup of GVU original when using.
        - Double check game files if it was modified before using as original files backup.
- Fixed
    - Incorrect locale for GSE instruction.

</details>

<details>
<summary><b>
v4.1.0
</b></summary>

- Added
    - Open game through steam when using original version to get steam's api to work. Opening through .exe most of the time won't show on steam you're playing it.
- Fixed
    - Launching Games in Original version will now show up on your steam (Given you own it).

</details>

<details>
<summary><b>
v4.0.2
</b></summary>

- Fixed
    - No GameVault mode causes crash. Code execution order changed to prevent any exceptions.
    - Set NoOriginal config entry to False when NoGameVault mode detected.
    - Set version changer config during NoGameVault mode to "Original"
    
</details>

<details>
<summary><b>
v4.0.1
</b></summary>

- Fixed
    - Start Game not working.
    - Symbolic Linking no longer occurs everytime you enter main menu.
    - gamevault-exec path not setting correct path when selecting "Start Game".
    
</details>

<details>
<summary><b>
v4.0.0
</b></summary>

- Added
    - Standalone mode to allow using GVU outside of GameVault Games to pass it around to legitimate users.
        - Backs up original files for restoration when switching back to legitimate for cases where the game does not have an original stored.
    - Localization for better handling of messages, through json files.
    - Config template in repository.

- Changed
    - Run gamevault games through url protocol gamevault://start
    - Close program instead of hiding when starting game, since GameVault detects based on if the app name is contained in GameVault games.
        - Also means GVU.exe needs to be prefixed per game or else it will cause all GVU handled games to update its `Last Played` / `Play Time`
    - Move global config to roaming instead.
        - For compatibility with No GameVault Mode.
        - To avoid newly formatted PC's from thinking that GameVault has already been setup on new machines.
    - Rename crack files dir name to cracked files for consistency.
    - UAC admin request changed to use pyinstaller built-in argument.
    - Change symlink behavior partially for optimization and decoupling.
    - Better instructions in main menu.

</details>

<details>
<summary><b>
v3.3.0
</b></summary>

- Added
    - Add keyword formatting for symlinking paths.
        - {game_name} - Game Folder name. ex. "(1)Random Game"
        - {game_persistent_data_path} - Folder path where persistent data of games are transferred to by GVU.

- Changed
    - Change global config location to GameVault root.
    - Separate symlink setup from game setup. (added new config variable)
    - Refactor config paths.

- Fixed
    - Error checking for symlink config.

</details>

<details>
<summary><b>
v3.2.2
</b></summary>

- Fixed
    - Goldberg_Old not completing its setup when proceeding with setup. (last patch was saying [n]o to modifying existing config)

</details>

<details>
<summary><b>
v3.2.1
</b></summary>

- Changed
    - Console now hides until game closes, which it will close soon after.
    - Add more info to start options.

- Fixed
    - GameVault now tracks game time even if users do not run with "Start Game and don't ask again"
    - Goldberg_Old option error in setup.
    - Goldberg_Old not completing its setup.
</details>

<details>
<summary><b>
v3.2.0
</b></summary>

- Added
    - Add debug mode for codes that are not necessary in development environment.
    - Add new Goldberg version as Goldberg in config.
    - Add VSCode task to avoid manually typing build.
    - Add Steam ID Generator in Steam ID prompts.

- Changed
    - Add ROAMING var to avoid code duplication.
    - Rename Goldberg to Goldberg Old.

- Fixed
    - Error handling of symlinking and its config.
    - Allow creating parents when link path doesn't exist.
    - (Y/N) instructions in prompts are not shown.

</details>

<details>
<summary><b>
v3.1.0
</b></summary>

- Added
    - Dynamic config based Symbolic Linking to avoid data wipes during updates for games with player data in game folder.

    - Add more error handling.
- Changed
    - Program now requires Administration for Symbolic Linking.

</details>

<details>
<summary><b>
v3.0.0
</b></summary>

- Added
    - Dynamic config based prompts to avoid constantly giving new updates.

- Changed
    - Moved definitions.

- Fixed
    - Goldberg Steam ID prompt's Default now shows existing ID, unless not, which the default would be the lowest Steam ID possible.

</details>

<details>
<summary><b>
v2.1.0
</b></summary>

- Added
    - Add header in main menu with version.
    - Config option for when there's no setup to do.
    - Config option for when there's no original.

- Fix
    - Confirming that you've done the setup in the past for OnlineFix setup, now marks the setup as complete.

</details>

<details>
<summary><b>
v2.0.0
</b></summary>

- Added
    - Prompts are now Arrow Key controled, using InquirerPy.

- Changed
    - Paths of config files are now inside the library of the python program.
    - Remove _ in original and crack directory names since they're in a specific folder now.
    - Rename program to GVU.exe.
    - Other options are restricted until setup is complete.

- Fix
    - Declining Goldberg edit now marks setup as complete.

</details>

<details>
<summary><b>
v1.0.0
</b></summary>

- Initial release

</details>