from frontpage.helpers import rss

class News():
    """ TODO """

    def __init__(self, logger, config, number_of_items):
        self.logger = logger
        self.config = config
        self.number_of_items = number_of_items
        self.url = "http://feeds.bbci.co.uk/news/rss.xml"

    def main(self):
        """ TODO """

        results = rss.get_feed(self.url, self.number_of_items)

        items = []
        for this_item in results:
            created_item = {
                'title' : this_item['title'],
                'summary' : this_item['summary']
            }

            items.append(created_item)

        return items
