from config import Config
from commander.commander import CommanderGUI
from comslogic.coms_logic import ComsLogic2K3N
from logging import Logging

def main():

    Logging.logInfo("Application starting")

    config = Config()
    config.load()

    commander = CommanderGUI()
    Logging.logInfo("Commander initialized")

    coms = ComsLogic2K3N()
    Logging.logInfo("Communication initialized")
    
    # Doing future things here

    # Placeholder for next actions...
    Logging.logInfo("Application exiting")

if __name__ == "__main__":
    main()