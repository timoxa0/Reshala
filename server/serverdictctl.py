import commentjson as json
import pickle
import os

class Dictionary:
    def __init__(self, dictfile):
        self.dictfile = dictfile
        if not os.path.exists(self.dictfile):
            with open(self.dictfile, 'w', encoding='utf-8') as file:
                json.dump({}, file)

    def load(self) -> dict:
        with open(self.dictfile, 'r', encoding='utf-8') as file:
            return json.load(file)

    def dump(self, dictionary) -> None:
        with open(self.dictfile, 'w', encoding='utf-8') as file:
            json.dump(dictionary, file, indent=4)


class ServerDict:

    def __init__(self, filename) -> None:
        self.dictionaryctl = Dictionary(filename)
    

    def dump(self, pickle_dictionary) -> None:
        dictionary = self.dictionaryctl.load()
        new_dictionary = pickle.loads(pickle_dictionary)
        for i in new_dictionary:
            if not i in dictionary:
                dictionary[i] = new_dictionary[i]
        
        self.dictionaryctl.dump(dictionary)
    

    def load(self) -> dict:
        return pickle.dumps(self.dictionaryctl.load())

