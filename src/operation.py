def new_put_operation(key, val):
    return {'operation': 'put', 'key': key, 'val': val}


def new_get_operation(key):
    return {'operation': 'get', 'key': key}


def new_append_operation(key, val):
    return {'operation': 'append', 'key': key, 'val': val}


def new_slice_operation(key, slice_):
    return {'operation': 'slice', 'key': key, 'slice': slice_}


def apply_operation(state, payload):
    operation = payload['operation']
    if operation == 'put':
        return state.put(payload['key'], payload['val'])
    elif operation == 'get':
        return state.get(payload['key'])
    elif operation == 'append':
        return state.append(payload['key'], payload['val'])
    elif operation == 'slice':
        return state.slice(payload['key'], payload['slice'])
