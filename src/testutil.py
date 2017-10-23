import json
import os
import random
import string

import operation


def persist_state(state, outfile):
    # TODO: refactor
    parent_dir = os.path.abspath(os.pardir)
    logs_dir = 'logs'
    full_path = os.path.join(parent_dir, logs_dir, outfile)
    with open(full_path, 'w+') as json_file:
        json.dump(state, json_file)


def parse_client_workloads(config):
    def parse_operation(raw_operation):
        if raw_operation.startswith('put'):
            key, value = map(lambda x: x.strip('\''), raw_operation[5:-1].split(','))
            return operation.new_put_operation(key, value)
        elif raw_operation.startswith('get'):
            key = raw_operation[5:-1].strip('\'')
            return operation.new_get_operation(key)
        elif raw_operation.startswith('append'):
            key, value = map(lambda x: x.strip('\''), raw_operation[7:-1].split(','))
            return operation.new_append_operation(key, value)
        elif raw_operation.startswith('slice'):
            key, value = map(lambda x: x.strip('\''), raw_operation[6:-1].split(','))
            return operation.new_slice_operation(key, value)

    def generate_operations(seed, count):
        random.seed(seed)
        operations = []
        previous_keys = []
        for _ in range(count):
            op = random.randint(1, 4)
            length = random.randint(0, 100)
            rand_key = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
            rand_value = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
            previous_keys.append(rand_key)
            rand_prev_key = random.choice(previous_keys)
            rand_slice = str(random.randint(0, 10)) + ':' + str(random.randint(0, 10))
            if op == 1:
                operations.append(operation.new_put_operation(rand_key, rand_value))
            elif op == 2:
                operations.append(operation.new_get_operation(rand_prev_key))
            elif op == 3:
                operations.append(operation.new_append_operation(rand_key, rand_value))
            else:
                operations.append(operation.new_slice_operation(rand_key, rand_slice))
        return operations

    client_workload = {}
    for k, v in config.items():
        if k.startswith('workload'):
            client_id = int(k[k.find('[') + 1]) + 1
            if not v.startswith('pseudorandom'):
                raw_operations = v.split('; ')
                workload = list(map(parse_operation, raw_operations))
            else:
                seed, n = map(int, v[v.find('(') + 1:-1].split(','))
                workload = generate_operations(seed, n)
            client_workload[client_id] = workload
    return client_workload


def parse_failure_scenarios(config):
    def parse_trigger_failure(trigger_failure_split):
        split = trigger_failure_split.split('),')
        c = int(split[0][-3]) + 1
        m = int(split[0][-1]) + 1
        if split[0].startswith('client'):
            trigger_type = 'client_request'
        elif split[0].startswith('forwarded'):
            trigger_type = 'forwarded_request'
        elif split[0].startswith('shuttle'):
            trigger_type = 'shuttle'
        elif split[0].startswith('result_shuttle'):
            trigger_type = 'result_shuttle'

        if 'operation' in split[1]:
            failure = 'change_operation'
        elif 'change_result' in split[1]:
            failure = 'change_result'
        else:
            failure = 'drop_result_stmt'
        return c, m, trigger_type, failure

    replica_failures = {}
    for k, v in config.items():
        if k.startswith('failures'):
            configuration = int(k[k.find('[') + 1])
            replica = int(k[k.find(']') - 1]) + 1
            failures = set()
            for trigger_failure in v.split('; '):
                c, m, trigger_type, failure = parse_trigger_failure(trigger_failure)
                failures.add((c, m, trigger_type, failure))
            replica_failures[(configuration, replica)] = failures
    return replica_failures


def change_operation():
    return operation.new_get_operation('x')


def change_result():
    return 'OK'


def drop_result_stmt(result_proof):
    result_proof['result_statements'] = result_proof['result_statements'][1:]
    return result_proof
