class ScrapData:

    id = None
    url = None
    description = None
    expert_estimate = None
    current_bid = None
    image_location = None
    winning_bid = None

    #for wine categories
    lot_details = None
    mixed_lot = None
    type = None
    vintage = None
    producer = None
    num_of_bottles = None
    bottle_size = None
    country = None



    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
