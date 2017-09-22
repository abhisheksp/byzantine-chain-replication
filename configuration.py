from replica import Replica


class Configuration:
    def __init__(self, config):
        self.replica_count = config.replica_count   # minimum 3
        # TODO: init_replica with chains
        self.replicas = [Replica(config.init_object) * self.replica_count]
        self.head = self.replicas[0]
        self.tail = self.replicas[-1]
        pass

    def get_head(self):
        return self.head   # TODO: verification?

    def get_tail(self):
        return self.tail   # TODO: verification?

    def broadcast_request(self, request):
        client, operation = request
        map(lambda x: x.send(client, operation), self.replicas)
