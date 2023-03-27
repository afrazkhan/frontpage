"""
TODO
"""

import click
import logging

@click.group()
@click.pass_context
def gather(ctx): # pylint: disable=unused-argument
    """ Commands for gathering information around the web """

    logger = logging.getLogger(ctx.obj['config']['log_level'])
    logger.setLevel(ctx.obj['config']['log_level'])
    ctx.obj['logger'] = logger

@gather.command()
@click.option('--country-code', '-c', multiple=True, default=['NL'], help='Country code for where to get info from. Can be given multipled times')
@click.option('--number-of-items', '-n', default=3, help='Number of items to fetch')
@click.pass_context
def google(ctx, country_code, number_of_items):
    """ Get the latest search trends """

    from frontpage.gather.google import Google
    this_google = Google(ctx.obj['logger'], ctx.obj['config'], country_code, number_of_items)
    print(this_google.main())

@gather.command()
@click.option("--city", "-c", help="City to get weather for")
@click.option("--coords", "-o", help="Give latitude and logitude as'lat,lon'")
@click.pass_context
def weather(ctx, city, coords):
    """ Show the current weather """

    from frontpage.gather.weather import Weather
    this_weather = Weather(ctx.obj['logger'], ctx.obj['config'], city, coords)
    print(this_weather.main())

@gather.command()
@click.pass_context
@click.option('--number-of-items', '-n', default=3, help='Number of items to fetch')
def news(ctx, number_of_items):
    """ Todays news """

    number_of_items = ctx.obj['config'].get('number_of_items') or number_of_items

    from frontpage.gather.news import News
    this_news = News(ctx.obj['logger'], ctx.obj['config'], number_of_items)
    print(this_news.main())
