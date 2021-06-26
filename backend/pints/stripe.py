import pandas as pd
pd.set_option("display.max_rows", 1000)
pd.set_option("display.max_columns", 200)
pd.set_option("display.max_colwidth", 2000)
import datetime
import os
import sys
import time
import requests
import json
import io
import concurrent.futures

import pdb

import collections

import pints

import stripe
# apiKey = os.environ.get('PAPER_STRIPE_API_KEY')

from logger import logger

longrun = concurrent.futures.ThreadPoolExecutor(max_workers=None)

# stripe.api_key = STRIPE_API_KEY

objs = {
    'coupons': {
        'api': stripe.Coupon,
        'expand': []
    },
    'customers': {
        'api': stripe.Customer,
        'expand': []
    },
    'subscriptions': {
        'api': stripe.Subscription,
        'expand': [],
        'all': True,
    },
    'plans': {
        'api': stripe.Plan,
        'expand': []
    },
    'invoices': {
        'api': stripe.Invoice,
        'expand': ['data.discounts']
    }
}

def getAll(engine, teamId):
    for key, obj in objs.items():
        longrun.submit(getObject, engine, teamId, key)
    return True

def getObject(engine, teamId, obj):
    apiKey = pints.pints.postgres.getStripeApiKey(engine, teamId)
    table = f'stripe_{obj}'
    getAll = objs[obj].get('all', False)
    if getAll:
        mr = False
    else:
        mr = pints.postgres.getMaxRecord(engine, table, teamId)
    logger.info(f'{obj} mr: {mr}')
    if mr:
        logger.info(f'{obj} with mr: {mr}')
        temp = objs[obj]['api'].list(limit=100, api_key=apiKey, created={'gt': mr}, expand=objs[obj]['expand'])
    elif getAll:
        temp = objs[obj]['api'].list(limit=100, status='all', api_key=apiKey, expand=objs[obj]['expand'])
    else:
        logger.info(f'{obj} without mr: {mr}')
        temp = objs[obj]['api'].list(limit=100, api_key=apiKey, expand=objs[obj]['expand'])
    ls = []
    for t in temp.auto_paging_iter():
        ls.append(t)
    logger.info(f'done getting {obj}, got {len(ls)} after {mr}')
    if getAll:
        pints.postgres.deleteRows(engine, table, teamId)
        logger.info(f'done deleteRows for {obj} ({len(ls)} rows)')
    pints.postgres.insertRows(engine, table, ls, teamId)
    logger.info(f'done inserting rows for {obj} ({len(ls)} rows)')
    return ls
