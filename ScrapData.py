class ScrapData:

    id = None
    url = None
    description = None
    expert_estimate = None
    current_bid = None
    picture = None
    winning_bid = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
