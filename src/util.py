import json

import os


def persist_state(state, outfile):
    # TODO: refactor
    parent_dir = os.path.abspath(os.pardir)
    logs_dir = 'logs'
    full_path = os.path.join(parent_dir, logs_dir, outfile)
    with open(full_path, 'w+') as json_file:
        json.dump(state, json_file)
