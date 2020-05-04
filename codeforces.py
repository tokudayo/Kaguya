import requests, json

class CodeforcesUser:
    def __init__(self, query):
        url = "https://codeforces.com/api/user.info?handles=" + query
        rawData = requests.get(url)
        jsonData = rawData.json()
        if jsonData['status'] == 'OK':
            data = jsonData['result']
            data = data[0]
            self.isNULL = False
            self.handle = data['handle']
            self.rating = data['rating']
            self.rank = data['rank']
            if 'country' in data: self.country = data['country']

    handle = ""
    isNULL = True
    rating = -1
    rank = "Undefined"
    country = "Undefined"
