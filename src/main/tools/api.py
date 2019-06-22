'''
API-related functions in one spot for convenience

Created by NGnius 2019-06-15
'''

from flask import jsonify, request
from threading import Semaphore, RLock

def get_param(param, silent=False):
    if request.method == 'GET':
        return request.args.get(param)
    else:
        try:
            return request.get_json(force=True, silent=silent)[param]
        except KeyError:
            return None

def error(status=500, reason=None):
    error_response = {'status':status}
    if reason is not None:
        error_response['reason'] = reason
    return jsonify(error_response), status

single_semaphores = dict()
resource_lock = RLock()
def start_single(identifier):
    resource_lock.acquire()
    if identifier not in single_semaphores:
        resource_lock.release()
        single_semaphores[identifier] = Semaphore(1)
    else:
        resource_lock.release()
        single_semaphores[identifier].acquire()

def end_single(identifier):
    resource_lock.acquire()
    single_semaphores[identifier].release()
