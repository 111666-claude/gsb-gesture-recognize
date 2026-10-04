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

    def test_span_over_max_ms_is_void(self):
        book = Gesture(300, 5, 10)
        book.down("e1", 0, 0, 0)
        book.move("e2", 100, 0, 1000)
        book.up("e3", 1000)
        self.assertEqual(book.recognize(1000), [])

    def test_span_at_max_ms_is_kept(self):
        book = Gesture(300, 5, 10)
        book.down("e1", 0, 0, 0)
        book.move("e2", 100, 0, 300)
        book.up("e3", 300)
        self.assertEqual(book.recognize(300), ["right"])

    def test_tie_direction_is_horizontal(self):
        book = Gesture(300, 5, 10)
        book.down("e1", 0, 0, 0)
        book.move("e2", 10, 10, 100)
        book.up("e3", 100)
        self.assertEqual(book.recognize(100), ["right"])

    def test_duplicate_down_does_not_reset_segment(self):
        book = Gesture(300, 5, 10)
        book.down("e1", 0, 0, 0)
        book.down("e1", 100, 0, 10)
        book.move("e2", 100, 0, 20)
        book.up("e3", 20)
        self.assertEqual(book.recognize(20), ["right"])
        self.assertEqual(book.recognize(20), [])

    def test_unclosed_segment_never_produced(self):
        book = Gesture(300, 5, 10)
        book.down("e1", 0, 0, 0)
        book.move("e2", 100, 0, 100)
        self.assertEqual(book.recognize(200), [])

    def test_budget_per_second_drops_overflow(self):
        book = Gesture(300, 5, 1)
        book.down("e1", 0, 0, 0)
        book.move("e2", 100, 0, 50)
        book.up("e3", 50)
        book.down("e4", 0, 0, 100)
        book.move("e5", 100, 0, 150)
        book.up("e6", 150)
        self.assertEqual(book.recognize(150), ["right"])
        self.assertEqual(book.dropped_count(), 1)

    def test_budget_is_per_second(self):
        book = Gesture(300, 5, 1)
        book.down("e1", 0, 0, 0)
        book.move("e2", 100, 0, 50)
        book.up("e3", 50)
        book.down("e4", 0, 0, 1000)
        book.move("e5", 100, 0, 1050)
        book.up("e6", 1050)
        self.assertEqual(book.recognize(1050), ["right", "right"])
        self.assertEqual(book.dropped_count(), 0)

    def test_recognize_scans_only_newly_finished(self):
        book = Gesture(300, 5, 1000000)
        for index in range(1000):
            tag = "g-%d" % index
            book.down(tag + "-down", 0, 0, index * 10)
            book.move(tag + "-move", 100, 0, index * 10 + 5)
            book.up(tag + "-up", index * 10 + 5)
        for _ in range(3000):
            book.recognize(5000)
        self.assertLessEqual(book.scanned_count(), 6000)


if __name__ == "__main__":
    unittest.main()
