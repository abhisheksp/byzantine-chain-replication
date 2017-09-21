from configuration import Configuration


class Olympus:
    def __init__(self, config):
        self.config = config
        self.configuration = Configuration(config.config)
        pass
