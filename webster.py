import requests, json
url = 'https://dictionaryapi.com/api/v3/references/learners/json/'
APIKey = '?key=281250e6-3e7e-4487-9b65-768400628bc0'

class Word:
    def __init__(self, word, definition, stems):
        self.isNULL = False
        self.word = word
        self.definition = definition
        self.stems = stems

    word = ""
    definition = []
    stems = []
    isNULL = True

    def getWord(self, query):
        rawData = requests.get(url + query + APIKey)
        jsonData = rawData.json()
        data = jsonData[0]
        if type(data) != dict: #data is a string
            rawData = requests.get(url + data + APIKey)
            jsonData = rawData.json()
            data = jsonData[0]
            
        self = Word(data['meta']['id'], data['shortdef'], data['meta']['stems'])