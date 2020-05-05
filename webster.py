import requests, json
url = 'https://dictionaryapi.com/api/v3/references/learners/json/'
APIKey = '?key=281250e6-3e7e-4487-9b65-768400628bc0'

def defineWord(query):
    rawData = requests.get(url + query + APIKey)
    jsonData = rawData.json()
    data = jsonData[0]
    if type(data) != dict: #data is a string
        print("Requested word not found in database, showing result for " + data)
        rawData = requests.get(url + data + APIKey)
        jsonData = rawData.json()
        data = jsonData[0]
        print("Showing definition for " + data["meta"]["id"])
    for auto in data['shortdef']: print(auto)
    print("Stems")
    for auto in data['meta']['stems']: print(auto,end=', ')

defineWord("concac")