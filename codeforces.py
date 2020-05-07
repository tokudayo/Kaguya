import requests, json

class CodeforcesUser:


    def __init__(self, query):
        self.handle = ""
        self.isNULL = True
        self.rating = 0
        self.rank = "No rank"
        self.country = "Unknown"
        self.avatar = ""
        self.ratingChange = []
        
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
            
            rawData = requests.get("https://codeforces.com/api/user.rating?handle=" + self.handle)
            ratingData = rawData.json()['result']
            for auto in ratingData:
                self.ratingChange.append((auto['ratingUpdateTimeSeconds'],auto['newRating']))
            jsonData = rawData.json()

