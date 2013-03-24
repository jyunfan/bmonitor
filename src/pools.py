#!/usr/bin/env python

import logging
import urllib2
import json

class Btcguild:
    def __init__(self, apikey):
        self.apikey = apikey

    def get_status(self):
        req = urllib2.urlopen('https://www.btcguild.com/api.php?api_key=%s' %
                self.apikey)
        response = req.read()

        try:
            data = json.loads(response)
        except:
            return {}
        return data

