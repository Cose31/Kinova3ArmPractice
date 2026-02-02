from logging import Logging
from commander.location import Location

class ComputerVisionModule:

    def detectTag(self) -> Location:
        Logging.logInfo("Detecting tag...")
        return Location(0, 0, 0)

    def scanAprilTag(self, location: Location):
        Logging.logInfo(f"Scanning AprilTag at {location}")

    def storeLocationData(self) -> Location:
        Logging.logInfo("Storing location data")
        return Location(0, 0, 0)

    def saveCurrentPose(self) -> Location:
        Logging.logInfo("Saving pose")
        return Location(0, 0, 0)

    def calibrateCamera(self):
        Logging.logInfo("Calibrating camera...")