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

    def test_tie_direction_is_horizontal(self):
        book = Gesture(300, 5, 10)
        book.down("e1", 0, 0, 0)
        book.move("e2", 10, 10, 100)
        book.up("e3", 100)
        self.assertEqual(book.recognize(100), ["right"])

    def test_vertical_swipe_when_dy_dominant(self):
        book = Gesture(300, 5, 10)
        book.down("e1", 0, 0, 0)
        book.move("e2", 3, 10, 100)
        book.up("e3", 100)
        self.assertEqual(book.recognize(100), ["up"])

    def test_duplicate_down_does_not_reset_segment(self):
        book = Gesture(300, 5, 10)
        book.down("e1", 0, 0, 0)
        book.down("e1", 100, 0, 10)
        book.move("e2", 100, 0, 20)
        book.up("e3", 20)
        self.assertEqual(book.recognize(20), ["right"])

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

    def test_budget_resets_next_second(self):
        book = Gesture(300, 5, 1)
        book.down("e1", 0, 0, 0)
        book.move("e2", 100, 0, 50)
        book.up("e3", 50)
        book.down("e4", 0, 0, 1000)
        book.move("e5", 100, 0, 1050)
        book.up("e6", 1050)
        self.assertEqual(book.recognize(1050), ["right", "right"])
        self.assertEqual(book.dropped_count(), 0)

    def test_unclosed_segment_never_produced(self):
        book = Gesture(300, 5, 10)
        book.down("e1", 0, 0, 0)
        book.move("e2", 100, 0, 50)
        self.assertEqual(book.recognize(50), [])
        self.assertEqual(book.recognize(5000), [])

    def test_closed_segment_produced_exactly_once(self):
        book = Gesture(300, 5, 10)
        book.down("e1", 0, 0, 0)
        book.move("e2", 100, 0, 50)
        book.up("e3", 50)
        self.assertEqual(book.recognize(50), ["right"])
        self.assertEqual(book.recognize(60), [])
        scanned = book.scanned_count()
        book.recognize(70)
        self.assertEqual(book.scanned_count(), scanned)

    def test_output_ordered_by_completion_time(self):
        book = Gesture(300, 5, 10)
        book.down("e1", 0, 0, 0)
        book.move("e2", 100, 0, 200)
        book.up("e3", 200)
        book.down("e4", 0, 0, 0)
        book.move("e5", 0, 100, 100)
        book.up("e6", 100)
        self.assertEqual(book.recognize(200), ["up", "right"])


if __name__ == "__main__":
    unittest.main()
