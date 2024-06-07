import tkinter as tk
from math import pi, cos, sin

class TimeTimerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Time Timer")

        self.canvas = tk.Canvas(master, width=400, height=400)
        self.canvas.pack()

        self.start_btn = tk.Button(master, text="Start", command=self.start_timer)
        self.start_btn.pack(side=tk.LEFT)

        self.stop_btn = tk.Button(master, text="Stop", command=self.stop_timer)
        self.stop_btn.pack(side=tk.RIGHT)

        self.running = False  # タイマーの状態を追跡するフラグ
        self.remaining_time = 10 * 60  # 残り時間（秒）
        self.total_time = self.remaining_time  # 総時間（秒）

    def draw_timer(self):
        angle = (self.remaining_time / self.total_time) * 360
        self.canvas.delete("all")
        x0, y0, x1, y1 = 50, 50, 350, 350
        self.canvas.create_oval(x0, y0, x1, y1, fill="white")
        if angle > 0:
            radians = (angle - 90) * pi / 180
            x = 200 + 150 * cos(radians)
            y = 200 + 150 * sin(radians)
            self.canvas.create_arc(x0, y0, x1, y1, start=-90, extent=angle, fill="red")
        self.canvas.create_text(200, 200, text=f"{int(self.remaining_time // 60)}:{int(self.remaining_time % 60):02d}", font=("Helvetica", 24))

    def update_timer(self):
        if self.remaining_time > 0 and self.running:
            self.remaining_time -= 1
            self.draw_timer()
            self.master.after(1000, self.update_timer)
        elif self.remaining_time == 0:
            self.draw_timer()  # 最後にタイマーを更新して0を表示
            print("Timer finished!")

    def start_timer(self):
        if not self.running:
            self.running = True
            self.update_timer()

    def stop_timer(self):
        self.running = False

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTimerApp(root)
    root.mainloop()
