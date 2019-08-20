# -*- coding:utf-8 -*-

import sys
from steem.account import SteemAccount
from steem.comment import SteemComment
from action.vote.recipe import VoteRecipe
from utils.logging.logger import logger


# app specific parameter
SEARCH_BY_TOKEN = "MARLIANS" # "UFM"
TRIBE_TAG = "cn"
APP = "steemcn"
BENEFICIARY_ACCOUNT = "steem-drivers"
BENEFICIARY_THRESHOLD = 5 # %
# voter configuration
VOTER_ACCOUNT = "steem-drivers"
VOTE_TIMING = 15 # mins
DAILY_VOTE_TIMING = 5 # mins
VOTE_WEIGHT = 25 # %
VOTE_CYCLE = 1.05 # days
VOTE_PER_ACCOUNT_LIMIT = 2
BLACKLIST = []
ACCOUNT_REPUTATION_THRESHOLD = 35


class SteemCnVoter(VoteRecipe):

    def mode(self):
        return "stream.comment"

    def by(self):
        return VOTER_ACCOUNT

    def what_to_vote(self, ops):
        posted_with_steemcn = self.ops.is_app(APP) and not self.ops.is_comment()
        if posted_with_steemcn:
            logger.info("Find post {} published with [{}] app".format(self.ops.get_url(), APP))
            c = SteemComment(ops=ops)
            beneficiary = c.get_beneficiaries(account=BENEFICIARY_ACCOUNT)
            if beneficiary >= BENEFICIARY_THRESHOLD:
                logger.info("Post {} has set {} beneficiary.".format(self.ops.get_url(), beneficiary, VOTE_TIMING))
                return True
        return False

    def who_to_vote(self, author):
        return True # anyone

    def when_to_vote(self, ops):
        return VOTE_TIMING # mins

    def how_to_vote(self, post):
        return VOTE_WEIGHT # %


class SteemCnDailyVoter(SteemCnVoter):

    def __init__(self):
        super().__init__()
        self.authors = {}
        self.posts_num = 0
        self.voted_posts = 0

    def mode(self):
        return "query.comment.post"

    def config(self):
        return {
            "token": SEARCH_BY_TOKEN, # the token is necessary because the query may miss some posts when the total number of tags exceeds 5
            "tag": TRIBE_TAG,
            "days": VOTE_CYCLE
        }

    def who_to_vote(self, author):
        if author in BLACKLIST:
            logger.info("Skip [{}] who is in my blacklist".format(author))
            return False

        account = SteemAccount(author)
        if account.reputation() < ACCOUNT_REPUTATION_THRESHOLD:
            logger.info("Skip [{}] whose reputation is too low".format(author))
            return False

        if self.authors.get(author) is None:
            self.authors[author] = 1
            self.posts_num += 1
            return True
        elif self.authors.get(author) < VOTE_PER_ACCOUNT_LIMIT:
            self.authors[author] += 1
            self.posts_num += 1
            return True
        elif self.authors.get(author) >= VOTE_PER_ACCOUNT_LIMIT:
            return False
        return False

    def when_to_vote(self, ops):
        return DAILY_VOTE_TIMING # mins

    def how_to_vote(self, post):
        self.voted_posts += 1
        logger.info("voting {} / {} posts".format(self.voted_posts, self.posts_num))
        weight = self.voter.estimate_vote_pct_for_n_votes(days=VOTE_CYCLE, n=self.posts_num)

        if weight  > 100:
            weight = 100

        return weight

    def after_success(self, res):
        if self.voted_posts == self.posts_num:
            logger.info("Done with voting. Exit.")
            sys.exit()
