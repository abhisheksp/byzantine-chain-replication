import json

import os


def persist_state(state, outfile):
    full_path = os.path.join(os.path.abspath(os.curdir) + '/logs/', outfile)
    # full_path = os.path.join('../logs/', outfile)
    with open(full_path, 'w+') as json_file:
        json.dump(state, json_file)
