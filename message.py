import uuid


class Message:
    client_request = 'request'
    replica_response = 'response'

    def __init__(self, identifier):
        self.identifier = identifier

    def new_request(self, payload):
        request_id = uuid.uuid4()
        message_body = {'id': self.identifier, 'request_id': request_id, 'payload': payload}
        return self.client_request, message_body

    def new_response(self, payload):
        message_body = {'id': self.identifier, 'payload': payload}
        return self.replica_response, message_body
