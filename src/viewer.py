#!/usr/bin/env python

import shelve
import pprint

import setting
from bottle import route, run
from templet import stringfunction

@stringfunction
def pool_template(db):
    """
    ${{
        for key in db.keys():
            out.append('<h1>%s</h1>' % key)
            out.append('<pre>%s</pre>' % pprint.pformat(db[key]))
    }}
    """

@route('/pool')
def show_pool():
    db = shelve.open(setting.DB_FILE)
    html = pool_template(db)
    db.close()
    return html

run(host='0.0.0.0', port=2100)
