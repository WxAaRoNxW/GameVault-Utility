from pathlib import Path
import sys
import subprocess
import time
from setup_game import CRACK_TYPES, is_complete, one_time_setup
from config_loader import BASE_PATH, GAMEVAULT_EXEC_CONFIG, Config, get_config_value, set_config_values
from util import clear_screen, get_exe_path
from version_changer import change_version
from gamevault_exec_handler import set_executable
from logger import console

# ----------------------------
# Functions
# ----------------------------

# 1. Start game
def start_game():
    # reset Don't Ask Again
    dont_ask_again = get_config_value(Config.Default.str(), Config.Default.DontAskAgain, "False").lower() == "true"
    if (dont_ask_again):
        set_config_values(Config.Default.str(), Config.Default.DontAskAgain, "False")
        set_executable(get_exe_path()) # revert to this python.exe
    # run exe
    exe_path = get_config_value(Config.Default.str(), Config.Default.Executable)
    exe_path = Path(exe_path)

    if exe_path.exists() and exe_path.is_file():
        console.print(f"Starting game: {exe_path}")
        subprocess.run(exe_path)
        sys.exit("Exiting...")
    else:
        console.print("[red]Executable path not found in external config.")
        time.sleep(2)

# 2. Start game and don't ask again
def start_game_no_prompt():
    # Update executable of gamevault-exec
    set_executable(str(BASE_PATH / get_config_value(Config.Default.str(), Config.Default.Executable)))
    
    console.print(f"Updated gamevault-exec file to skip prompt next time.")
    time.sleep(2)
    start_game()

# 4. Change version (delete files in __folder1, merge __folder2 into base)
def prompt_change_version():
    while True:

        console.print("Choose version:")
        console.print("1. Original")
        console.print("2. Pirated")
        console.print("3. Back")
        choice = input("Enter choice (1 or 2): ").strip()
        match choice:
            case "1":
                choice = "Original"
                break
            case "2":
                choice = "Pirated"
                break
            case "3":
                clear_screen()
                return
            case _:
                console.print("Invalid choice.")
        clear_screen()

    clear_screen()
    change_version(version=choice)

# ----------------------------
# Main prompt loop
# ----------------------------
def main():
    while True:
        # Load suffix info from external config
        setup_type = get_config_value(Config.Crack.str(), Config.Crack.Type, "CONTACT GAMEVAULT ADMIN")
        setup_done = is_complete()

        # Build option 3 string
        match CRACK_TYPES[setup_type]:
            case CRACK_TYPES.OnlineFix:
                option3_str = f"3. One-time global setup for '{setup_type}'"
            case CRACK_TYPES.Goldberg:
                option3_str = f"3. One-time global setup for '{setup_type}'"
            case CRACK_TYPES.RUNE:
                option3_str = f"3. Per-Game Setup for '{setup_type}'"
            case _:
                option3_str = "3. Option error, Contact GameVault Admin!"
        if setup_done:
            option3_str += " (complete)"
        else:
            option3_str += " (DO THIS FIRST)"
            

        option4_str = "4. Change version"
        current_version = get_config_value(Config.Default.str(), Config.Default.GameVersion, "")
        if current_version:
            option4_str += f". Current: {current_version}"

        console.print("\nSelect an option:")
        console.print("1. Start game")
        console.print("2. Start game and don't ask again")
        console.print(option3_str)
        console.print(option4_str)
        console.print("5. Exit")
        
        choice = input("Enter choice (1-5): ").strip()
        clear_screen()
        if choice == "1":
            start_game()
        elif choice == "2":
            start_game_no_prompt()
        elif choice == "3":
            one_time_setup()
        elif choice == "4":
            prompt_change_version()
        elif choice == "5":
            sys.exit("Exiting...")
        else:
            console.print("Invalid choice, try again.")
            clear_screen()

# ----------------------------
# Entry point
# ----------------------------
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")