'''
Created 2019-06-01 by NGnius
'''

from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    app.run(threaded=True)
