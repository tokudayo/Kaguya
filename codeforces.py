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
            if 'rating' in data: self.rating = data['rating']
            if 'rank' in data: self.rank = data['rank']
            self.avatar = data['avatar']
            if 'country' in data: self.country = data['country']

    handle = ""
    isNULL = True
    rating = 0
    rank = "No rank"
    country = "Unknown"
    avatar = ""