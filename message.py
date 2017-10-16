import uuid


class Message:
    client_request = 'request'
    replica_response = 'response'
    request_shuttle = 'request_shuttle'

    def __init__(self, identifier):
        self.identifier = identifier

    def new_request(self, payload):
        request_id = uuid.uuid4()
        # TODO: make id explicit
        message_body = {'id': self.identifier, 'request_id': request_id, 'payload': payload}
        return self.client_request, message_body

    def new_response(self, payload):
        message_body = {'id': self.identifier, 'payload': payload}  # TODO: make id explicit
        return self.replica_response, message_body

    def new_request_shuttle(self, payload):
        message_body = {'replica_id': self.identifier, 'payload': payload}
        return self.request_shuttle, message_body

    def new_order_statement(self, operation, slot=None):
        slot = slot if slot else uuid.uuid4()
        order_statement = {
            'slot': slot,
            'operation': operation,
            'replica_id': self.identifier
        }
        return order_statement

    def new_order_proof(self, client_id, request_id, slot, operation, configuration, new_order_statement,
                        old_order_statements):
        order_statements = old_order_statements + [new_order_statement]

        # TODO: figure out serializing named tuple
        order_proof = {
            'client_id': client_id,
            'request_id': request_id,
            'slot': slot,
            'operation': operation,
            'configuration': configuration,
            'order_statements': order_statements
        }
        return order_proof
