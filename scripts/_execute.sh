#!/bin/sh

set -e

nohup pipenv run invoke recipe.vote -r steemcn_daily &
