import requests, json
url = 'https://dictionaryapi.com/api/v3/references/learners/json/'
APIKey = '?key=281250e6-3e7e-4487-9b65-768400628bc0'

class Word(object):
    word = ""
    definition = []
    stems = []
    isNULL = True

    def __init__(self, query):
        self.isNULL = False
        rawData = requests.get(url + query + APIKey)
        jsonData = rawData.json()
        data = jsonData[0]
        if data.size() == 0:
            return
            
        if type(data) != dict: #data is a string
            rawData = requests.get(url + data + APIKey)
            jsonData = rawData.json()
            data = jsonData[0]
        self.word = data['meta']['id']
        self.definition = data['shortdef']
        self.stems = data['meta']['stems']
        return