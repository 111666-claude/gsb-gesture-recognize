"""命令行入口：跑手势识别样例。"""

import argparse

from .core import Gesture


def build_parser():
    parser = argparse.ArgumentParser(prog="gesture-recognize", description="滑动手势识别")
    parser.add_argument("--sample", default="window", help="window / dir / dup / scan")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.sample == "window":
        book = Gesture(max_ms=300, min_dist=5)
        book.push("e1", 0, 0, 0)
        book.push("e2", 100, 0, 1000)
        print("dir=%s" % book.recognize(1000))
    elif args.sample == "dir":
        book = Gesture(max_ms=300, min_dist=5)
        book.push("e1", 0, 0, 0)
        book.push("e2", 10, 10, 100)
        print("dir=%s" % book.recognize(100))
    elif args.sample == "dup":
        book = Gesture(max_ms=300, min_dist=5)
        book.push("e1", 0, 0, 0)
        book.push("e1", 50, 0, 50)
        print("dir=%s" % book.recognize(50))
    elif args.sample == "scan":
        book = Gesture(max_ms=1000000, min_dist=5)
        for index in range(3000):
            book.push("e-%d" % index, index, 0, index)
        for _ in range(3000):
            book.recognize(2999)
        print("scanned=%d" % book.scanned_count())
    else:
        raise SystemExit("需要 --sample window|dir|dup|scan")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
