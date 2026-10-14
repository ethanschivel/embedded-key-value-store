
import json


class WriteAheadLog:

    def __init__(self, filename="wal.log"):
        self.filename = filename

    def append(self, operation, key, value=None):
        record = {
            "operation": operation,
            "key": key,
            "value": value
        }

        with open(self.filename, "a") as file:
            file.write(json.dumps(record) + "\n")
            file.flush()

    def recover(self):
        records = []

        try:
            with open(self.filename, "r") as file:
                for line in file:
                    record = json.loads(line)
                    records.append(record)

        except FileNotFoundError:
            pass

        return records
