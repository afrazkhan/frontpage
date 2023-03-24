"""
TODO
"""

import click
import logging

@click.group
@click.pass_context
def gather(ctx): # pylint: disable=unused-argument
    """ Commands for gathering information around the web """

    logger = logging.getLogger(ctx.obj['config']['log_level'])
    logger.setLevel(ctx.obj['config']['log_level'])
    ctx.obj['logger'] = logger

@gather.command()
@click.option("--country-code", "-c", multiple=True, default=['GB', 'NL'], help="Country code for where to get info from. Can be given multipled times")
@click.pass_context
def google(ctx, country_code):
    """ Look up security groups associated with [hostname], and add port allowances for this machine's IP """

    from frontpage.gather import google as this_google
    print(this_google.main(ctx.obj['config'], country_code))

@gather.command()
@click.option("--city", "-c", default=None, help="City to get weather for")
@click.option("--coords", "-o", default=None, help="Give latitude and logitude as'lat,lon'")
@click.pass_context
def weather(ctx, city, coords):
    """ Weather """

    from frontpage.gather import weather as this_weather
    print(this_weather.main(ctx.obj['config'], ctx.obj['logger'], city, coords))
