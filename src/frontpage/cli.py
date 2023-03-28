"""
Top level command for frontpage
"""

import logging
import click
from frontpage.helpers import configuration

from frontpage import __version__

__author__ = "Afraz Ahmadzadeh"
__copyright__ = "Afraz Ahmadzadeh"
__license__ = "MIT"


log_level = 'WARN'
logging.basicConfig(format='%(levelname)s: %(message)s', level=log_level)
logger = logging.getLogger(log_level)
logger.setLevel(log_level)
config = configuration.get_config(logger)

@click.group()
@click.option('-l', '--log-level', default='ERROR', help='How much logging to show', type=click.Choice(['DEBUG', 'WARN', 'ERROR', 'CRIT', 'INFO']))
@click.pass_context
def run(ctx, log_level): # pylint: disable=redefined-outer-name
    """
    What's going on today?
    """

    if ctx.obj is None:
        ctx.obj = {}

    config['log_level'] = log_level
    ctx.obj['config'] = config

from frontpage.gather.commands import gather as gather_commands
run.add_command(gather_commands)

from frontpage.display.commands import display as display_commands
run.add_command(display_commands)
