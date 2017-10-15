import uuid


class Request:
    client_request = 'request'

    def __init__(self, client_id):
        self.client_id = client_id

    def new_request(self, payload):
        request_id = uuid.uuid4()
        message_body = {'client_id': self.client_id, 'request_id': request_id, 'payload': payload}
        return self.client_request, message_body
