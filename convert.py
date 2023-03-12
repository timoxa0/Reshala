import commentjson as json


def clearStr(input, mask):
    l = [i for i in input]
    m = [i for i in mask]
    l.sort()
    m.sort()
    for i in m:
        l.remove(i)
    if len(l) >= 1:
        l = list(dict.fromkeys(l))[0]
    elif l == []:
        l = ''
    return l


def main():
    with open('errors.json', 'r') as file:
        e_log = json.load(file)

    with open('oks.json', 'r') as file:
        o_log = json.load(file)
    Dict = o_log
    for word in e_log:
        answer = clearStr(e_log[word], word)
        Dict[word] = answer

    print(Dict)
    with open('dictionary.json', 'w') as file:
        json.dump(Dict, file)


if __name__=='__main__':
    main()
