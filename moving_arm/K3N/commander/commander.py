from logging import Logging

class CommanderGUI:

    def __init__(self):
        self.currentPosition = []  # list of [Vector, Location]

    def displayLogs(self):
        """ Will be used to display/stream logs from the text file that is collecting the logs"""
        return

    def acceptCommand(self, cmd: str) -> str:
        """ Will be used to take in a command from the GUI """
        Logging.logInfo(f"Command accepted: {cmd}")
        return cmd

    def dispatchLog(self):
        # Could be scrapped from final design - will be used to call specific logError, logWarn or logInfo
        return