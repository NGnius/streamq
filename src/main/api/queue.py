'''
Queue API routings

Created by NGnius 2019-06-15
'''

from flask import Blueprint, jsonify
from . import api
from ..tools import api as api_tools
from ..tools import codes
from ..repo import queue_service
from ..repo import sound_service
from ..objects.queue import SoundQueue

bp = blueprint = Blueprint('api-queue', __name__, url_prefix='/api/queue')

''' Start of routes '''
@blueprint.route('/', methods=['GET', 'POST'])
def get_queue():
    # get queue
    err, queue = do_preamble(lock=True)
    if err is not None:
        return err
    release_queue_lock(queue.id)
    return jsonify(queue.to_jsonable())

@blueprint.route('/new', methods=['GET', 'POST'])
def new():
    # create new queue
    queue = SoundQueue()
    queue_service.save_queue(queue)
    acquire_queue_lock(queue.id)
    release_queue_lock(queue.id)
    return jsonify(queue.to_jsonable())

@blueprint.route('/shuffle', methods=['GET', 'POST'])
def shuffle():
    # enable or disable shuffle mode
    err, queue = do_preamble(lock=True)
    if err is not None:
        return err
    shuffle_mode = api_tools.get_param('mode')
    if shuffle_mode is False or (isinstance(shuffle_mode, str) and shuffle_mode.lower() in ['f', 'false']):
        mode = False
    else:
        mode = True
    queue.shuffle(mode=mode)
    queue_service.save_queue(queue)
    release_queue_lock(queue.id)
    return jsonify(queue.to_jsonable())

@blueprint.route('/now', methods=['GET', 'POST'])
def now():
    # get current song
    err, queue = do_preamble(lock=True)
    if err is not None:
        return err
    release_queue_lock(queue.id)
    return jsonify(queue.now().to_jsonable())

@blueprint.route('/next', methods=['GET', 'POST'])
def next():
    # go to next song
    err, queue = do_preamble(lock=True)
    if err is not None:
        return err
    queue.next()
    queue_service.save_queue(queue)
    release_queue_lock(queue.id)
    queue_now = queue.now()
    if queue_now is None:
        return api_tools.error(404, "Queue has completed")
    return jsonify(queue_now.to_jsonable())

@blueprint.route('/previous', methods=['GET', 'POST'])
def previous():
    # return to last played song
    err, queue = do_preamble(lock=True)
    if err is not None:
        return err
    queue.previous()
    queue_service.save_queue(queue)
    release_queue_lock(queue.id)
    return jsonify(queue.now().to_jsonable())

@blueprint.route('/repeat', methods=['GET', 'POST'])
def repeat():
    err, queue = do_preamble(lock=True)
    if err is not None:
        return err
    # not implemented
    queue_service.save_queue(queue)
    release_queue_lock(queue.id)
    return jsonify(queue.to_jsonable())

@blueprint.route('/add', methods=['GET', 'POST'])
def add():
    err, queue = do_preamble(lock=True)
    if err is not None:
        return err
    sound_code = api_tools.get_param('sound-code')
    if sound_code is None:
        return api_tools.error(400, 'Missing sound code/id.')
    sound = sound_service.get_sound(codes.code2id(sound_code), create=False)
    if sound is None:
        return api_tools.error(404, 'Sound does not exist.')
    queue += sound
    queue_service.save_queue(queue)
    release_queue_lock(queue.id)
    return jsonify(queue.to_jsonable())


''' End of routes '''

def do_preamble(lock=True):
    id = get_queue_id()
    if id is None:
        return api_tools.error(400, 'Missing or invalid queue code/id.'), None
    create_param = api_tools.get_param('create')
    if lock is True:
        acquire_queue_lock(id)
    queue = queue_service.get_queue(id, create=False)
    if queue is None:
        if lock is True:
            release_queue_lock(id)
        return api_tools.error(404, 'Queue not found. To create a new queue, set create=true in your request (or omit the create parameter).'), None
    return None, queue

def get_queue_id():
    queue_code = api_tools.get_param('code')
    if queue_code is None:
        return
    return codes.code2id(queue_code)

def acquire_queue_lock(id):
    api_tools.start_single('queue-%s' % id)

def release_queue_lock(id):
    api_tools.end_single('queue-%s' % id)
