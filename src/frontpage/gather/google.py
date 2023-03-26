from frontpage.helpers import rss

class Google():
    """ TODO """

    def __init__(self, logger, config, country_codes, number_of_items):
        self.logger = logger
        self.config = config
        self.country_codes = country_codes
        self.number_of_items = number_of_items

    def get_trends(self):
        """ Fetch the first few titles from trending searches """

        all_feeds = []
        for this_country in self.country_codes:
            all_feeds.append(self.get_searches(this_country))

        return all_feeds

    def get_searches(self, country_code):
        """ Retrieve the first three items from Google's RSS feed of daily trends """

        results = rss.get_feed(f"https://trends.google.com/trends/trendingsearches/daily/rss?geo={country_code}", self.number_of_items)

        items = []
        for this_item in results:
            created_item = {
                'title' : this_item['title'],
                'summary' : this_item['ht_news_item_snippet']
            }

            items.append(created_item)

        return {country_code: items}
