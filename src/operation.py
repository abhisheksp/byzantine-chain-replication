def new_put_operation(key, val):
    return {'operation': 'put', 'key': key, 'val': val}


def new_get_operation(key):
    return {'operation': 'get', 'key': key}


def new_append_operation(key, val):
    return {'operation': 'append', 'key': key, 'val': val}


def new_slice_operation(key, slice_):
    return {'operation': 'slice', 'key': key, 'slice': slice_}
