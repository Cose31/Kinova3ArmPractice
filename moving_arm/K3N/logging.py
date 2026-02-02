from datetime import datetime

class Logging:

    @staticmethod
    def _write(level: str, message: str):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{ts}] [{level}] {message}")

    @staticmethod
    def logInfo(message: str):
        Logging._write("INFO", message)

    @staticmethod
    def logWarning(message: str):
        Logging._write("WARN", message)

    @staticmethod
    def logError(message: str):
        Logging._write("ERROR", message)