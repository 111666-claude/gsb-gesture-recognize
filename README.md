# gesture-recognize

滑动手势识别：按 down / move / up 分成一段段手势，逐段识别方向，只用 Python 标准库。

```
python3 -m gesture.cli --sample window
python3 -m gesture.cli --sample dir
python3 -m gesture.cli --sample dup
python3 -m gesture.cli --sample budget
python3 -m gesture.cli --sample scan
python3 -m unittest discover -s tests -v
```

## 口径（README 为准）

- **分段状态机**：只有 `down` 开头、`up` 收尾的一段才是一次手势；`up` 之后该段清空，不会再次产出；
  没有收尾的段永远不产出。
- **跨度**：`up` 时刻减去 `down` 时刻大于 `max_ms` 的段作废。
- **位移与方向**：段内最早与最晚两点的位移长度不小于 `min_dist` 才算一次滑动；
  `|dx|` 不小于 `|dy|` 算水平（平手算水平），否则垂直，正负号决定 right / left / up / down。
- **幂等**：同一个 `event_id` 只生效一次，重复 `down` 不重置当前段。
- **预算配额**：同一整秒产出的手势数不超过 `budget_per_sec`，放不下的丢弃并计入 `dropped`；
  产出按完成时刻升序。
- **代价**：`recognize` 只处理已经收尾且尚未产出的段，`scanned_count()` 不随历史事件数乘识别次数增长。
- **规模**：每秒 10 万次触摸与识别，单次摊还 O(1)，内存只跟未完成的段有关。

## 输出契约（不改格式）

```
count=..
dir=..
count=.. dropped=..
scanned=..
```

## 目录

```
gesture/core.py   分段状态机、跨度、方向量化与预算
gesture/cli.py    命令行入口
tests/            unittest 用例
```
