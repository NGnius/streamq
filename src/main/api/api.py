'''
Base api routing provider

Created by NGnius 2019-03-31
'''

from flask import Blueprint
from flask import jsonify
from flask import request
from . import queue
from . import sound
from . import file
from ..tools import api as api_tools

# password & debug dependencies
from os import getenv
from random import SystemRandom
from ..tools import codes

bp = blueprint = Blueprint('api', __name__, url_prefix='/api')

def register_blueprints(app):
    app.register_blueprint(blueprint)
    app.register_blueprint(queue.blueprint)
    app.register_blueprint(sound.blueprint)
    app.register_blueprint(file.blueprint)

# password & debug stuff
MODE = getenv('STREAMQ_MODE', 'DISABLED')
if MODE == 'DEBUG':
    password = codes.code2id('DEBUG')
elif MODE != 'DISABLED':
    random = SystemRandom()
    password = random.randint(1000000000, 999999999999)

if MODE != 'DISABLED':
    print('API Admin password: %s' % codes.id2code(password))

    @bp.route('/shutdown')
    def shutdown():
        if api_tools.get_param('password') == codes.id2code(password):
            func = request.environ.get('werkzeug.server.shutdown')
            if func is None:
                raise RuntimeError('Not running with the Werkzeug Server')
            func()
            return api_tools.error(200, 'Okay')
        else:
            return api_tools.error(403, 'You do not have valid credentials to access this page')

    @bp.route('/test')
    def test():
        if api_tools.get_param('password') == codes.id2code(password):
            return api_tools.error(200, 'Okay')
        else:
            return api_tools.error(403, 'You do not have valid credentials to access this page')
