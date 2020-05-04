import requests, json
async def test(context):
    url = "https://codeforces.com/api/blogEntry.comments?blogEntryId=76830"
    rawData = requests.get(url)
    jsonData = rawData.json()
    if jsonData['status'] == 'OK':
        data = jsonData['result']
        response = ""
        for comment in data: 
            response += comment['commentatorHandle'] + ", upvote: " + str(comment['rating']) + '\n'
    await context.send(response)