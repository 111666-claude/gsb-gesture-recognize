import unittest

from gesture.core import Gesture


class GestureTest(unittest.TestCase):
    def test_single_point_has_no_direction(self):
        book = Gesture(300, 5)
        book.push("e1", 0, 0, 0)
        self.assertIsNone(book.recognize(0))

    def test_horizontal_swipe_is_right(self):
        book = Gesture(300, 5)
        book.push("e1", 0, 0, 0)
        book.push("e2", 20, 0, 100)
        self.assertEqual(book.recognize(100), "right")

    def test_short_swipe_is_none(self):
        book = Gesture(300, 5)
        book.push("e1", 0, 0, 0)
        book.push("e2", 1, 0, 100)
        self.assertIsNone(book.recognize(100))

    def test_scanned_starts_at_zero(self):
        self.assertEqual(Gesture(300, 5).scanned_count(), 0)


if __name__ == "__main__":
    unittest.main()
