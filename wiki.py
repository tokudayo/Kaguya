from wikipedia import search, summary, WikipediaPage

class WikiPage():
    def __init__(self, args):
        self.title = ""
        query = ""
        print(args)
        for auto in args:
            query += auto + " "
        suggestions = search(query)
        print(suggestions)
        if len(suggestions):
            self.title = suggestions[0]
        self.shortSummary = summary(query, sentences=2)