class Vectors:
    def __init__(self, xTheta: float, yTheta: float, zTheta: float):
        self.xTheta = xTheta
        self.yTheta = yTheta
        self.zTheta = zTheta

    def replace(self, x, y, z):
        self.xTheta = x
        self.yTheta = y
        self.zTheta = z