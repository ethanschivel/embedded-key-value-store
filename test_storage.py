import os
import tempfile
import unittest
from storage import KeyValueStore


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.wal = os.path.join(self.tmp.name, 'wal.log')
        self.sst = os.path.join(self.tmp.name, 'sstable.json')

    def tearDown(self):
        self.tmp.cleanup()

    def store(self, threshold=3):
        return KeyValueStore(self.wal, self.sst, threshold)

    def test_put_get(self):
        db = self.store()
        db.put('apple', 10)
        self.assertEqual(db.get('apple'), 10)
        self.assertIsNone(db.get('missing'))

    def test_update(self):
        db = self.store()
        db.put('a', 1)
        db.put('a', 2)
        self.assertEqual(db.get('a'), 2)

    def test_delete(self):
        db = self.store()
        db.put('a', 1)
        db.delete('a')
        self.assertIsNone(db.get('a'))

    def test_recovery_before_flush(self):
        db = self.store()
        db.put('a', 1)
        self.assertEqual(self.store().get('a'), 1)

    def test_flush_after_three_changes(self):
        db = self.store()
        for i in range(3):
            db.put(str(i), i)
        self.assertEqual(db.pending_writes, 0)
        self.assertEqual(db.sstable.read(), {'0': 0, '1': 1, '2': 2})

    def test_restart_after_flush(self):
        db = self.store()
        for i in range(3):
            db.put(str(i), i)
        self.assertEqual(self.store().get('2'), 2)

    def test_delete_persists(self):
        db = self.store()
        db.put('a', 1)
        db.put('b', 2)
        db.put('c', 3)
        db.delete('b')
        self.assertIsNone(self.store().get('b'))

    def test_pending_counter(self):
        db = self.store()
        for i in range(5):
            db.put(str(i), i)
        self.assertEqual(db.pending_writes, 2)


if __name__ == '__main__':
    unittest.main()
