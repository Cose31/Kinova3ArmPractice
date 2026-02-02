class Location:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def replaceCoord(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z