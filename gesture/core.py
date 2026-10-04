"""滑动手势识别：从带时间戳的触摸点里识别四方向滑动。

缺陷：窗口不裁剪、方向平手时判成垂直、同一 event_id 重复入队、位移阈值用小于比较、
每次识别全扫点表。
"""


class Gesture:
    """手势识别缓冲。"""

    def __init__(self, max_ms=300, min_dist=5):
        self.max_ms = max_ms
        self.min_dist = min_dist
        self.points = []
        self.seen = set()
        self.scanned = 0

    def push(self, event_id, x, y, at_ms):
        """记录一个触摸点。缺陷：event_id 不去重。"""
        self.points.append((x, y, at_ms))

    def recognize(self, now_ms):
        """识别滑动方向，识别不出来返回 None。缺陷：不裁窗口、平手判垂直、全扫点表。"""
        self.scanned += len(self.points)
        if len(self.points) < 2:
            return None
        start = self.points[0]
        end = self.points[-1]
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        if dx * dx + dy * dy < self.min_dist * self.min_dist:
            return None
        if abs(dx) > abs(dy):
            return "right" if dx > 0 else "left"
        return "up" if dy > 0 else "down"

    def scanned_count(self):
        return self.scanned
