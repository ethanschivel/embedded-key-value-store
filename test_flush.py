from storage import KeyValueStore

store = KeyValueStore(
    wal_filename="test_wal.log",
    sstable_filename="test_sstable.json"
)

store.put("apple", 10)
store.put("banana", 20)
store.put("cherry", 30)

store.put("banana", 20)
store.put("cherry", 30)

print("MemTable:", store.memtable)
print("Saved to disk:", store.sstable.read())

print("MemTable:", store.memtable)
print("Saved to disk:", store.sstable.read())