import requests, json
url = 'https://dictionaryapi.com/api/v3/references/collegiate/json/'
encryptedKey = "5a[o3,[[-X)&&#,WZ[#*-++#/,+'#')'*-.&*'X('"
APIKey = ""
for auto in encryptedKey: APIKey += chr(ord(auto) + 10)

class Word(object):

    def __init__(self, query):
        self.word = ""
        self.definition = []
        self.stems = []
        self.isNULL = True
        self.redirected = False
        lookup = ""
        for auto in query.split()[0:len(query.split())-1]:
            lookup += auto + '-'
        lookup += query.split()[len(query.split())-1]
        rawData = requests.get(url + lookup + APIKey)
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