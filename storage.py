
from wal import WriteAheadLog
from sstable import SSTable


class KeyValueStore:

    def __init__(self, wal_filename="wal.log", sstable_filename="sstable.json"):
        self.memtable = {}
        self.flush_threshold = 3
        self.pending_writes = 0

        self.wal = WriteAheadLog(wal_filename)
        self.sstable = SSTable(sstable_filename)

        self.recover()

    def recover(self):
        self.memtable = self.sstable.read()
        records = self.wal.recover()

        for record in records:
            operation = record["operation"]
            key = record["key"]
            value = record.get("value")

            if operation == "PUT":
                self.memtable[key] = value

            elif operation == "DELETE":
                self.memtable.pop(key, None)

        self.pending_writes = len(records)

    def put(self, key, value):
        self.wal.append("PUT", key, value)
        self.memtable[key] = value

        self.pending_writes += 1

        if self.pending_writes >= self.flush_threshold:
            self.flush()

    def get(self, key):
        return self.memtable.get(key)

    def delete(self, key):
        self.wal.append("DELETE", key)
        self.memtable.pop(key, None)

        self.pending_writes += 1

        if self.pending_writes >= self.flush_threshold:
            self.flush()

    def flush(self):
        self.sstable.write(self.memtable)
        self.wal.clear()
        self.pending_writes = 0

        print("MemTable saved to disk!")
