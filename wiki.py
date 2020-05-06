import wikipedia

class WikiPage():
    def __init__(self, args):
        self.title = ""
        self.shortSummary = ""
        self.url = "https://en.wikipedia.org/wiki/"
        query = ""
        print(args)
        for auto in args:
            query += auto + " "
        suggestions = wikipedia.search(query)
        print(suggestions)
        if len(suggestions):
            self.title = suggestions[0]
            urlSuffix = ""
            for auto in self.title.split()[:len(self.title.split())-1]: urlSuffix += auto + "_"
            urlSuffix += self.title.split()[len(self.title.split())-1]
            self.url += urlSuffix
            print(self.url)
            try:
                summaryQuery = "" # There is a odd bug in the wikipedia package. wikipedia.summary("mercury (planet)")
                for char in self.title:
                    if char != ')' and char != '(':
                        summaryQuery += char
                self.shortSummary = wikipedia.summary(summaryQuery, sentences=2)
            except wikipedia.exceptions.DisambiguationError:
                self.title = "Topic too broad."
        else:
            self.title = "No article found."