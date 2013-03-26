#!/usr/bin/env python
# Get pool information.

import logging
import urllib2
import json

# Convert guild name to valid class name
NameTable = {'50btc': 'Fiftybtc'}

def getpool(name, apikey):
    if name in NameTable:
        name = NameTable[name]

    if not name in globals():
        return None

    poolclass = globals()[name]

    return poolclass(apikey)

class Btcguild:
    def __init__(self, apikey):
        self.apikey = apikey

    def get_status(self):
        req = urllib2.urlopen('https://www.btcguild.com/api.php?api_key=%s' %
                self.apikey)
        response = req.read()

        try:
            data = json.loads(response)

            # Create standard format
            workers = {}
            for key in data['workers']:
                worker = data['workers'][key]
                workers[worker['worker_name']] = { 'hash_rate': float(worker['hash_rate']) }
            data['std'] = { 'workers' : workers }
        except:
            return {}
        return data

# 50BTC
class Fiftybtc:
    def __init__(self, apikey):
        self.apikey = apikey

    def get_status(self):
        req = urllib2.urlopen('https://50btc.com/api/%s' %
                self.apikey)
        response = req.read()

        try:
            data = json.loads(response)

            # Create standard format
            workers = {}
            for key in data['workers']:
                worker = data['workers'][key]
                workers[worker['worker_name']] = { 'hash_rate': float(worker['hash_rate']) }
            data['std'] = { 'workers' : workers }
        except:
            return {}
        return data

class Slush:
    def __init__(self, apikey):
        self.apikey = apikey

    def get_status(self):
        req = urllib2.urlopen('https://mining.bitcoin.cz/accounts/profile/json/%s' %
                self.apikey)
        response = req.read()

        try:
            data = json.loads(response)

            # Create standard format
            workers = {}
            for key in data['workers']:
                worker = data['workers'][key]
                workers[key] = { 'hash_rate': worker['hashrate'] }
            data['std'] = { 'workers' : workers }
        except:
            return {}
        return data

