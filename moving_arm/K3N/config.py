import json
import os

class Config:
    DEFAULT_PATH = "config.json"

    def __init__(self, path: str = None):
        self.path = path or self.DEFAULT_PATH
        self.data = {}

    def load(self):
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"Config file not found: {self.path}")

        with open(self.path, "r") as f:
            self.data = json.load(f)

    def get(self, key, default=None):
        return self.data.get(key, default)