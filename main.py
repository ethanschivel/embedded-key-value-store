
from storage import KeyValueStore

store = KeyValueStore()

store.put("name", "Ethan")
store.put("language", "Python")

print("Before flush:", store.memtable)

store.flush()

print("After flush:", store.sstable.read())
