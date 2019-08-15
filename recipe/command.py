# -*- coding:utf-8 -*-

from invoke import task

from steem.settings import settings
from utils.logging.logger import logger

from recipe.vote.cookbook import VoteCookbook


@task(help={
      'recipe': 'the recipe to run',
      'debug': 'enable the debug mode'
      })
def vote(ctx, recipe=None, debug=False):
    """ run a specific vote recipe"""

    # if debug:
        # settings.set_debug_mode()

    settings.set_steem_node()

    cookbook = VoteCookbook()
    cookbook.cook(recipe)
