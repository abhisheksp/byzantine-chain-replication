import json
import os
import random
import string
import logging
import operation
import time
import nacl.signing
import nacl.exceptions


def persist_state(state, outfile):
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
    def between(s, start, end):
        p1 = s.find(start)
        p2 = s.find(end)
        return s[p1+1:p2]

    def parse_failure(split):
        if 'operation' in split:
            failure = 'change_operation'
        elif 'change_result' in split:
            failure = 'change_result'
        elif 'drop_result_stmt' in split:
            failure = 'drop_result_stmt'
        elif 'crash' in split:
            failure = 'crash'
        elif 'truncate_history' in split:
            failure = 'truncate_history'
        elif 'sleep' in split:
            failure = 'sleep'
        elif 'drop(' in split:
            failure = 'drop'
        elif 'increment_slot' in split:
            failure = 'increment_slot'
        elif 'extra_op' in split:
            failure = 'extra_op'
        elif 'invalid_order_sig' in split:
            failure = 'invalid_order_sig'
        elif 'invalid_result_sig' in split:
            failure = 'invalid_result_sig'
        elif 'drop_checkpt_stmts' in split:
            failure = 'drop_checkpt_stmts'
        else:
            failure = 'replace_me'
        return failure

    def parse_trigger(split):
        if split.startswith('client'):
            trigger_type = 'client_request'
        elif split.startswith('forwarded'):
            trigger_type = 'forwarded_request'
        elif split.startswith('shuttle'):
            trigger_type = 'shuttle'
        elif split.startswith('result_shuttle'):
            trigger_type = 'result_shuttle'
        elif split.startswith('wedge_request'):
            trigger_type = 'wedge_request'
        elif split.startswith('new_configuration'):
            trigger_type = 'new_configuration'
        elif split.startswith('checkpoint'):
            trigger_type = 'checkpoint'
        elif split.startswith('completed_checkpoint'):
            trigger_type = 'completed_checkpoint'
        elif split.startswith('get_running_state'):
            trigger_type = 'get_running_state'
        elif split.startswith('catch_up'):
            trigger_type = 'catch_up'
        else:
            trigger_type = 'UNKNOWN'
        return trigger_type

    def parse_trigger_failure(trigger_failure_split):
        if len(between(trigger_failure_split, '(', ')')) == 3:
            split = trigger_failure_split.split('),')
            c = int(split[0][-3]) + 1
            m = int(split[0][-1]) + 1
            trigger_type = parse_trigger(split[0])
            failure = parse_failure(split[1])
            failure_parameter = None
            if failure in ('truncate_history', 'sleep'):
                failure_parameter = int(between(split[1], '(', ')'))
            return c, m, trigger_type, failure, failure_parameter
        elif len(between(trigger_failure_split, '(', ')')) == 1:
            split = trigger_failure_split.split('),')
            m = int(split[0][-1]) + 1
            trigger_type = parse_trigger(split[0])
            failure = parse_failure(split[1])
            failure_parameter = None
            if failure in ('truncate_history', 'sleep'):
                failure_parameter = int(between(split[1], '(', ')'))
            return m, trigger_type, failure, failure_parameter

    replica_failures = {}
    for k, v in config.items():
        if k.startswith('failures'):
            configuration = int(k[k.find('[') + 1]) + 1
            replica = int(k[k.find(']') - 1]) + 1
            failures = {}
            for trigger_failure in v.split('; '):
                failure = parse_trigger_failure(trigger_failure)
                if len(failure) == 5:
                    c, m, trigger_type, failure, failure_param = parse_trigger_failure(trigger_failure)
                    failures[(c, m, trigger_type, failure)] = failure_param
                else:
                    m, trigger_type, failure, failure_param = parse_trigger_failure(trigger_failure)
                    failures[(m, trigger_type, failure)] = failure_param
            replica_failures[(configuration, replica)] = failures
    return replica_failures


def change_operation():
    return operation.new_get_operation('x')


def change_result():
    return 'OK'


def drop_result_stmt(result_proof):
    result_proof['result_statements'] = result_proof['result_statements'][1:]
    return result_proof


def testfailure():
    return "TEST COMPLETE"


def crash():
    logging.shutdown()
    os._exit(-1)


def sleep():
    time.sleep(6)


def drop(request):
    if request == 'checkpoint':
        return 'ignore_messages'
    elif request == 'completed_checkpoint':
        return 'ignore_messages'


def extra_op(cur_running_state):
    extra_operation = {'operation': 'put', 'key': 'a', 'val': 'a'}
    return operation.apply_operation(cur_running_state, extra_operation)


def invalid_order_sig():
    pass


def generate_fake_key():
    sign_key = nacl.signing.SigningKey.generate()
    return sign_key


def truncate_history(history):
    return history[:-1]
