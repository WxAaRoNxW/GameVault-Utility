# Changelog
<details open>
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