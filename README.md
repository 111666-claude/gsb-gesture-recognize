# gesture-recognize

滑动手势识别：从带时间戳的触摸点里识别四方向滑动，只用 Python 标准库。

```
python3 -m gesture.cli --sample window
python3 -m gesture.cli --sample dir
python3 -m gesture.cli --sample dup
python3 -m gesture.cli --sample scan
python3 -m unittest discover -s tests -v
```

## 口径（README 为准）

- **时间窗口**：只看 `[now_ms - max_ms, now_ms]` 内的触摸点，窗口外的点不参与识别。
- **位移**：取窗口内最早与最晚两个点算位移，位移长度不小于 `min_dist` 才算一次滑动。
- **方向**：`|dx|` 不小于 `|dy|` 时算水平（平手算水平），否则算垂直；正负号决定 right / left / up / down。
- **幂等**：同一个 `event_id` 只入队一次，重复推送不改变缓冲。
- **查询代价**：`recognize` 只取窗口内的首尾两点，`scanned_count()` 不随缓冲点数乘识别次数增长。
- **规模**：每秒 10 万次触摸与识别，单次摊还 O(1)。

## 输出契约（不改格式）

```
dir=..
scanned=..
```

## 目录

```
gesture/core.py   窗口裁剪、位移与方向量化
gesture/cli.py    命令行入口
tests/            unittest 用例
```
