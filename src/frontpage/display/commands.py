"""
TODO
"""

import click
import logging

@click.group()
@click.pass_context
def display(ctx): # pylint: disable=unused-argument
    """ Commands for displaying information """

    logger = logging.getLogger(ctx.obj['config']['log_level'])
    logger.setLevel(ctx.obj['config']['log_level'])
    ctx.obj['logger'] = logger

@display.command()
@click.option('--page', '-p', default='front', type=click.Choice(['front', 'web', 'news', 'weather']), help='Which page to display')
@click.option('--mock', '-m', is_flag=True, default=False, help='Mock the Inky board, for testing')
@click.pass_context
def inky(ctx, page, mock):
    """ Display information on Inky ePaper display """

    from frontpage.display.inky import Inky
    this_inky = Inky(ctx.obj['logger'], ctx.obj['config'], page, mock)
    this_inky.main()
    ctx.obj['logger'].info(f"Successfully created image")
