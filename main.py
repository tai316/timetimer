import tkinter as tk
from math import pi, cos, sin

class TimeTimerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Time Timer")

        self.canvas = tk.Canvas(master, width=400, height=400)
        self.canvas.pack()

        # 入力フィールドとラベルの追加
        self.label = tk.Label(master, text="0~60の値を入力してください。:")
        self.label.pack()
        
        self.entry = tk.Entry(master)
        self.entry.pack()

        self.set_btn = tk.Button(master, text="タイマーをセットする", command=self.set_time)
        self.set_btn.pack(side=tk.LEFT)

        self.start_btn = tk.Button(master, text="Start", command=self.start_timer)
        self.start_btn.pack(side=tk.LEFT)

        self.stop_btn = tk.Button(master, text="Stop", command=self.stop_timer)
        self.stop_btn.pack(side=tk.RIGHT)

        self.running = False
        self.remaining_time = 0  # 初期時間は0
        self.total_time = 60 * 60  # 全体の時間を60分と設定

    def set_time(self):
        # 入力された時間を取得しタイマーを設定
        minutes = self.entry.get()
        if minutes.isdigit():
            minutes = int(minutes)
            if 0 <= minutes <= 60:
                self.remaining_time = minutes * 60  # 分を秒に変換
                self.total_time = 60 * 60  # 全体の時間を常に60分に設定
                self.draw_timer()  # タイマー表示を更新
            else:
                print("Please enter a number between 0 and 60.")
        else:
            print("Please enter a valid number.")

    def draw_clock_marks(self):
        x_center, y_center = 200, 200
        radius = 150
        for i in range(12):  # 0から60まで5分ごとに13のメモリ
            angle = (i / 12) * 360 - 90  # 12時の位置からスタート
            radians = angle * pi / 180
            x_inner = x_center + (radius - 10) * cos(radians)
            y_inner = y_center + (radius - 10) * sin(radians)
            x_outer = x_center + radius * cos(radians)
            y_outer = y_center + radius * sin(radians)
            self.canvas.create_line(x_inner, y_inner, x_outer, y_outer, width=2)
            # 数字を配置
            x_text = x_center + (radius + 20) * cos(radians)
            y_text = y_center + (radius + 20) * sin(radians)
            self.canvas.create_text(x_text, y_text, text=str(i * 5), font=("Helvetica", 30))

    def draw_timer(self):
        self.canvas.delete("all")
        x0, y0, x1, y1 = 50, 50, 350, 350
        self.canvas.create_oval(x0, y0, x1, y1, fill="white")
        self.draw_clock_marks()

        angle = (self.remaining_time / self.total_time) * 360 if self.total_time > 0 else 0
        if angle > 0:
            self.canvas.create_arc(x0, y0, x1, y1, start=90, extent=-angle, fill="red")
        self.canvas.create_text(200, 200, text=f"{int(self.remaining_time // 60):02d}:{int(self.remaining_time % 60):02d}", font=("Helvetica", 50))

    def update_timer(self):
        if self.remaining_time > 0 and self.running:
            self.remaining_time -= 1
            self.draw_timer()
            self.master.after(1000, self.update_timer)
        elif self.remaining_time == 0 and self.running:
            self.draw_timer()  # 最後にタイマーを更新して0を表示
            print("Timer finished!")
            self.running = False

    def start_timer(self):
        if not self.running and self.remaining_time > 0:
            self.running = True
            self.update_timer()

    def stop_timer(self):
        self.running = False

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTimerApp(root)
    root.mainloop()
