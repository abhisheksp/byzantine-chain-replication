class Slot:
    def __init__(self, seed=0):
        self.value = seed

    def __next__(self):
        self.value += 1
        return self.value

    def reset(self):
        self.value = 0
