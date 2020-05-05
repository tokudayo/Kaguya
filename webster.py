import requests, json
url = 'https://dictionaryapi.com/api/v3/references/collegiate/json/'
APIKey = '?key=6ee7b300-6ade-4755-9651-131478041b21'

class Word(object):

    def __init__(self, query):
        self.word = ""
        self.definition = []
        self.stems = []
        self.isNULL = True
        self.redirected = False
        rawData = requests.get(url + query + APIKey)
        jsonData = rawData.json()
        if len(jsonData) == 0: return
        self.isNULL = False
        self.word = query
        check = jsonData[0]
        if type(check) != dict: #no definition found, but there are closely related words
            self.redirected = True
            self.word = check
            rawData = requests.get(url + check + APIKey)
            jsonData = rawData.json()
        for data in jsonData:
            self.definition += data['shortdef']
            #self.stems += data['meta']['stems']
        return