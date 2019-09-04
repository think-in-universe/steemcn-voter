#!/bin/sh

set -e

pipenv run invoke recipe.vote -r steemcn_daily
