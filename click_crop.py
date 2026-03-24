import os
import time
from datetime import datetime

import mss
from PIL import Image
from pynput import mouse

CROP_SIZE = 40  # 60x60
HALF = CROP_SIZE // 2

OUT_DIR = "click_shots"
os.makedirs(OUT_DIR, exist_ok=True)


def grab_centered(x: int, y: int) -> Image.Image:
    # 注意：pynput 的回调在独立线程执行；mss 在 Windows 上不是线程安全的。
    # 这里在当前线程创建/释放 mss，避免 '_thread._local' object has no attribute 'srcdc'。
    with mss.mss() as sct:
        mon = sct.monitors[0]  # 全虚拟屏幕（含多显示器）
        left = int(x - HALF)
        top = int(y - HALF)
        right = left + CROP_SIZE
        bottom = top + CROP_SIZE

        # 裁剪区域与屏幕交集（避免点到边缘时报错）
        clip_left = max(left, mon["left"])
        clip_top = max(top, mon["top"])
        clip_right = min(right, mon["left"] + mon["width"])
        clip_bottom = min(bottom, mon["top"] + mon["height"])

        w = max(0, clip_right - clip_left)
        h = max(0, clip_bottom - clip_top)
        if w == 0 or h == 0:
            raise RuntimeError("点击位置不在可截屏范围内")

        img = sct.grab({"left": clip_left, "top": clip_top, "width": w, "height": h})
        im = Image.frombytes("RGB", img.size, img.rgb)

    # 若在边缘，补黑边到 60x60，保证输出尺寸一致
    if w != CROP_SIZE or h != CROP_SIZE:
        canvas = Image.new("RGB", (CROP_SIZE, CROP_SIZE), (0, 0, 0))
        paste_x = clip_left - left
        paste_y = clip_top - top
        canvas.paste(im, (paste_x, paste_y))
        return canvas

    return im


def on_click(x, y, button, pressed):
    # 只在右键按下时截图
    if (not pressed) or (button != mouse.Button.right):
        return

    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = os.path.join(OUT_DIR, f"{ts}_x{x}_y{y}.png")

    try:
        im = grab_centered(int(x), int(y))
        im.save(filename)
        print(f"已保存: {filename}")
    except Exception as e:
        print(f"截图失败: {e}")

    # 防止高频点击时文件名过于接近
    time.sleep(0.02)


if __name__ == "__main__":
    print("开始监听鼠标点击：右键按下即保存 60x60 截图到 ./click_shots")
    print("退出方式：在此窗口按 Ctrl+C")
    listener = mouse.Listener(on_click=on_click)
    listener.start()
    try:
        # 勿用 listener.join() 阻塞主线程：Windows 上 Ctrl+C 往往无法打断 join
        while listener.running:
            time.sleep(0.15)
    except KeyboardInterrupt:
        pass
    finally:
        listener.stop()
        listener.join(timeout=3.0)
    print("已退出。")
