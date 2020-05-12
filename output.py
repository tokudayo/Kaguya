def dumpToFile(**kwargs):
    f = open(kwargs['path'],'w+', encoding='utf-8')
    f.write(kwargs['response'])
    f.close()