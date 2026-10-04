"""滑动手势识别：按 down / move / up 分成一段段手势，逐段识别方向。

分段状态机：down 开头、up 收尾的一段才是一次手势；up 之后该段清空不再产出，
没收尾的段不产出。recognize 只处理已收尾且尚未产出的段。
"""


class Gesture:
    """手势分段台账。"""

    def __init__(self, max_ms=300, min_dist=5, budget_per_sec=1):
        self.max_ms = max_ms
        self.min_dist = min_dist
        self.budget = budget_per_sec
        self._seen_ids = set()
        self._open = []
        self._open_down_at = None
        self._closed = []
        self._spent = {}
        self.dropped = 0
        self.scanned = 0

    def down(self, event_id, x, y, at_ms):
        """开始一段手势；同一 event_id 重复 down 不重置当前段。"""
        if event_id in self._seen_ids:
            return False
        self._seen_ids.add(event_id)
        self._open = [(x, y, at_ms)]
        self._open_down_at = at_ms
        return True

    def move(self, event_id, x, y, at_ms):
        """段内移动；同一 event_id 只生效一次，段外的 move 忽略。"""
        if event_id in self._seen_ids:
            return False
        self._seen_ids.add(event_id)
        if self._open:
            self._open.append((x, y, at_ms))
        return True

    def up(self, event_id, at_ms):
        """结束当前段；没有进行中的段则忽略。"""
        if event_id in self._seen_ids:
            return False
        self._seen_ids.add(event_id)
        if self._open:
            self._closed.append((at_ms, self._open_down_at, self._open))
            self._open = []
            self._open_down_at = None
        return True

    def recognize(self, now_ms):
        """产出已收尾且尚未产出的段，按完成时刻升序，受每秒预算约束。"""
        pending = self._closed
        self._closed = []
        pending.sort(key=lambda segment: segment[0])
        out = []
        for up_at, down_at, points in pending:
            self.scanned += len(points) + 1
            if up_at - down_at > self.max_ms:
                continue
            direction = self._direction(points)
            if direction is None:
                continue
            second = up_at // 1000
            used = self._spent.get(second, 0)
            if used >= self.budget:
                self.dropped += 1
                continue
            self._spent[second] = used + 1
            out.append(direction)
        return out

    def _direction(self, points):
        if len(points) < 2:
            return None
        first = min(points, key=lambda point: point[2])
        last = max(points, key=lambda point: point[2])
        dx = last[0] - first[0]
        dy = last[1] - first[1]
        if dx * dx + dy * dy < self.min_dist * self.min_dist:
            return None
        if abs(dx) >= abs(dy):
            return "right" if dx > 0 else "left"
        return "up" if dy > 0 else "down"

    def dropped_count(self):
        return self.dropped

    def scanned_count(self):
        return self.scanned
