import requests, json
url = 'https://dictionaryapi.com/api/v3/references/collegiate/json/'
APIKey = '?key=6ee7b300-6ade-4755-9651-131478041b21'

class Word(object):
    word = ""
    definition = []
    stems = []
    isNULL = True
    redirected = False

    def __init__(self, query):
        rawData = requests.get(url + query + APIKey)
        jsonData = rawData.json()
        if len(jsonData) == 0: return
        self.isNULL = False
        self.word = query
        data = jsonData[0]
        if type(data) != dict: #data is a string
            self.redirected = True
            self.word = data
            rawData = requests.get(url + data + APIKey)
            jsonData = rawData.json()
            data = jsonData[0]
        self.definition = data['shortdef']
        self.stems = data['meta']['stems']
        return