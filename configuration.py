from replica import Replica
from head import Head
from tail import Tail


class Configuration:
    def __init__(self, config):
        self.replica_count = config.replica_count
        self.head = Head(config.init_object)
        self.tail = Tail(config.init_object)
        # create inner_replicas with chains
        inner_replicas = [Replica(config.init_object) * self.replica_count]
        self.replicas = [head] + inner_replicas + [tail]
        pass

    def get_head(self):
        return self.head

    def get_tail(self):
        return self.tail

    def broadcast_request(self, request):
        client, operation = request
        map(lambda replica: send((client, operation), to=replica), self.replicas)
