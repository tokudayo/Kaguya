import wikipedia
from datetime import datetime
import time
import requests

API_URL = 'http://en.wikipedia.org/w/api.php'
RATE_LIMIT = False
RATE_LIMIT_MIN_WAIT = None
RATE_LIMIT_LAST_CALL = None
USER_AGENT = 'wikipedia (https://github.com/goldsmith/Wikipedia/)'

def _wiki_request(params):
    global RATE_LIMIT_LAST_CALL
    global USER_AGENT

    params['format'] = 'json'
    if not 'action' in params:
        params['action'] = 'query'

    headers = {
        'User-Agent': USER_AGENT
    }

    if RATE_LIMIT and RATE_LIMIT_LAST_CALL and \
        RATE_LIMIT_LAST_CALL + RATE_LIMIT_MIN_WAIT > datetime.now():

    # it hasn't been long enough since the last API call
    # so wait until we're in the clear to make the request

        wait_time = (RATE_LIMIT_LAST_CALL + RATE_LIMIT_MIN_WAIT) - datetime.now()
        time.sleep(int(wait_time.total_seconds()))

    r = requests.get(API_URL, params=params, headers=headers)

    if RATE_LIMIT:
        RATE_LIMIT_LAST_CALL = datetime.now()

    return r.json()

def summary(title, sentences=0, chars=0, auto_suggest=True, redirect=True):
  # use auto_suggest and redirect to get the correct article
  # also, use page's error checking to raise DisambiguationError if necessary
  page_info = wikipedia.WikipediaPage(title, redirect=redirect)
  title = page_info.title
  pageid = page_info.pageid

  query_params = {
    'prop': 'extracts',
    'explaintext': '',
    'titles': title
  }

  if sentences:
    query_params['exsentences'] = sentences
  elif chars:
    query_params['exchars'] = chars
  else:
    query_params['exintro'] = ''

  request = _wiki_request(query_params)
  summary = request['query']['pages'][pageid]['extract']

  return summary

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
                self.shortSummary = summary(self.title, sentences=2)
            except wikipedia.exceptions.DisambiguationError:
                self.title = "Topic too broad."
        else:
            self.title = "No article found."