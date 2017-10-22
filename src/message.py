import uuid
import nacl
import nacl.hash
import nacl.encoding
from collections import namedtuple


class Message:
    client_request_tag = 'request'
    client_retransmission_tag = 'retransmission'
    replica_response_tag = 'response'
    reconfiguration_tag = 'reconfiguration_request'
    request_shuttle_tag = 'request_shuttle'
    result_shuttle_tag = 'result_shuttle'
    OrderStatement = namedtuple('OrderStatement', 'slot operation replica_id')
    OrderProof = namedtuple(
        'OrderProof',
        'client_id request_id slot operation configuration order_statements'
    )
    ResultStatement = namedtuple('OrderStatement', 'result operation replica_id')
    ResultProof = namedtuple(
        'ResultProof',
        'client_id request_id result operation configuration result_statements'
    )
    RequestShuttle = namedtuple('RequestShuttle', 'order_proof result_proof')
    ResultShuttle = namedtuple('ResponseShuttle', 'result result_proof')

    def __init__(self, identifier):
        self.identifier = identifier

    def new_request(self, payload):
        request_id = uuid.uuid4()
        message_body = {'client_id': self.identifier, 'request_id': request_id, 'payload': payload}
        return self.client_request_tag, message_body

    def new_retransmission_request(self, old_request_id, payload):
        message_body = {'client_id': self.identifier, 'request_id': old_request_id, 'payload': payload}
        return self.client_retransmission_tag, message_body

    def new_reconfiguration_request(self, type_, payload):
        message_body = {'id': self.identifier, 'type': type_, 'payload': payload}
        return self.reconfiguration_tag, message_body

    def new_response(self, payload):
        message_body = {'replica_id': self.identifier, 'payload': payload}
        return self.replica_response_tag, message_body

    def new_request_shuttle(self, payload):
        message_body = {'replica_id': self.identifier, 'payload': payload}
        return self.request_shuttle_tag, message_body

    def new_result_shuttle(self, payload):
        message_body = {'replica_id': self.identifier, 'payload': payload}
        return self.result_shuttle_tag, message_body

    def new_order_statement(self, operation, slot):
        order_statement = {
            'slot': slot,
            'operation': operation,
            'replica_id': self.identifier
        }
        return order_statement

    def new_order_proof(self, previous_order_proof, new_order_statement):
        order_statements = previous_order_proof.order_statements + [new_order_statement]

        # TODO: figure out serializing named tuple
        order_proof = {
            'client_id': previous_order_proof.client_id,
            'request_id': previous_order_proof.request_id,
            'slot': previous_order_proof.slot,
            'operation': previous_order_proof.operation,
            'configuration': 'DEFAULT',
            'order_statements': order_statements
        }
        return order_proof

    def new_result_statement(self, operation, result):
        hashed_result = nacl.hash.sha256(bytes(result, 'utf-8'), encoder=nacl.encoding.HexEncoder)
        result_statement = {
            'result': hashed_result,
            'operation': operation,
            'replica_id': self.identifier
        }
        return result_statement

    def new_result_proof(self, previous_result_proof, new_result_statement):
        result_statements = previous_result_proof.result_statements + [new_result_statement]

        # TODO: figure out serializing named tuple
        result_proof = {
            'client_id': previous_result_proof.client_id,
            'request_id': previous_result_proof.request_id,
            'result': previous_result_proof.result,
            'operation': previous_result_proof.operation,
            'configuration': 'DEFAULT',
            'result_statements': result_statements
        }
        return result_proof