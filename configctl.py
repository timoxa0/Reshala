import commentjson as json
import os


class Config:
    def __init__(self, dictfile):
        self.dictfile = dictfile
        if not os.path.exists(self.dictfile):
            with open(self.dictfile, 'w', encoding='utf-8') as file:
                json.dump({
                        "basic": {
                            "login": "",
                            "password": "",
                            "toplimit": 3,
                            "downlimit": 2
                        },
                            "dictionary": {
                                "server": "1.2.3.4",
                                "userID": "12345678",
                                "userKey": "87654321",
                                "use": 1
                        },
                        "advanced": {
                            "logLevel": "DEBUG",
                            "logfmt": "{%(name)s} %(levelname)s: %(message)s",
                            "Always Continue": 0,
                            "chrome_process": "chrome.exe",
                            "driver_process": "chromedriver.exe"
                    }
                }, file, indent=4)

    def load(self) -> dict:
        with open(self.dictfile, 'r', encoding='utf-8') as file:
            return json.load(file)

    def dump(self, dictionary) -> None:
        with open(self.dictfile, 'w', encoding='utf-8') as file:
            json.dump(dictionary, file, indent=4)
