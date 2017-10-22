import uuid
from collections import namedtuple


class Request:
    def __init__(self, client_id, operation):
        # generate unique id for each request
        self.id = uuid.uuid4()

        self.client = client_id
        self.operation = operation


RequestShuttle = namedtuple('RequestShuttle', ['request', 'order_proof'])
Shuttle = namedtuple('Shuttle', ['request', 'order_proof', 'result_proof'])
ResultShuttle = namedtuple('ResultShuttle', ['request', 'result_proof'])
ErrorShuttle = namedtuple('ErrorShuttle', ['request', 'error'])
OrderStatement = namedtuple('OrderStatement', ['request', 'slot', 'operation'])
WedgeStatement = namedtuple('WedgeStatement', ['running_state', 'history', 'checkpoint','replica_id'])
WedgeRequest = namedtuple('WedgeRequest', [])
ReconfigureRequest = namedtuple('ReconfigureRequest', [])
CatchUpRequest = namedtuple('CatchupRequest', [])
ResultStatement = namedtuple('ResultStatement', ['request', 'slot', 'operation'])
Quorum = namedtuple('Quorum', ['initial_running_state','history'])

OrderProof = namedtuple('OrderProof', [
    'request', 'slot',
    'operation', 'configuration',
    'order_statements'])

ResultProof = namedtuple('ResultProof', [
    'request', 'slot',
    'operation', 'configuration',
    'result_statements'])

