def read_configuration(filepath):
    config = {}
    with open(filepath, 'r') as f:
        for line in f:
            if line[0] != '#':
                (key, sep, val) = line.partition('=')
                # if the line does not contain '=', it is invalid and hence ignored
                if len(sep) != 0:
                    val = val.strip()
                    config[key.strip()] = int(val) if str.isdecimal(val) else val
    return config
