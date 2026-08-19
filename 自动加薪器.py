import tkinter as tk
from tkinter import ttk


class SalaryBooster:
    def __init__(self, root):
        self.root = root
        self.root.title("公司智能加薪系统.exe")
        self.root.geometry("600x720")
        self.root.minsize(560, 680)
        self.root.configure(bg="#f1f3f5")
        self.stage = 0
        self.font_size = 38
        self.dialog = None
        self.build_ui()

    def build_ui(self):
        style = ttk.Style()
        style.theme_use("vista")
        style.configure("Raise.TButton", font=("Microsoft YaHei UI", 14, "bold"), padding=12)

        titlebar = tk.Frame(self.root, bg="#1672c7", height=46)
        titlebar.pack(fill="x")
        tk.Label(titlebar, text="公司智能加薪系统  Pro Max", bg="#1672c7", fg="white",
                 font=("Microsoft YaHei UI", 12, "bold")).pack(side="left", padx=16, pady=11)
        tk.Label(titlebar, text="—　□　×", bg="#1672c7", fg="white",
                 font=("Microsoft YaHei UI", 12)).pack(side="right", padx=14)

        body = tk.Frame(self.root, bg="#f1f3f5")
        body.pack(fill="both", expand=True, padx=36, pady=30)
        tk.Label(body, text="AI 自动加薪器", bg="#f1f3f5", fg="#222",
                 font=("Microsoft YaHei UI", 25, "bold")).pack()
        tk.Label(body, text="一次操作，立即看到明显变化", bg="#f1f3f5", fg="#777",
                 font=("Microsoft YaHei UI", 11)).pack(pady=(6, 24))

        employee = tk.Frame(body, bg="white", bd=1, relief="solid")
        employee.pack(fill="x")
        self.make_info(employee, "员工姓名", "码上搞笑", 0)
        self.make_info(employee, "所在部门", "废物软件研究所", 1)
        self.make_info(employee, "加薪审批状态", "老板已授权AI全权处理", 2)

        tk.Label(body, text="当前月薪", bg="#f1f3f5", fg="#666",
                 font=("Microsoft YaHei UI", 11)).pack(pady=(25, 8))
        self.salary_canvas = tk.Canvas(body, height=190, bg="white", bd=1,
                                       relief="solid", highlightthickness=0)
        self.salary_canvas.pack(fill="x")
        self.salary_text = self.salary_canvas.create_text(
            264, 95, text="3000元", fill="#222",
            font=("Microsoft YaHei UI", self.font_size, "bold")
        )
        self.salary_canvas.bind("<Configure>", self.center_salary)

        self.change_label = tk.Label(body, text="本月变化：0元", bg="#f1f3f5", fg="#777",
                                     font=("Microsoft YaHei UI", 11))
        self.change_label.pack(pady=13)

        self.button = ttk.Button(body, text="开始加薪", style="Raise.TButton",
                                 command=self.raise_salary)
        self.button.pack(fill="x")
        self.progress = ttk.Progressbar(body, mode="determinate", maximum=100, value=0)
        self.progress.pack(fill="x", pady=(17, 8))
        self.status = tk.Label(body, text="系统状态：等待加薪", bg="#f1f3f5", fg="#777",
                               font=("Microsoft YaHei UI", 10))
        self.status.pack()

    def make_info(self, parent, name, value, row):
        tk.Label(parent, text=name, bg="white", fg="#777",
                 font=("Microsoft YaHei UI", 10)).grid(row=row, column=0, sticky="w", padx=16, pady=10)
        tk.Label(parent, text=value, bg="white", fg="#222",
                 font=("Microsoft YaHei UI", 11, "bold")).grid(row=row, column=1, sticky="e", padx=16, pady=10)
        parent.grid_columnconfigure(1, weight=1)

    def center_salary(self, event):
        self.salary_canvas.coords(self.salary_text, event.width / 2, 95)

    def raise_salary(self):
        targets = [78, 155, 310]
        if self.stage >= len(targets):
            return
        target = targets[self.stage]
        self.button.config(state="disabled")
        self.status.config(text="AI正在执行加薪操作……", fg="#d17900")
        self.animate_font(target)

    def animate_font(self, target):
        if self.font_size < target:
            self.font_size += max(2, (target - self.font_size) // 7)
            self.salary_canvas.itemconfig(
                self.salary_text,
                font=("Microsoft YaHei UI", self.font_size, "bold")
            )
            self.progress["value"] = min(95, self.progress["value"] + 8)
            self.root.after(35, lambda: self.animate_font(target))
            return
        self.font_size = target
        self.salary_canvas.itemconfig(
            self.salary_text,
            font=("Microsoft YaHei UI", self.font_size, "bold")
        )
        self.progress["value"] = 100
        self.finish_raise()

    def finish_raise(self):
        messages = [
            ("加薪成功", "恭喜！\n您的工资已经明显变大。"),
            ("再次加薪成功", "本次加薪幅度：100%\n当前工资：3000元"),
            ("加薪失败", "已达到公司预算上限\n暂时无法继续放大。"),
        ]
        title, message = messages[self.stage]
        self.change_label.config(text="本月变化：0元", fg="#c40000")
        self.status.config(text="系统状态：加薪操作已完成", fg="#16823b")
        self.stage += 1
        self.show_dialog(title, message)

    def show_dialog(self, title, message):
        self.root.bell()
        self.dialog = tk.Toplevel(self.root)
        self.dialog.title(title)
        self.dialog.geometry("460x235")
        self.dialog.resizable(False, False)
        self.dialog.transient(self.root)
        self.dialog.grab_set()

        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 460) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 235) // 2
        self.dialog.geometry(f"460x235+{x}+{y}")

        panel = tk.Frame(self.dialog, bg="#f7f7f7")
        panel.pack(fill="both", expand=True)
        tk.Label(panel, text="$", bg="#16823b", fg="white",
                 font=("Segoe UI", 25, "bold"), width=2).place(x=29, y=50)
        tk.Label(panel, text=message, bg="#f7f7f7", fg="#111",
                 font=("Microsoft YaHei UI", 18, "bold"), justify="left").place(x=110, y=43)
        bottom = tk.Frame(panel, bg="#e9e9e9", height=62)
        bottom.pack(side="bottom", fill="x")
        ttk.Button(bottom, text="确定", command=self.close_dialog).pack(
            side="right", padx=22, pady=14, ipadx=27
        )
        self.dialog.bind("<Return>", lambda _event: self.close_dialog())

    def close_dialog(self):
        if self.dialog and self.dialog.winfo_exists():
            self.dialog.grab_release()
            self.dialog.destroy()
        self.progress["value"] = 0
        if self.stage == 1:
            self.button.config(text="继续加薪", state="normal")
        elif self.stage == 2:
            self.button.config(text="还不够，再加一点", state="normal")
        else:
            self.button.config(text="公司已无力承担", state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    SalaryBooster(root)
    root.mainloop()
