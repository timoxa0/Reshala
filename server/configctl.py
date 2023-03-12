import commentjson as json
import os


class Config:
    def __init__(self, dictfile):
        self.dictfile = dictfile
        if not os.path.exists(self.dictfile):
            with open(self.dictfile, 'w', encoding='utf-8') as file:
                json.dump({
                        "users": {
                            "testUser": "password"
                        },
                        "logfmt": "{%(name)s} %(levelname)s: %(message)s",
                        "logLevel": "DEBUG"
                }, file, indent=4)

    def load(self) -> dict:
        with open(self.dictfile, 'r', encoding='utf-8') as file:
            return json.load(file)

    def dump(self, dictionary) -> None:
        with open(self.dictfile, 'w', encoding='utf-8') as file:
            json.dump(dictionary, file, indent=4)
