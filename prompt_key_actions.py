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

def get_l_instruction_suffix(key_action: str):
    instruction_text = ""
    match key_action:
        case "uuid":
            instruction_text = "Ctrl + R to regenerate new UUID"
    
    return instruction_text