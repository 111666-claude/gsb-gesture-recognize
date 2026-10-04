import unittest

from gesture.core import Gesture


class GestureTest(unittest.TestCase):
    def test_empty_recognize(self):
        self.assertEqual(Gesture(300, 5, 1).recognize(0), [])

    def test_horizontal_swipe_is_right(self):
        book = Gesture(300, 5, 10)
        book.down("e1", 0, 0, 0)
        book.move("e2", 20, 0, 100)
        book.up("e3", 100)
        self.assertEqual(book.recognize(100), ["right"])

    def test_short_swipe_is_none(self):
        book = Gesture(300, 5, 10)
        book.down("e1", 0, 0, 0)
        book.move("e2", 1, 0, 100)
        book.up("e3", 100)
        self.assertEqual(book.recognize(100), [])

    def test_counters_start_at_zero(self):
        book = Gesture(300, 5, 1)
        self.assertEqual(book.scanned_count(), 0)
        self.assertEqual(book.dropped_count(), 0)


if __name__ == "__main__":
    unittest.main()
