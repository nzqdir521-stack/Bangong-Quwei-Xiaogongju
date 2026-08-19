import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta


class OffWorkCalculator:
    """搞笑短视频用桌面程序：只模拟关机，不会调用系统关机命令。"""

    def __init__(self, root):
        self.root = root
        self.root.title("智能下班计算器.exe")
        self.root.geometry("600x760")
        self.root.minsize(560, 700)
        self.root.configure(bg="#f2f2f2")
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)
        self.stage = 0
        self.jobs = []
        self.blackout = None
        self.dialog = None
        self.dialog_index = 0
        self.shutdown_angle = 0
        self.build_ui()

    def build_ui(self):
        style = ttk.Style()
        style.theme_use("vista")
        style.configure("Action.TButton", font=("Microsoft YaHei UI", 14, "bold"), padding=11)

        header = tk.Frame(self.root, bg="#1672c7", height=46)
        header.pack(fill="x")
        tk.Label(
            header, text="智能下班计算器  Pro Max",
            bg="#1672c7", fg="white", font=("Microsoft YaHei UI", 12, "bold")
        ).pack(side="left", padx=16, pady=11)
        tk.Label(header, text="—　□　×", bg="#1672c7", fg="white",
                 font=("Microsoft YaHei UI", 12)).pack(side="right", padx=13)

        body = tk.Frame(self.root, bg="#f2f2f2")
        body.pack(fill="both", expand=True, padx=34, pady=28)
        tk.Label(body, text="智能下班时间计算器", bg="#f2f2f2",
                 font=("Microsoft YaHei UI", 23, "bold")).pack()
        tk.Label(body, text="科学计算，拒绝无效加班", bg="#f2f2f2", fg="#777",
                 font=("Microsoft YaHei UI", 11)).pack(pady=(5, 22))

        form = tk.Frame(body, bg="#f2f2f2")
        form.pack(fill="x")
        self.start_var = tk.StringVar(value="09:00")
        self.hours_var = tk.StringVar(value="8")
        self.make_field(form, "今天几点上班", self.start_var, 0)
        self.make_field(form, "今天需要工作几小时", self.hours_var, 1)

        self.button = ttk.Button(body, text="开始计算下班时间", style="Action.TButton",
                                 command=self.next_step)
        self.button.pack(fill="x", pady=(20, 18))

        terminal_frame = tk.Frame(body, bg="#101820", bd=3, relief="sunken")
        terminal_frame.pack(fill="both", expand=True)
        self.log = tk.Text(
            terminal_frame, bg="#101820", fg="#bdcbd3", insertbackground="white",
            font=("Consolas", 12), relief="flat", padx=17, pady=15,
            wrap="word", state="disabled", height=12
        )
        self.log.pack(fill="both", expand=True)

        result_box = tk.Frame(body, bg="white", bd=1, relief="solid")
        result_box.pack(fill="x", pady=(16, 0))
        tk.Label(result_box, text="预计下班时间", bg="white", fg="#777",
                 font=("Microsoft YaHei UI", 10)).pack(pady=(12, 0))
        self.result = tk.Label(result_box, text="--:--", bg="white", fg="#222",
                               font=("Microsoft YaHei UI", 30, "bold"))
        self.result.pack(pady=(2, 11))

        self.status = tk.Label(body, text="系统状态：等待计算", bg="#f2f2f2", fg="#777",
                               font=("Microsoft YaHei UI", 10))
        self.status.pack(pady=12)

        self.write_log("系统初始化完成。\n正在等待员工提交下班申请……")

    def make_field(self, parent, label, variable, column):
        box = tk.Frame(parent, bg="white", bd=1, relief="solid")
        box.grid(row=0, column=column, sticky="ew", padx=(0, 7) if column == 0 else (7, 0))
        parent.grid_columnconfigure(column, weight=1)
        tk.Label(box, text=label, bg="white", fg="#666",
                 font=("Microsoft YaHei UI", 9)).pack(anchor="w", padx=12, pady=(10, 2))
        ttk.Entry(box, textvariable=variable, font=("Microsoft YaHei UI", 16),
                  justify="center").pack(fill="x", padx=10, pady=(0, 11))

    def next_step(self):
        if self.stage == 0:
            self.stage = 1
            try:
                start = datetime.strptime(self.start_var.get().strip(), "%H:%M")
                hours = float(self.hours_var.get().strip())
                finish = start + timedelta(hours=hours + 1)
                result = finish.strftime("%H:%M")
            except ValueError:
                result = "18:00"
            self.write_log(
                "> 正在读取考勤记录……\n"
                "> 工作时长计算完成。\n"
                "> 暂未发现必须加班的理由。"
            )
            self.result.config(text=result, fg="#16823b")
            self.status.config(text="恭喜，理论上可以下班", fg="#16823b")
            self.button.config(text="立即下班")

        elif self.stage == 1:
            self.stage = 2
            self.button.config(state="disabled", text="正在提交下班申请……")
            self.result.config(text="审核中", fg="#d07a00")
            self.write_log("> 已收到员工下班请求……")
            self.dialog_index = 0
            self.show_reply_dialog()

    def show_reply_dialog(self):
        replies = [
            ("下班申请回复", "下什么班？"),
            ("程序通知", "我先下班了。"),
            ("关机申请", "电脑也要下班，\n你自己上班吧。"),
        ]
        if self.dialog_index >= len(replies):
            self.fake_shutdown()
            return

        title, message = replies[self.dialog_index]
        self.root.bell()
        self.dialog = tk.Toplevel(self.root)
        self.dialog.title(title)
        self.dialog.geometry("430x220")
        self.dialog.resizable(False, False)
        self.dialog.transient(self.root)
        self.dialog.grab_set()
        self.dialog.protocol("WM_DELETE_WINDOW", self.next_reply)

        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 430) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 220) // 2
        self.dialog.geometry(f"430x220+{x}+{y}")

        panel = tk.Frame(self.dialog, bg="#f6f6f6")
        panel.pack(fill="both", expand=True)
        icon = tk.Label(panel, text="!", bg="#1672c7", fg="white",
                        font=("Segoe UI", 24, "bold"), width=2, height=1)
        icon.place(x=30, y=48)
        tk.Label(panel, text=message, bg="#f6f6f6", fg="#111",
                 font=("Microsoft YaHei UI", 20, "bold"), justify="left").place(x=105, y=43)
        bottom = tk.Frame(panel, bg="#e9e9e9", height=62)
        bottom.pack(side="bottom", fill="x")
        ttk.Button(bottom, text="确定", command=self.next_reply).pack(side="right", padx=22, pady=14, ipadx=25)
        self.dialog.bind("<Return>", lambda _event: self.next_reply())

    def next_reply(self):
        if self.dialog and self.dialog.winfo_exists():
            self.dialog.grab_release()
            self.dialog.destroy()
        self.dialog_index += 1
        self.show_reply_dialog()

    def fake_shutdown(self):
        self.result.config(text="程序已下班", fg="#c40000")
        self.status.config(text="电脑正在关机……", fg="#c40000")
        self.root.after(350, self.show_shutdown_screen)

    def show_shutdown_screen(self):
        self.blackout = tk.Toplevel(self.root)
        self.blackout.configure(bg="#0067b8")
        self.blackout.attributes("-fullscreen", True)
        self.blackout.attributes("-topmost", True)
        self.blackout.bind("<Escape>", lambda _event: self.exit_program())

        center = tk.Frame(self.blackout, bg="#0067b8")
        center.place(relx=.5, rely=.5, anchor="center")
        self.spinner = tk.Canvas(center, width=70, height=70, bg="#0067b8",
                                 highlightthickness=0)
        self.spinner.pack()
        tk.Label(center, text="正在关机", bg="#0067b8", fg="white",
                 font=("Microsoft YaHei UI", 25)).pack(pady=(14, 0))
        tk.Label(self.blackout, text="  ", bg="#0067b8", fg="#8fc5ea",
                 font=("Microsoft YaHei UI", 9)).place(relx=.5, rely=.94, anchor="center")
        self.animate_spinner()

    def animate_spinner(self):
        if not self.blackout or not self.blackout.winfo_exists():
            return
        self.spinner.delete("all")
        cx, cy, radius = 35, 35, 23
        for index in range(8):
            angle = (self.shutdown_angle + index * 45) % 360
            import math
            radians = math.radians(angle)
            x = cx + math.cos(radians) * radius
            y = cy + math.sin(radians) * radius
            shade = 80 + index * 20
            shade = min(shade, 255)
            color = f"#{shade:02x}{shade:02x}{shade:02x}"
            self.spinner.create_oval(x-3, y-3, x+3, y+3, fill=color, outline="")
        self.shutdown_angle = (self.shutdown_angle + 22) % 360
        self.jobs.append(self.blackout.after(70, self.animate_spinner))

    def write_log(self, value):
        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        self.log.insert("end", value)
        self.log.see("end")
        self.log.config(state="disabled")

    def append_log(self, value):
        self.log.config(state="normal")
        self.log.insert("end", "\n" + value)
        self.log.see("end")
        self.log.config(state="disabled")
        self.root.bell()

    def close_window(self):
        self.append_log("> 程序拒绝关闭：还没到下班时间。")

    def exit_program(self):
        for job in self.jobs:
            try:
                self.root.after_cancel(job)
            except tk.TclError:
                pass
        self.root.destroy()


if __name__ == "__main__":
    app_root = tk.Tk()
    OffWorkCalculator(app_root)
    app_root.mainloop()
