import os
import sys
import random
import tkinter as tk


# -------------------------
# настройки
# -------------------------
MESSAGES = [
    "drink water ♡",
    "mon chouchou ♡",
    "have a good day ♡",
    "i love you ♡",
    "bois un peu d'eau ♡",
    "prends soin de toi ♡",
    "petit rappel ♡",
    "n'oublie pas de boire ♡",
    "tu es précieux ♡",
    "je pense à toi ♡"
]

WINDOW_WIDTH = 300
WINDOW_HEIGHT = 70
DURATION_MS = 5000

CARD_BG = "#f7eef5"
SHADOW_BG = "#ddcad8"
TEXT_MAIN = "#5f5363"

TRANSPARENT_KEY = "#01F0F1"
CAT_GIF_PATH = "kit.gif"

IS_WINDOWS = sys.platform.startswith("win")


# -------------------------
# утилиты
# -------------------------
def resource_path(relative_path: str):
    return os.path.join(os.path.abspath("."), relative_path)


def rounded_rect(canvas, x1, y1, x2, y2, r, **kwargs):
    points = [
        x1 + r, y1,
        x2 - r, y1,
        x2, y1,
        x2, y1 + r,
        x2, y2 - r,
        x2, y2,
        x2 - r, y2,
        x1 + r, y2,
        x1, y2,
        x1, y2 - r,
        x1, y1 + r,
        x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, splinesteps=36, **kwargs)


# -------------------------
# виджет
# -------------------------
class WaterToast:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.message = random.choice(MESSAGES)

        self.frames = []
        self.frame_index = 0
        self.cat_item = None

        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.0)

        if IS_WINDOWS:
            self.root.configure(bg=TRANSPARENT_KEY)
            try:
                self.root.wm_attributes("-transparentcolor", TRANSPARENT_KEY)
            except:
                pass
            canvas_bg = TRANSPARENT_KEY
        else:
            self.root.configure(bg=CARD_BG)
            canvas_bg = CARD_BG

        screen_w = self.root.winfo_screenwidth()

        margin = 16
        self.final_x = screen_w - WINDOW_WIDTH - margin
        self.final_y = margin
        self.start_y = self.final_y - 18

        self.root.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{self.final_x}+{self.start_y}"
        )

        self.canvas = tk.Canvas(
            self.root,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            bg=canvas_bg,
            highlightthickness=0,
            bd=0,
        )
        self.canvas.pack()

        self.draw_ui()

        self.root.bind("<Button-1>", lambda e: self.hide())
        self.root.after(10, self.animate_in)

    # -------------------------
    # GIF загрузка
    # -------------------------
    def load_gif(self, path):

        i = 0

        while True:
            try:
                frame = tk.PhotoImage(file=path, format=f"gif -index {i}").subsample(2,2)
                self.frames.append(frame)
                i += 1
            except:
                break

    # -------------------------
    # GIF анимация
    # -------------------------
    def animate_gif(self):

        if not self.frames:
            return

        frame = self.frames[self.frame_index]

        self.canvas.itemconfig(self.cat_item, image=frame)

        self.frame_index = (self.frame_index + 1) % len(self.frames)

        self.root.after(120, self.animate_gif)

    def draw_ui(self):

        rounded_rect(
            self.canvas,
            10, 10, WINDOW_WIDTH - 2, WINDOW_HEIGHT - 2,
            24,
            fill=SHADOW_BG,
            outline=""
        )

        rounded_rect(
            self.canvas,
            4, 4, WINDOW_WIDTH - 8, WINDOW_HEIGHT - 8,
            24,
            fill=CARD_BG,
            outline=""
        )

        gif_path = resource_path(CAT_GIF_PATH)

        cat_x = 10
        cat_y = WINDOW_HEIGHT // 2

        text_x = 110
        text_y = WINDOW_HEIGHT // 2

        if os.path.exists(gif_path):

            self.load_gif(gif_path)

            if self.frames:
                self.cat_item = self.canvas.create_image(
                    cat_x,
                    cat_y,
                    image=self.frames[0],
                    anchor="w"
                )

                self.animate_gif()

        else:

            self.canvas.create_text(
                30,
                cat_y,
                text="🐱",
                font=("Monocraft", 13, "bold"),
                fill=TEXT_MAIN,
                anchor="w"
            )

        self.canvas.create_text(
            text_x,
            text_y,
            text=self.message,
            font=("Monocraft", 13, "bold"),
            fill=TEXT_MAIN,
            anchor="w"
        )

    def animate_in(self, step=0):

        total_steps = 12
        progress = min(step / total_steps, 1.0)

        alpha = 0.97 * progress
        y = int(self.start_y + (self.final_y - self.start_y) * progress)

        self.root.attributes("-alpha", alpha)

        self.root.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{self.final_x}+{y}"
        )

        if step < total_steps:
            self.root.after(14, lambda: self.animate_in(step + 1))
        else:
            self.root.after(DURATION_MS, self.hide)

    def hide(self, step=0):

        total_steps = 10
        progress = min(step / total_steps, 1.0)

        alpha = 0.97 * (1.0 - progress)
        y = int(self.final_y - 10 * progress)

        self.root.attributes("-alpha", alpha)

        self.root.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{self.final_x}+{y}"
        )

        if step < total_steps:
            self.root.after(14, lambda: self.hide(step + 1))
        else:
            self.root.destroy()


REMINDER_INTERVAL = 60 * 60 * 1000  # 1 час


def show_toast():
    toast_root = tk.Toplevel(root)
    WaterToast(toast_root)

    root.after(REMINDER_INTERVAL, show_toast)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # скрываем основное окно

    show_toast()

    root.mainloop()