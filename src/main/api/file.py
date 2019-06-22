'''
File API routings

Created by NGnius 2019-06-22
'''
from flask import Blueprint, jsonify, request, send_file
from ..tools import api as api_tools
from ..tools import codes
from ..repo import file_service

bp = blueprint = Blueprint('api-file', __name__, url_prefix='/api/file')

''' Start of routes '''
@blueprint.route('/', methods=['GET'])
def get_file():
    # get file data
    err, id = do_preamble()
    if err is not None:
        return err
    file = file_service.get_file(id, file_like=True)
    return send_file(file, mimetype='audio/mp3')

@blueprint.route('/', methods=['POST'])
def save():
    # save file data
    err, id = do_preamble()
    if err is not None:
        return err
    file_service.save_file(id, request.data)
    return api_tools.error(200, 'Success')

''' End of routes '''

def do_preamble():
    id = get_id()
    if id is None:
        return api_tools.error(400, 'Missing of invalid file code/id. This should be the same code as used for the Sound.'), None
    return None, id

def get_id():
    code = request.args.get('code')
    if code is None:
        return
    return codes.code2id(code)

def acquire_file_lock(id):
    api_tools.start_single('file-%s' % id)

def release_file_lock(id):
    api_tools.end_single('file-%s' % id)
