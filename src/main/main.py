'''
Created 2019-06-01 by NGnius
'''

from flask import Flask
from .repo import gherkin
from os import getenv
if getenv('STREAMQ_MODE', 'DISABLED') == 'DEBUG':
    gherkin.set_db('streamq_test.db')
else:
    gherkin.set_db('stream-q.db')
from .api import api

app = Flask(__name__)

def run():
    api.register_blueprints(app)
    app.run(host='0.0.0.0', threaded=True)

if __name__ == '__main__':
    run()
