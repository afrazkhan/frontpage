import feedparser

def get_feed(url, number_of_items):
    """ TODO """

    feed = feedparser.parse(url)['entries'][0:number_of_items]

    return feed
