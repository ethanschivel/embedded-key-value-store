
import json
import os


class SSTable:

    def __init__(self, filename="sstable.json"):
        self.filename = filename

    def write(self, data):
        sorted_data = dict(sorted(data.items()))

        with open(self.filename, "w") as file:
            json.dump(sorted_data, file)

    def read(self):
        if not os.path.exists(self.filename):
            return {}

        with open(self.filename, "r") as file:
            return json.load(file)
