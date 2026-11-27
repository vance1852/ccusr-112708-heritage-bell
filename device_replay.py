"""读取模拟现场的配置和设备帧，保持接收顺序。"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load_profile(root=ROOT):
    return json.loads((root / "data" / "site.json").read_text(encoding="utf-8"))


def read_frames(root=ROOT):
    with (root / "data" / "frames.jsonl").open(encoding="utf-8") as stream:
        for line in stream:
            yield json.loads(line)


def main():
    parser = argparse.ArgumentParser(description="按接收顺序读取本地联调消息")
    parser.add_argument("--root", type=Path, default=ROOT, help="含 data 目录的路径")
    args = parser.parse_args()
    load_profile(args.root)
    for frame in read_frames(args.root):
        print(json.dumps(frame, ensure_ascii=False))


if __name__ == "__main__":
    main()
