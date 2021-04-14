import json
import os
from typing import Optional

from src.decorators import handle_exception

TEMPLATE_ROLE_ARN_KEY = "TemplateRoleArn"
SUPPORTED_KEYS = [TEMPLATE_ROLE_ARN_KEY]
CONFIG_FILE_PATH = "~/.imp.json"


class ConfigManager:
    def __init__(self):
        self.file = os.path.expanduser(CONFIG_FILE_PATH)

    def list(self) -> Optional[dict]:
        if os.path.isfile(self.file):
            with open(self.file, 'r') as stream:
                return json.load(stream)
        else:
            return None

    def get(self, key: str) -> Optional[str]:
        if os.path.isfile(self.file):
            with open(self.file, 'r') as read_stream:
                return json.load(read_stream).get(key)
        else:
            return None

    @handle_exception
    def set(self, key: str, value: str) -> None:
        if key in SUPPORTED_KEYS:

            if os.path.isfile(self.file):
                with open(self.file, 'r') as read_stream:
                    data = json.load(read_stream)
                    data[key] = value
                    with open(self.file, 'w') as write_stream:
                        json.dump(data, write_stream)
            else:
                with open(self.file, 'w') as stream:
                    json.dump({key: value}, stream)
        else:
            raise Exception(f"Only the following keys are supported: {', '.join(SUPPORTED_KEYS)}")
