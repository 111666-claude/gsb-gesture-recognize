"""滑动手势识别：按 down / move / up 分成一段段手势，逐段识别方向。"""


class Gesture:
    """手势分段台账。

    一段手势以 down 开头、up 收尾；up 后该段清空且只产出一次，未收尾的段
    永远不产出。recognize 只处理已收尾尚未产出的段，按完成时刻升序产出，
    每个整秒受 budget_per_sec 配额限制。
    """

    def __init__(self, max_ms=300, min_dist=5, budget_per_sec=1):
        self.max_ms = max_ms
        self.min_dist = min_dist
        self.budget = budget_per_sec
        self._seen = set()
        self._active = None
        self._finished = []
        self.spent = {}
        self.dropped = 0
        self.scanned = 0

    def down(self, event_id, x, y, at_ms):
        """开始一段手势；重复 event_id 或段未收尾时无效，不会重置当前段。"""
        if event_id in self._seen or self._active is not None:
            return False
        self._seen.add(event_id)
        self._active = [[x, y, at_ms], [x, y, at_ms]]
        return True

    def move(self, event_id, x, y, at_ms):
        """记录段内移动点（取段内最早/最晚时刻的点）；重复 id 或无段时无效。"""
        if event_id in self._seen or self._active is None:
            return False
        self._seen.add(event_id)
        point = (x, y, at_ms)
        if at_ms < self._active[0][2]:
            self._active[0] = point
        if at_ms > self._active[1][2]:
            self._active[1] = point
        return True

    def up(self, event_id, at_ms):
        """收尾当前段；重复 event_id 或没有进行中的段时无效。"""
        if event_id in self._seen or self._active is None:
            return False
        self._seen.add(event_id)
        start, end = tuple(self._active[0]), tuple(self._active[1])
        self._finished.append((at_ms, start, end))
        self._active = None
        return True

    def recognize(self, now_ms):
        """处理已收尾且未产出的段，按完成时刻升序返回本刻产出的方向。"""
        out = []
        pending = self._finished
        self._finished = []
        pending.sort(key=lambda item: item[0])
        for end_at, start, end in pending:
            self.scanned += 1
            if end_at - start[2] > self.max_ms:
                continue
            direction = self._direction(start, end)
            if direction is None:
                continue
            second = end_at // 1000
            used = self.spent.get(second, 0)
            if used >= self.budget:
                self.dropped += 1
                continue
            self.spent[second] = used + 1
            out.append(direction)
        return out

    def _direction(self, start, end):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        if dx * dx + dy * dy < self.min_dist * self.min_dist:
            return None
        if abs(dx) >= abs(dy):
            return "right" if dx > 0 else "left"
        return "up" if dy > 0 else "down"

    def dropped_count(self):
        return self.dropped

    def scanned_count(self):
        return self.scanned
