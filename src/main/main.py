'''
Created 2019-06-01 by NGnius
'''

from flask import Flask
from .repo import gherkin

gherkin.set_db('stream-q.db')

app = Flask(__name__)

if __name__ == '__main__':
    app.run(threaded=True)
