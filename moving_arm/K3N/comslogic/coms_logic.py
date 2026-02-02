from logging import Logging

class ComsLogic2K3N:
    
    def __init__(self):
        # Flags are the only members as of now - will flesh this out once we decide what flags are necessary
        self.engageState = False
        self.powerState = False
        self.flag3 = False

    def sendCommand(self, param) -> str:
        Logging.logInfo(f"Sending command: {param}")
        return "OK"

    def getTelemetryData(self):
        Logging.logInfo("Fetching telemetry data")

    def parseLogs(self):
        return
    
    def parseFlags(self):
        return

    def dispatchLog(self):
        return