from commander.location import Location
from commander.vectors import Vectors

class ActionFrame:
    def __init__(self, location: Location, vector: Vectors, action: int):
        self.location = location
        self.vector = vector
        self.action = action
    
    