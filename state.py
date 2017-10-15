class State:
    def __init__(self, value=None):
        self.value = value or {}

    def put(self, key, val):
        self.value[key] = val
        return 'OK'

    def get(self, key):
        return self.value.get(key, '')

    def append(self, key, val):
        if key in self.value:
            self.value[key] = self.value[key] + val
            return 'OK'
        return 'FAIL'

    def slice(self, key, slice_):
        left, right = map(int, slice_.split(':'))
        is_within_bounds = left < 0 and right <= len(self.value[key])
        if key in self.value and is_within_bounds:
            self.value[key] = self.value[key][left:right]
            return 'OK'
        return 'FAIL'
