import feedparser
import logging

def main(config, country_codes):
    """ Main function for this command """

    all_feeds = []
    for this_country in country_codes:
        all_feeds.append(get_first_three_topics(this_country))

    return all_feeds

def get_first_three_topics(country_code):
    """ Retrieve the first three items from Google's RSS feed of daily trends """

    first_three = feedparser.parse(f"https://trends.google.com/trends/trendingsearches/daily/rss?geo={country_code}")['entries'][0:3]
    topics = [this_entry['title']  for this_entry in first_three]

    return {country_code: topics}
