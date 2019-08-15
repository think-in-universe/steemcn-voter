# -*- coding:utf-8 -*-

from steem.comment import SteemComment
from action.vote.recipe import VoteRecipe
from utils.logging.logger import logger

# app specific parameter
APP = "steemcn"
BENEFICIARY_ACCOUNT = "steem-drivers"
BENEFICIARY_THRESHOLD = 5 # %
# voter configuration
VOTER_ACCOUNT = "steem-drivers"
VOTE_TIMING = 15 # mins
VOTE_WEIGHT = 25 # %

class SteemCnVoter(VoteRecipe):

    def mode(self):
        return "stream.comment"

    def by(self):
        return VOTER_ACCOUNT

    def what_to_vote(self, ops):
        posted_with_steemcn = self.ops.is_app(APP) and not self.ops.get_comment().is_comment()
        if posted_with_steemcn:
            logger.info("Find post {} published with [{}] app".format(self.ops.get_url(), APP))
            c = SteemComment(ops=ops)
            beneficiary = c.get_beneficiaries()
            if beneficiary >= BENEFICIARY_THRESHOLD:
                logger.info("Post {} has set {} beneficiary. I'll vote in {} minutes".format(self.ops.get_url(), beneficiary, VOTE_TIMING))
                return True
        return False

    def who_to_vote(self, author):
        return True # anyone

    def when_to_vote(self, ops):
        return VOTE_TIMING # mins

    def how_to_vote(self, post):
        return VOTE_WEIGHT # %
