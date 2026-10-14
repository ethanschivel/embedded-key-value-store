
# Embedded Key-Value Storage Engine

A Python-based embedded key-value storage engine built from scratch to explore database internals and LSM-tree architecture.

## Current Features

- In-memory key-value storage using a MemTable
- PUT, GET, and DELETE operations
- Write-Ahead Log (WAL) for recording changes
- Data recovery from the WAL after restarting
- Sorted key-value storage using JSON files
- Manual MemTable flushing to disk

## Technologies

- Python
- JSON
- File I/O

## Run

```bash
python3 main.py
```

## Project Status

Work in progress.

Planned improvements:
- Multiple immutable SSTables
- Automatic MemTable flushing
- Tombstones for deleted keys
- WAL checkpointing
- Background compaction
- Automated tests and performance benchmarks
