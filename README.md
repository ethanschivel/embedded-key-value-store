# Embedded Key-Value Storage Engine

A small persistent key-value database written in Python. Supports string keys and JSON-serializable values, in-memory reads, write-ahead logging (WAL), automatic checkpoints, and recovery on restart.

## Quick start

Requires Python 3.9+; no third-party dependencies.

```python
from storage import KeyValueStore

db = KeyValueStore('wal.log', 'sstable.json', flush_threshold=3)
db.put('apple', 10)
print(db.get('apple'))  # 10
db.delete('apple')
print(db.get('apple'))  # None
```

## Architecture

1. `put` and `delete` append a JSON record to the WAL and fsync before modifying memory.
2. Reads use an in-memory dictionary.
3. Every `flush_threshold` changes, the engine writes a full JSON snapshot to a temporary file, fsyncs it, and atomically replaces the previous snapshot.
4. After snapshot replacement, the WAL is cleared.
5. On restart, the snapshot is loaded and remaining WAL entries are replayed.

## Test

```bash
python3 -m unittest -v test_storage.py
python3 benchmark.py
```

## Limitations

Educational single-process engine, not production-ready. Snapshots rewrite the entire database; it does not implement immutable sorted SSTables, compaction, concurrency control, multi-process locking, or transaction isolation. The WAL is JSON-lines and its recovery tolerates an incomplete final line, but the log is not protected by checksums or generations. Crash/power-loss behavior around snapshot replacement and WAL truncation has not been exhaustively fault-injection tested. Use only one writer, and do not store important data.
