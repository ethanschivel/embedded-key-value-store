import json
import os


class WriteAheadLog:
    def __init__(self, filename='wal.log'):
        self.filename = filename

    def append(self, operation, key, value=None):
        record = {'operation': operation, 'key': key, 'value': value}
        line = json.dumps(record, allow_nan=False) + '\n'
        with open(self.filename, 'a', encoding='utf-8') as file:
            file.write(line)
            file.flush()
            os.fsync(file.fileno())

    def recover(self):
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, encoding='utf-8') as file:
            lines = file.readlines()
        records = []
        for index, line in enumerate(lines):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
                if record.get('operation') not in ('PUT', 'DELETE') or not isinstance(record.get('key'), str):
                    raise ValueError('Invalid WAL record')
                records.append(record)
            except (json.JSONDecodeError, ValueError) as exc:
                if index == len(lines) - 1 and not line.endswith('\n'):
                    break  # incomplete final record after a crash
                raise ValueError(f'Corrupt WAL record on line {index + 1}') from exc
        return records

    def clear(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            file.flush()
            os.fsync(file.fileno())
