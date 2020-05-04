import requests, json, pprint, discord
async def cfResponse(user, message):
    if user.mentioned_in(message):
        url = "https://codeforces.com/api/blogEntry.comments?blogEntryId=76830"
        rawData = requests.get(url)
        jsonData = rawData.json()
        if jsonData['status'] == 'OK':
            data = jsonData['result']
            response = ""
            for comment in data: 
                response += comment['commentatorHandle'] + ", upvote: " + str(comment['rating']) + '\n'
        await message.channel.send(response)