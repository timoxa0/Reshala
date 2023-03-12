import syncdictctl

d = syncdictctl.ServerDictionary()
#dd = d.load()
d.load()
print(d.cache)