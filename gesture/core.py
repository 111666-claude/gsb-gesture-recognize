"""滑动手势识别：按 down / move / up 分成一段段手势，逐段识别方向。

缺陷：段的跨度不校验、方向平手时判成垂直、同一 event_id 重复 down 会重置段、
每秒产出没有预算、每次识别全扫历史事件。
"""


class Gesture:
    """手势分段台账。"""

    def __init__(self, max_ms=300, min_dist=5, budget_per_sec=1):
        self.max_ms = max_ms
        self.min_dist = min_dist
        self.budget = budget_per_sec
        self.events = []
        self.spent = {}
        self.dropped = 0
        self.scanned = 0

    def down(self, event_id, x, y, at_ms):
        """开始一段手势。缺陷：同一 event_id 重复 down 会重置当前段。"""
        self.events.append(("down", x, y, at_ms))
        return True

    def move(self, event_id, x, y, at_ms):
        """段内移动。缺陷：同一 event_id 不去重。"""
        self.events.append(("move", x, y, at_ms))
        return True

    def up(self, event_id, at_ms):
        """结束当前段。"""
        self.events.append(("up", 0, 0, at_ms))
        return True

    def recognize(self, now_ms):
        """返回本刻产出的手势方向。缺陷：不校验跨度、平手判垂直、全扫、没有预算。"""
        self.scanned += len(self.events)
        out = []
        segment = []
        for kind, x, y, at in self.events:
            if kind == "down":
                segment = [(x, y, at)]
            elif kind == "move":
                segment.append((x, y, at))
            elif kind == "up":
                if len(segment) >= 2:
                    direction = self._direction(segment[0], segment[-1])
                    if direction is not None:
                        out.append(direction)
                segment = []
        return out

    def _direction(self, start, end):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        if dx * dx + dy * dy < self.min_dist * self.min_dist:
            return None
        if abs(dx) > abs(dy):
            return "right" if dx > 0 else "left"
        return "up" if dy > 0 else "down"

    def dropped_count(self):
        return self.dropped

    def scanned_count(self):
        return self.scanned
