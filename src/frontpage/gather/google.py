import feedparser

class Google():
    """ TODO """

    def __init__(self, logger, config, country_codes):
        self.logger = logger
        self.config = config
        self.country_codes = country_codes

    def get_trends(self):
        """ Fetch the first few titles from trending searches """

        all_feeds = []
        for this_country in self.country_codes:
            all_feeds.append(self.get_first_three_topics(this_country))

        return all_feeds

    def get_first_three_topics(self, country_code):
        """ Retrieve the first three items from Google's RSS feed of daily trends """

        first_three = feedparser.parse(f"https://trends.google.com/trends/trendingsearches/daily/rss?geo={country_code}")['entries'][0:3]
        topics = [this_entry['title']  for this_entry in first_three]

        return {country_code: topics}
