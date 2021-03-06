# -*- coding:utf-8 -*-

import requests
import time
# from steem.settings import settings
# from utils.logging.logger import logger

SCOT_API_URL = "https://scot-api.steem-engine.com/{}"

cached = {
    "token_info": {},
    "token_config": {},
    "author": {},
    "comment": {}
}

def _http_api(path, retries=5):
    try:
        r = requests.get(SCOT_API_URL.format(path))
        if r.ok:
            return r.json()
        else:
            return None
    except:
        if retries > 0:
            return _http_api(path, retries-1)
        else:
            return None

def _entity_data(key, entity):
    if entity is not None:
        if entity in cached[key]:
            info = cached[key][entity]
            if time.time() < info['expiration']:
                return info['data']
        info = {}
        info['data'] = _http_api(entity)
        info['expiration'] = time.time() + 60 * 1 # minutes
        cached[key][entity] = info
        return info['data']
    return None

def author(author):
    return _entity_data("author", "@"+author)

def comment(author, permlink):
    return _entity_data("comment", "@"+author+"/"+permlink)

def _token_data(key, symbol):
    if symbol is not None:
        cached_key = 'token_{}'.format(key)
        if symbol in cached[cached_key]:
            info = cached[cached_key][symbol]
            if time.time() < info['expiration']:
                return info['data']
        info = {}
        info['data'] = _http_api("{}?token={}".format(key, symbol))
        info['expiration'] = time.time() + 60 * 5 # minutes
        cached[cached_key][symbol] = info
        return info['data']
    return None

def _token_item(key, symbol, item):
    data = _token_data(key, symbol)
    if data is not None:
        if item is not None:
            if item in data:
                return data[item]
        else:
            return data
    return None

def token_info(symbol, item=None):
    return _token_item("info", symbol, item)

def token_config(symbol, item=None):
    return _token_item("config", symbol, item)

def get_discussions(mode="created", token=None, tag=None, limit=-1, start_author=None, start_permlink=None):
    params = ""
    if tag:
        params += "&tag={}".format(tag)
    if limit and limit > 0:
        params += "&limit={}".format(limit)
    if start_author:
        params += "&start_author={}".format(start_author)
    if start_permlink:
        params += "&start_permlink={}".format(start_permlink)
    return _http_api("get_discussions_by_{}?token={}{}".format(mode, token, params))
