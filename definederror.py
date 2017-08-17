
class definederror(Exception):
    def __init__(self, why):
        self.reason = why

    def __str__(self):
        return self.reason
