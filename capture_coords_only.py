import csv
import os
import time
from datetime import datetime

from pynput import mouse


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "calib")
CSV_PATH = os.path.join(OUT_DIR, "extra_coords.csv")


def ensure_out_file() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(["index", "x", "y", "captured_at"])


def append_coord(idx: int, x: int, y: int) -> None:
    with open(CSV_PATH, "a", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow([idx, x, y, datetime.now().isoformat(timespec="seconds")])


def main() -> None:
    ensure_out_file()
    print("坐标捕捉（简版）已启动。")
    print(f"输出文件：{CSV_PATH}")
    print("操作：每次鼠标右键按下记录一次坐标；Ctrl+C 退出。")

    count = 0
    lockout_until = 0.0

    def on_click(x, y, button, pressed):
        nonlocal count, lockout_until
        if not pressed:
            return
        if button != mouse.Button.right:
            return

        now = time.time()
        if now < lockout_until:
            return
        lockout_until = now + 0.12

        count += 1
        ax = int(x)
        ay = int(y)
        append_coord(count, ax, ay)
        print(f"[{count}] x={ax}, y={ay}")

    listener = mouse.Listener(on_click=on_click)
    listener.start()
    try:
        listener.join()
    except KeyboardInterrupt:
        listener.stop()
        print(f"已退出，共记录 {count} 个坐标。")
        print(f"结果保存在：{CSV_PATH}")


if __name__ == "__main__":
    main()

