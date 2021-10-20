class Entry():

    # Class initializer. It has 5 custom parameters, with the
    # special `self` parameter that every method on a class
    # needs as the first parameter.
    def __init__(self, id, concept, entry, moodId, date, tags=[]):
        self.id = id
        self.concept = concept
        self.entry = entry
        self.moodId = moodId
        self.date = date
        self.mood = None
        self.tags = tags