import json
import os
import tempfile


class SSTable:
    def __init__(self, filename='sstable.json'):
        self.filename = filename

    def read(self):
        if not os.path.exists(self.filename):
            return {}
        with open(self.filename, encoding='utf-8') as file:
            data = json.load(file)
        if not isinstance(data, dict):
            raise ValueError('SSTable must contain a JSON object')
        return data

    def write(self, data):
        directory = os.path.dirname(os.path.abspath(self.filename))
        path = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=directory, delete=False) as file:
                path = file.name
                json.dump(data, file, allow_nan=False)
                file.flush()
                os.fsync(file.fileno())
            os.replace(path, self.filename)
            # Persist directory metadata on Unix-like systems.
            if hasattr(os, 'O_DIRECTORY'):
                fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY)
                try:
                    os.fsync(fd)
                finally:
                    os.close(fd)
        finally:
            if path and os.path.exists(path):
                os.unlink(path)
