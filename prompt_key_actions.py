import random
import uuid
from InquirerPy.prompts.input import InputPrompt

def get_keybindings(prompt: InputPrompt, key_action: str):
    match key_action:
        case "uuid":
            @prompt.register_kb("c-r")
            def _(event):
                # access the current prompt buffer
                buffer = event.app.current_buffer

                # change the input text
                buffer.text = str(uuid.uuid4())
                buffer.cursor_position = len(buffer.text)
        case "steam_id":
            @prompt.register_kb("c-r")
            def _(event):
                # access the current prompt buffer
                buffer = event.app.current_buffer

                # change the input text
                buffer.text = str(generate_steamid64())
                buffer.cursor_position = len(buffer.text)


def get_l_instruction_suffix(key_action: str):
    instruction_text = ""
    match key_action:
        case "uuid":
            instruction_text = "Ctrl + R to generate a random UUID"
        case "steam_id":
            instruction_text = "Ctrl + R to generate a random Steam ID"
    
    return instruction_text

def generate_steamid64(
    universe=1,
    account_type=1,
    instance=1,
    account_number=None,
    y=None
):
    if account_number is None:
        account_number = random.randint(1, 2**31 - 1)

    if y is None:
        y = random.randint(0, 1)

    steamid64 = (
        (universe & 0xFF) << 56 |
        (account_type & 0xF) << 52 |
        (instance & 0xFFFFF) << 32 |
        (account_number & 0x7FFFFFFF) << 1 |
        (y & 0x1)
    )

    return steamid64
