"""命令行入口：跑手势识别样例。"""

import argparse

from .core import Gesture


def build_parser():
    parser = argparse.ArgumentParser(prog="gesture-recognize", description="滑动手势识别")
    parser.add_argument("--sample", default="window", help="window / dir / dup / budget / scan")
    return parser


def swipe(book, tag, x0, y0, x1, y1, start_ms, end_ms):
    book.down(tag + "-down", x0, y0, start_ms)
    book.move(tag + "-move", x1, y1, end_ms)
    book.up(tag + "-up", end_ms)


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.sample == "window":
        book = Gesture(max_ms=300, min_dist=5, budget_per_sec=10)
        swipe(book, "g1", 0, 0, 100, 0, 0, 1000)
        print("count=%d" % len(book.recognize(1000)))
    elif args.sample == "dir":
        book = Gesture(max_ms=300, min_dist=5, budget_per_sec=10)
        swipe(book, "g1", 0, 0, 10, 10, 0, 100)
        print("dir=%s" % book.recognize(100)[0])
    elif args.sample == "dup":
        book = Gesture(max_ms=300, min_dist=5, budget_per_sec=10)
        book.down("e1", 0, 0, 0)
        book.down("e1", 100, 0, 10)
        book.move("e2", 100, 0, 20)
        book.up("e3", 20)
        print("count=%d" % len(book.recognize(20)))
    elif args.sample == "budget":
        book = Gesture(max_ms=300, min_dist=5, budget_per_sec=1)
        swipe(book, "g1", 0, 0, 100, 0, 0, 50)
        swipe(book, "g2", 0, 0, 100, 0, 100, 150)
        dirs = book.recognize(150)
        print("count=%d dropped=%d" % (len(dirs), book.dropped_count()))
    elif args.sample == "scan":
        book = Gesture(max_ms=300, min_dist=5, budget_per_sec=1000000)
        for index in range(1000):
            swipe(book, "g-%d" % index, 0, 0, 100, 0, index * 10, index * 10 + 5)
        for _ in range(3000):
            book.recognize(5000)
        print("scanned=%d" % book.scanned_count())
    else:
        raise SystemExit("需要 --sample window|dir|dup|budget|scan")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
