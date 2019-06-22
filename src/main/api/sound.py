'''
Sound API routings

Created by NGnius 2019-06-22
'''
from flask import Blueprint, jsonify
from ..tools import api as api_tools
from ..tools import codes
from ..repo import sound_service
from ..objects.sound import Sound

bp = blueprint = Blueprint('api-sound', __name__, url_prefix='/api/sound')

''' Start of routes '''
@blueprint.route('/', methods=['GET', 'POST'])
def get_sound():
    # get sound
    err, id = do_preamble(lock=True)
    if err is not None:
        return err
    sound = sound_service.get_sound(id, create=False)
    if sound is None:
        release_sound_lock(id)
        return api_tools.error(404, 'Sound does not exist')
    refresh_metadata = api_tools.get_param('refresh')
    if refresh_metadata is not None and refresh_metadata.lower() in ['true', 't']:
        sound.populate_metadata()
        sound_service.save_sound(sound)
    release_sound_lock(id)
    return jsonify(sound.to_jsonable())

@blueprint.route('/new', methods=['GET','POST'])
def new():
    # create new sound
    new_sound = Sound()
    sound_service.save_sound(new_sound)
    acquire_sound_lock(new_sound.id)
    release_sound_lock(new_sound.id)
    return jsonify(new_sound.to_jsonable())

''' End of routes '''

def do_preamble(id_is_optional=False, lock=False):
    id = get_id()
    if id is None and id_is_optional is False:
        return api_tools.error(400, 'Missing or invalid sound code/id.'), None
    if lock is True:
        acquire_sound_lock(id)
    return None, id

def get_id():
    code = api_tools.get_param('code')
    if code is None:
        return
    return codes.code2id(code)

def acquire_sound_lock(id):
    api_tools.start_single('sound-%s' % id)

def release_sound_lock(id):
    api_tools.end_single('sound-%s' % id)
