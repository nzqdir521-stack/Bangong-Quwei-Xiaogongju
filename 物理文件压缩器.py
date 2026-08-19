import tkinter as tk
from tkinter import ttk


class PhysicalCompressor:
    def __init__(self, root):
        self.root = root
        self.root.title("物理文件压缩器.exe")
        self.root.geometry("620x760")
        self.root.minsize(580, 720)
        self.root.configure(bg="#f1f3f5")

        self.stage = 0
        self.file_height = 190
        self.file_width = 155
        self.dialog = None
        self.animating = False
        self.build_ui()

    def build_ui(self):
        style = ttk.Style()
        style.theme_use("vista")
        style.configure("Compress.TButton", font=("Microsoft YaHei UI", 14, "bold"), padding=12)

        titlebar = tk.Frame(self.root, bg="#176fc1", height=46)
        titlebar.pack(fill="x")
        tk.Label(
            titlebar, text="物理文件压缩器  Pro Max",
            bg="#176fc1", fg="white",
            font=("Microsoft YaHei UI", 12, "bold")
        ).pack(side="left", padx=16, pady=11)
        tk.Label(
            titlebar, text="—　□　×", bg="#176fc1", fg="white",
            font=("Microsoft YaHei UI", 12)
        ).pack(side="right", padx=14)

        body = tk.Frame(self.root, bg="#f1f3f5")
        body.pack(fill="both", expand=True, padx=35, pady=27)

        tk.Label(
            body, text="物理文件压缩器", bg="#f1f3f5", fg="#222",
            font=("Microsoft YaHei UI", 25, "bold")
        ).pack()
        tk.Label(
            body, text="采用先进物理技术，真正压缩每一个文件",
            bg="#f1f3f5", fg="#777",
            font=("Microsoft YaHei UI", 11)
        ).pack(pady=(6, 20))

        info = tk.Frame(body, bg="white", bd=1, relief="solid")
        info.pack(fill="x")
        self.make_info(info, "文件名称", "年中工作报告.zip", 0)
        self.make_info(info, "文件大小", "2.00 GB", 1)
        self.make_info(info, "当前厚度", "8.00 cm", 2, value_name="thickness")

        self.canvas = tk.Canvas(
            body, height=300, bg="#e8edf2", bd=1,
            relief="solid", highlightthickness=0
        )
        self.canvas.pack(fill="x", pady=(19, 14))
        self.canvas.bind("<Configure>", lambda _event: self.draw_file())

        self.button = ttk.Button(
            body, text="开始物理压缩", style="Compress.TButton",
            command=self.compress
        )
        self.button.pack(fill="x")

        self.progress = ttk.Progressbar(body, maximum=100, mode="determinate")
        self.progress.pack(fill="x", pady=(17, 8))
        self.status = tk.Label(
            body, text="状态：等待压缩", bg="#f1f3f5", fg="#777",
            font=("Microsoft YaHei UI", 10)
        )
        self.status.pack()

        tk.Label(
            body, text="提示：本软件只改变文件厚度，不改变文件大小",
            bg="#f1f3f5", fg="#a0a0a0",
            font=("Microsoft YaHei UI", 9)
        ).pack(side="bottom", pady=(15, 0))

    def make_info(self, parent, key, value, row, value_name=None):
        tk.Label(
            parent, text=key, bg="white", fg="#777",
            font=("Microsoft YaHei UI", 10)
        ).grid(row=row, column=0, sticky="w", padx=16, pady=10)
        label = tk.Label(
            parent, text=value, bg="white", fg="#222",
            font=("Microsoft YaHei UI", 11, "bold")
        )
        label.grid(row=row, column=1, sticky="e", padx=16, pady=10)
        parent.grid_columnconfigure(1, weight=1)
        if value_name == "thickness":
            self.thickness_label = label

    def draw_file(self):
        self.canvas.delete("all")
        width = max(self.canvas.winfo_width(), 500)
        cx = width / 2
        bottom = 260
        top = bottom - self.file_height
        left = cx - self.file_width / 2
        right = cx + self.file_width / 2

        shadow_height = max(3, min(15, self.file_height * 0.08))
        self.canvas.create_oval(
            left - 20, bottom + 8,
            right + 20, bottom + 8 + shadow_height,
            fill="#aeb7c0", outline=""
        )

        fold = min(42, self.file_height * 0.28, self.file_width * 0.28)
        points = [
            left, top,
            right - fold, top,
            right, top + fold,
            right, bottom,
            left, bottom,
        ]
        self.canvas.create_polygon(
            points, fill="#ffffff", outline="#6f7d8a", width=2
        )
        if self.file_height > 22:
            self.canvas.create_polygon(
                right - fold, top,
                right - fold, top + fold,
                right, top + fold,
                fill="#dfe8f0", outline="#6f7d8a"
            )

        if self.file_height > 75:
            font_size = max(9, min(18, int(self.file_height / 10)))
            self.canvas.create_text(
                cx, top + self.file_height * 0.54,
                text="ZIP", fill="#176fc1",
                font=("Arial", font_size, "bold")
            )
            self.canvas.create_text(
                cx, top + self.file_height * 0.73,
                text="2.00 GB", fill="#555",
                font=("Microsoft YaHei UI", max(8, font_size - 5))
            )
        elif self.file_height > 12:
            self.canvas.create_text(
                cx, top + self.file_height / 2,
                text="2GB", fill="#176fc1",
                font=("Arial", 8, "bold")
            )

        self.canvas.create_text(
            cx, 282, text="年中工作报告.zip",
            fill="#333", font=("Microsoft YaHei UI", 11)
        )

    def compress(self):
        if self.animating:
            return
        targets = [58, 7]
        if self.stage >= len(targets):
            self.show_dialog(
                "压缩失败",
                "无法继续压缩\n文件已经没有厚度了。",
                warning=True
            )
            return

        self.animating = True
        self.button.config(state="disabled")
        self.status.config(text="状态：液压装置正在工作……", fg="#d07a00")
        self.progress["value"] = 5
        self.animate_to(targets[self.stage])

    def animate_to(self, target):
        if self.file_height > target:
            difference = self.file_height - target
            self.file_height -= max(2, difference // 8)
            self.progress["value"] = min(94, self.progress["value"] + 7)
            self.update_thickness()
            self.draw_file()
            self.root.after(40, lambda: self.animate_to(target))
            return

        self.file_height = target
        self.progress["value"] = 100
        self.update_thickness()
        self.draw_file()
        self.animating = False
        self.finish_compression()

    def update_thickness(self):
        thickness = 8 * self.file_height / 190
        self.thickness_label.config(text=f"{thickness:.2f} cm")

    def finish_compression(self):
        self.stage += 1
        if self.stage == 1:
            self.status.config(text="状态：压缩完成，文件大小未发生变化", fg="#16823b")
            self.show_dialog(
                "压缩成功",
                "文件大小：2.00 GB → 2.00 GB\n文件厚度：8.00 cm → 2.44 cm"
            )
        else:
            self.status.config(text="状态：文件已被压成一条线", fg="#c40000")
            self.show_dialog(
                "深度压缩成功",
                "文件大小：2.00 GB → 2.00 GB\n文件厚度：2.44 cm → 0.29 cm"
            )

    def show_dialog(self, title, message, warning=False):
        self.root.bell()
        self.dialog = tk.Toplevel(self.root)
        self.dialog.title(title)
        self.dialog.geometry("500x245")
        self.dialog.resizable(False, False)
        self.dialog.transient(self.root)
        self.dialog.grab_set()

        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 500) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 245) // 2
        self.dialog.geometry(f"500x245+{x}+{y}")

        panel = tk.Frame(self.dialog, bg="#f7f7f7")
        panel.pack(fill="both", expand=True)
        color = "#c43131" if warning else "#16823b"
        symbol = "!" if warning else "✓"
        tk.Label(
            panel, text=symbol, bg=color, fg="white",
            font=("Segoe UI Symbol", 24, "bold"), width=2
        ).place(x=28, y=52)
        tk.Label(
            panel, text=message, bg="#f7f7f7", fg="#111",
            font=("Microsoft YaHei UI", 16, "bold"), justify="left"
        ).place(x=108, y=44)
        bottom = tk.Frame(panel, bg="#e9e9e9", height=62)
        bottom.pack(side="bottom", fill="x")
        ttk.Button(
            bottom, text="确定", command=self.close_dialog
        ).pack(side="right", padx=22, pady=14, ipadx=28)
        self.dialog.bind("<Return>", lambda _event: self.close_dialog())

    def close_dialog(self):
        if self.dialog and self.dialog.winfo_exists():
            self.dialog.grab_release()
            self.dialog.destroy()
        self.progress["value"] = 0
        if self.stage == 1:
            self.button.config(text="继续压缩", state="normal")
        elif self.stage == 2:
            self.button.config(text="再压最后一次", state="normal")
        else:
            self.button.config(state="normal")


if __name__ == "__main__":
    app_root = tk.Tk()
    PhysicalCompressor(app_root)
    app_root.mainloop()
