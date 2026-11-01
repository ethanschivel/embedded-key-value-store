import os
from wal import WriteAheadLog
from sstable import SSTable


class KeyValueStore:
    def __init__(self, wal_filename='wal.log', sstable_filename='sstable.json', flush_threshold=3):
        if flush_threshold < 1:
            raise ValueError('flush_threshold must be positive')
        self.flush_threshold = flush_threshold
        self.wal = WriteAheadLog(wal_filename)
        self.sstable = SSTable(sstable_filename)
        self.memtable = self.sstable.read()
        records = self.wal.recover()
        for record in records:
            if record['operation'] == 'PUT':
                self.memtable[record['key']] = record['value']
            elif record['operation'] == 'DELETE':
                self.memtable.pop(record['key'], None)
        self.pending_writes = len(records)

    def put(self, key, value):
        self.wal.append('PUT', key, value)
        self.memtable[key] = value
        self._changed()

    def get(self, key):
        return self.memtable.get(key)

    def delete(self, key):
        self.wal.append('DELETE', key)
        self.memtable.pop(key, None)
        self._changed()

    def _changed(self):
        self.pending_writes += 1
        if self.pending_writes >= self.flush_threshold:
            self.flush()

    def flush(self):
        self.sstable.write(self.memtable)
        self.wal.clear()
        self.pending_writes = 0
