## transaction class with memebers payer, points and timestamp

class Transaction(object):
    def __init__(self, payer, points, timestamp):
        self.payer = payer
        self.points = points
        self.timestamp = timestamp
    