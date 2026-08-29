import json
from config.config import LOCALE_PATH

class Lang:
    def __init__(self, path, lang):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.texts = data.get(lang, {})

    def __getitem__(self, key):
        # Support nested keys with dot notation (e.g., "messages.start_game" or "errors.config_missing")
        keys = key.split('.')
        value = self.texts
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return f"[{key}]"
            else:
                return f"[{key}]"
        
        # return a lambda if text has placeholders
        if isinstance(value, str) and "{" in value:
            return lambda **kwargs: value.format(**kwargs)
        return value

lang = Lang(LOCALE_PATH, "en")