import commentjson as json
import os


class Lang:
    def __init__(self, dictfile):
        self.dictfile = dictfile
        if not os.path.exists(self.dictfile):
            with open(self.dictfile, 'w', encoding='utf-8') as file:
                json.dump({
                        "gui": {
                            "title": "Решамба",
                            "saveExitBtn": "Сохранить и выйти",
                            "saveRunBtn": "Сохранить и запустить",

                            "basicSettings": {
                                "tabName": "Базовые",
                                "loginLabel": "Логин:",
                                "passwordLabel": "Пароль:",
                                "delayLabel": "Задержка:",
                                "downDelayLimitLabel": "От:",
                                "topDelayLimitLabel": "До:",
                                "secLabel": "сек"
                            },
                            "dictionarySettings": {
                                "tabName": "Словарь",
                                "serverIPLabel": "IP Сервера:",
                                "loginLabel": "Логин:",
                                "passwordLabel": "Пароль:",
                                "useDictionaryLabel": "Использовать словарь:"
                            },
                            "advancedSettings": {
                                "tabName": "Прочие",
                                "logLevelLabel": "Уровень логов:",
                                "acLabel": "Продолжать всегда:",
                                "chromeProcessLabel": "Процесс Chrome:",
                                "driverProcessLabel": "Процесс Driver:"
                            },
                            "other": {
                                "yes": "Да",
                                "no": "Нет"
                            }
                        }
                    }, file, indent=4)

    def load(self) -> dict:
        with open(self.dictfile, 'r', encoding='utf-8') as file:
            return json.load(file)

    def dump(self, dictionary) -> None:
        with open(self.dictfile, 'w', encoding='utf-8') as file:
            json.dump(dictionary, file, indent=4)
