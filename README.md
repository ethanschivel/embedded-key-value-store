# Embedded Key-Value Storage Engine

A lightweight, persistent key-value storage engine built from scratch in Python.

This project explores fundamental database concepts, including write-ahead logging (WAL), in-memory indexing, disk persistence, automatic checkpointing, and crash recovery.

## Features

- **Key-Value Operations:** Insert, retrieve, update, and delete records.
- **In-Memory Storage:** Fast lookups using Python dictionaries.
- **Write-Ahead Logging:** Records changes before updating in-memory data.
- **Persistent Storage:** Saves database snapshots to disk using JSON.
- **Automatic Checkpointing:** Flushes data after a configurable number of changes.
- **Crash Recovery:** Reconstructs database state using snapshots and WAL records.
- **Automated Testing:** Unit tests covering CRUD operations, persistence, flushing, and recovery.
- **Performance Benchmarking:** Measures read and write throughput.

## Technologies

- Python 3.9+
- Python Standard Library
- JSON
- File I/O
- Git and GitHub
- unittest

No third-party dependencies required.

## Getting Started

Clone the repository:

```bash
git clone https://github.com/ethanschivel/embedded-key-value-store.git
cd embedded-key-value-store
```

Run Python:

```python
from storage import KeyValueStore

db = KeyValueStore(
    "wal.log",
    "sstable.json",
    flush_threshold=3
)

db.put("apple", 10)
db.put("banana", 20)

print(db.get("apple"))  # 10

db.put("apple", 50)
print(db.get("apple"))  # 50

db.delete("banana")
print(db.get("banana"))  # None
```

## How It Works

1. **Write:** PUT and DELETE operations are recorded in the WAL before the in-memory dictionary is updated.
2. **Read:** GET operations retrieve values directly from memory.
3. **Checkpoint:** After the configured number of changes, the engine writes a complete JSON snapshot to disk.
4. **Recovery:** When restarted, the engine loads the saved snapshot and replays remaining WAL records.

The current implementation uses JSON snapshots rather than immutable sorted SSTables.

## Testing

Run automated unit tests:

```bash
python3 -m unittest test_storage -v
```

The current test suite includes eight tests covering basic operations, updates, deletions, flushing, and restart recovery.

## Performance Benchmarks

Example results measured on a MacBook Air:

| Operation | Throughput |
|---|---:|
| Writes | 8,470 operations/second |
| Reads | 3,357,576 operations/second |

Run the benchmark:

```bash
python3 benchmark.py
```

Results depend on hardware, workload, storage conditions, and benchmark configuration. These figures are not directly comparable to production database benchmarks.

## Project Structure

```text
embedded-key-value-store/
├── main.py
├── storage.py
├── wal.py
├── sstable.py
├── test_flush.py
├── test_storage.py
├── benchmark.py
└── README.md
```

## Limitations

This is an educational, single-process storage engine rather than a production database.

- Full JSON snapshots are rewritten during checkpointing.
- No immutable sorted SSTables or compaction.
- No transaction isolation or multi-process locking.
- No concurrent writer support.
- WAL records do not use checksums or generation identifiers.
- Crash and power-loss scenarios have not been exhaustively tested.

The project is intended for learning database internals and systems programming, not storing important production data.

## Future Improvements

Potential extensions include immutable SSTables, compaction, concurrency support, stronger crash-recovery guarantees, and additional performance testing.
