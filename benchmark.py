import os
import tempfile
import time
from storage import KeyValueStore

COUNT = 1000
with tempfile.TemporaryDirectory() as directory:
    db = KeyValueStore(os.path.join(directory, 'wal.log'), os.path.join(directory, 'sstable.json'), flush_threshold=100)
    start = time.perf_counter()
    for i in range(COUNT):
        db.put(f'key-{i}', i)
    write_time = time.perf_counter() - start
    start = time.perf_counter()
    for i in range(COUNT):
        assert db.get(f'key-{i}') == i
    read_time = time.perf_counter() - start
    print(f'Writes: {COUNT / write_time:,.0f} ops/sec')
    print(f'Reads:  {COUNT / read_time:,.0f} ops/sec')
