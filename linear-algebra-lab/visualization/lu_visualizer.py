"""Run ``python -m visualization.lu_visualizer`` from the project root."""

import math
import tkinter as tk
from tkinter import messagebox

from linear_algebra import Matrix, Vector
from .lu_steps import build_lu_steps


def parse_matrix(text):
    rows = [[float(value) for value in row.split()] for row in text.split(";")]
    return Matrix(rows)


def parse_vector(text):
    return Vector(float(value) for value in text.replace(";", " ").split())


def interpolate(before, after, progress):
    """Return a matrix between two snapshots for a visible transition."""
    if before is None:
        return after
    return [
        [old + (new - old) * progress for old, new in zip(old_row, new_row)]
        for old_row, new_row in zip(before, after)
    ]


def ease_in_out(progress):
    """A gentle acceleration and deceleration for visual transitions."""
    return progress * progress * (3 - 2 * progress)


class LUVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("LU 分解：算法过程动画")
        self.root.configure(bg="#090b10")
        self.steps = []
        self.step_index = 0
        self.playing = False
        self.animating = False

        controls = tk.Frame(root, padx=12, pady=8, bg="#090b10")
        controls.pack(fill="x")
        label_style = {"bg": "#090b10", "fg": "#e2e8f0"}
        button_style = {"bg": "#1e293b", "fg": "#f8fafc", "activebackground": "#334155", "activeforeground": "#ffffff", "relief": "flat"}
        tk.Label(controls, text="A（行用 ; 分隔）：", **label_style).grid(row=0, column=0, sticky="w")
        self.matrix_input = tk.Entry(controls, width=28, bg="#111827", fg="#f8fafc", insertbackground="#f8fafc", relief="flat")
        self.matrix_input.insert(0, "2 1; 4 3")
        self.matrix_input.grid(row=0, column=1, padx=4)
        tk.Label(controls, text="b：", **label_style).grid(row=1, column=0, sticky="w")
        self.vector_input = tk.Entry(controls, width=28, bg="#111827", fg="#f8fafc", insertbackground="#f8fafc", relief="flat")
        self.vector_input.insert(0, "5 11")
        self.vector_input.grid(row=1, column=1, padx=4)
        tk.Button(controls, text="生成动画", command=self.load, **button_style).grid(row=0, column=2, rowspan=2, padx=8)

        self.title = tk.Label(root, font=("Microsoft YaHei", 16, "bold"), pady=4, bg="#090b10", fg="#f8fafc")
        self.title.pack()
        self.operation = tk.Label(root, font=("Microsoft YaHei", 12), fg="#7dd3fc", bg="#090b10", pady=4)
        self.operation.pack()
        self.canvas = tk.Canvas(root, width=840, height=310, bg="#090b10", highlightthickness=0)
        self.canvas.pack(padx=10, pady=4)

        navigation = tk.Frame(root, pady=10, bg="#090b10")
        navigation.pack()
        tk.Button(navigation, text="上一步", command=self.previous, **button_style).pack(side="left", padx=4)
        tk.Button(navigation, text="下一步", command=self.next, **button_style).pack(side="left", padx=4)
        self.play_button = tk.Button(navigation, text="自动播放", command=self.toggle_play, **button_style)
        self.play_button.pack(side="left", padx=4)
        self.counter = tk.Label(navigation, **label_style)
        self.counter.pack(side="left", padx=12)

        self.load()

    def load(self):
        try:
            result = build_lu_steps(parse_matrix(self.matrix_input.get()), parse_vector(self.vector_input.get()))
        except (ValueError, IndexError) as error:
            messagebox.showerror("输入错误", str(error))
            return
        self.steps = result["steps"]
        self.step_index = 0
        self.playing = False
        self.play_button.config(text="自动播放")
        self.draw(self.steps[0])

    def draw_matrix(self, label, matrix, left, top, highlight=None, target=None, target_shift=0, highlight_color="#86efac"):
        self.canvas.create_text(left, top - 22, text=label, anchor="w", fill="#f8fafc", font=("Consolas", 15, "bold"))
        cell = 42
        for row, values in enumerate(matrix):
            for column, value in enumerate(values):
                color = "#172033"
                if highlight == (row, column):
                    color = highlight_color
                elif target == row:
                    color = "#fed7aa"  # Row being eliminated
                row_shift = target_shift if target == row else 0
                x1, y1 = left + column * cell + row_shift, top + row * cell
                self.canvas.create_rectangle(x1, y1, x1 + cell, y1 + cell, fill=color, outline="#475569")
                text = "?" if value is None else f"{value:g}"
                self.canvas.create_text(x1 + cell / 2, y1 + cell / 2, text=text, fill="#f8fafc", font=("Consolas", 12))

    def draw_vector(self, label, values, left, top, active_row=None, color="#172033"):
        if values is None:
            self.canvas.create_text(left, top, text=f"{label}：等待", anchor="w", fill="#94a3b8", font=("Microsoft YaHei", 11))
            return
        highlight = None if active_row is None else (active_row, 0)
        self.draw_matrix(label, [[value] for value in values], left, top, highlight, highlight_color=color)

    def draw(self, step, previous=None, progress=1, target_shift=0):
        self.canvas.delete("all")
        upper = interpolate(previous["upper"], step["upper"], progress) if previous else step["upper"]
        lower = interpolate(previous["lower"], step["lower"], progress) if previous else step["lower"]
        self.title.config(text=step["title"])
        self.operation.config(text=step["operation"])
        pivot = step["pivot"] if step["phase"] == "eliminate" else None
        target = step["target"] if step["phase"] == "eliminate" else None
        y_values = step["y"]
        x_values = step["x"]
        # The answer is revealed near the end of its animated derivation.
        if step["phase"] == "forward" and y_values is not None and progress < 0.72:
            y_values = y_values[:]
            y_values[step["active_row"]] = None
        if step["phase"] == "backward" and x_values is not None and progress < 0.72:
            x_values = x_values[:]
            x_values[step["active_row"]] = None
        self.draw_matrix("L（记录消元倍数）", lower, 30, 70)
        self.canvas.create_text(300, 115, text="×", fill="#f8fafc", font=("Consolas", 24))
        self.draw_matrix("U（正在被消元）", upper, 340, 70, pivot, target, target_shift)
        self.canvas.create_text(620, 115, text="→", fill="#f8fafc", font=("Consolas", 24))
        forward_row = step["active_row"] if step["phase"] == "forward" else None
        backward_row = step["active_row"] if step["phase"] == "backward" else None
        self.draw_vector("y", y_values, 680, 70, forward_row, "#38bdf8")
        self.draw_vector("x", x_values, 760, 70, backward_row, "#c084fc")

        if step["phase"] == "eliminate":
            pivot_row, pivot_column = step["pivot"]
            target_row = step["target"]
            # The multiplier visibly travels from the row operation to L.
            start_x = 340 + pivot_column * 42 + 21
            start_y = 70 + target_row * 42 + 21
            end_x = 30 + pivot_column * 42 + 21
            end_y = 70 + target_row * 42 + 21
            moving_x = start_x + (end_x - start_x) * progress
            moving_y = start_y + (end_y - start_y) * progress
            self.canvas.create_line(start_x, start_y, end_x, end_y, arrow="last", fill="#f97316", width=2)
            self.canvas.create_oval(moving_x - 14, moving_y - 14, moving_x + 14, moving_y + 14, fill="#fed7aa", outline="#ea580c")
            self.canvas.create_text(moving_x, moving_y, text=f"{step['multiplier']:g}", font=("Consolas", 11, "bold"))
            self.canvas.create_text(30, 245, anchor="w", fill="#15803d", font=("Microsoft YaHei", 11), text="绿色：主元    橙色：正在消元的目标行")
        elif step["phase"] == "forward":
            # A blue marker moves from L toward the newly solved y entry.
            start_x, start_y = 190, 70 + step["active_row"] * 42 + 21
            end_x, end_y = 701, start_y
            x = start_x + (end_x - start_x) * progress
            self.canvas.create_oval(x - 10, start_y - 10, x + 10, start_y + 10, fill="#38bdf8", outline="")
            self.canvas.create_text(30, 245, anchor="w", fill="#175b8d", font=("Microsoft YaHei", 11), text="当前阶段：从上到下进行前代，求 L @ y = b。")
        elif step["phase"] == "backward":
            # A purple marker moves from U toward the newly solved x entry.
            start_x, start_y = 500, 70 + step["active_row"] * 42 + 21
            end_x, end_y = 781, start_y
            x = start_x + (end_x - start_x) * progress
            self.canvas.create_oval(x - 10, start_y - 10, x + 10, start_y + 10, fill="#c084fc", outline="")
            self.canvas.create_text(30, 245, anchor="w", fill="#175b8d", font=("Microsoft YaHei", 11), text="当前阶段：从下到上进行回代，求 U @ x = y。")
        else:
            self.canvas.create_text(30, 245, anchor="w", fill="#175b8d", font=("Microsoft YaHei", 11), text="动画按算法流程播放，而不是直接跳到最终解。")

        phases = ["开始", "消元", "L、U", "前代", "回代"]
        phase_index = {"start": 0, "eliminate": 1, "decomposed": 2, "forward": 3, "backward": 4}[step["phase"]]
        left, right, line_y = 80, 760, 280
        self.canvas.create_line(left, line_y, right, line_y, fill="#334155", width=2)
        for index, name in enumerate(phases):
            x = left + (right - left) * index / (len(phases) - 1)
            color = "#38bdf8" if index <= phase_index else "#334155"
            self.canvas.create_oval(x - 5, line_y - 5, x + 5, line_y + 5, fill=color, outline="")
            self.canvas.create_text(x, line_y + 17, text=name, fill="#94a3b8", font=("Microsoft YaHei", 9))
        self.counter.config(text=f"第 {self.step_index + 1} / {len(self.steps)} 步")

    def transition_to(self, new_index):
        if self.animating or new_index == self.step_index:
            return
        old_step = self.steps[self.step_index]
        new_step = self.steps[new_index]
        self.animating = True

        def frame(number):
            progress = ease_in_out(number / 30)
            # The target row moves out and returns while its values update.
            shift = 32 * math.sin(progress * math.pi) if new_step["phase"] == "eliminate" else 0
            self.draw(new_step, old_step, progress, shift)
            if number < 30:
                self.root.after(16, lambda: frame(number + 1))
            else:
                self.step_index = new_index
                self.animating = False
                self.draw(new_step)

        frame(1)

    def previous(self):
        if not self.animating:
            self.transition_to(max(0, self.step_index - 1))

    def next(self):
        if not self.animating:
            self.transition_to(min(len(self.steps) - 1, self.step_index + 1))

    def toggle_play(self):
        self.playing = not self.playing
        self.play_button.config(text="暂停" if self.playing else "自动播放")
        if self.playing:
            self.play()

    def play(self):
        if not self.playing:
            return
        if self.step_index >= len(self.steps) - 1:
            self.playing = False
            self.play_button.config(text="自动播放")
            return
        self.next()
        self.root.after(900, self.play)


if __name__ == "__main__":
    window = tk.Tk()
    LUVisualizer(window)
    window.mainloop()
