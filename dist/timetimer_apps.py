import tkinter as tk
from math import pi, cos, sin

class TimeTimerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Time Timer")

        self.canvas = tk.Canvas(master)
        self.canvas.pack(fill=tk.BOTH, expand=True)  # Canvasをウィンドウ全体に拡張

        # 入力フィールド、ラベル、ボタンを格納するフレームの追加
        control_frame = tk.Frame(master)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        time_frame = tk.Frame(control_frame)
        time_frame.pack(side=tk.LEFT, padx=5, pady=5)

        font_frame = tk.Frame(control_frame)
        font_frame.pack(side=tk.LEFT, padx=5, pady=5)

        # Set Time 関連のウィジェット
        self.label = tk.Label(time_frame, text="数字を入力してください(0~60):")
        self.label.pack(side=tk.TOP)

        self.entry = tk.Entry(time_frame)
        self.entry.pack(side=tk.TOP)

        self.set_time_btn = tk.Button(time_frame, text="Set Time", command=self.set_time)
        self.set_time_btn.pack(side=tk.TOP)

        # Set Font Size 関連のウィジェット
        self.font_label = tk.Label(font_frame, text="フォントサイズを入力してください(8以上):")
        self.font_label.pack(side=tk.TOP)

        self.font_size_entry = tk.Entry(font_frame)
        self.font_size_entry.pack(side=tk.TOP)

        self.set_font_btn = tk.Button(font_frame, text="Set Font Size", command=self.set_font_size)
        self.set_font_btn.pack(side=tk.TOP)

        # Start and Stop Buttons
        self.start_btn = tk.Button(master, text="Start", command=self.start_timer, bg='green', activebackground='light green')
        self.start_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.stop_btn = tk.Button(master, text="Stop", command=self.stop_timer, bg='red', activebackground='dark red')
        self.stop_btn.pack(side=tk.RIGHT, padx=5, pady=5)

        self.running = False
        self.remaining_time = 0  # 初期時間は0
        self.total_time = 60 * 60  # 全体の時間を60分と設定
        self.font_size = 12  # 初期フォントサイズ

        self.canvas.bind("<Configure>", self.on_resize)  # ウィンドウサイズ変更イベント

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
            print("Please enter a valid number for time.")

    def set_font_size(self):
        # 入力されたフォントサイズを取得し設定
        font_size = self.font_size_entry.get()
        if font_size.isdigit():
            font_size = max(int(font_size), 8)  # フォントサイズの最小値を8に設定
            self.font_size = font_size
            self.draw_timer()  # タイマー表示を更新
        else:
            print("Please enter a valid number for font size.")

    def on_resize(self, event):
        # ウィンドウサイズが変更された時にタイマーを再描画
        self.draw_timer()

    def draw_clock_marks(self, x_center, y_center, radius):
        # 1分ごとの小さなメモリと5分ごとのメモリを描画
        for i in range(60):
            angle = (i / 60) * 360 - 90
            radians = angle * pi / 180
            x_inner = x_center + (radius - (20 if i % 5 == 0 else 10)) * cos(radians)
            y_inner = y_center + (radius - (20 if i % 5 == 0 else 10)) * sin(radians)
            x_outer = x_center + radius * cos(radians)
            y_outer = y_center + radius * sin(radians)
            self.canvas.create_line(x_inner, y_inner, x_outer, y_outer, width=2 if i % 5 == 0 else 1)
            if i % 5 == 0:
                # 数字を配置
                x_text = x_center + (radius + 30) * cos(radians)
                y_text = y_center + (radius + 30) * sin(radians)
                self.canvas.create_text(x_text, y_text, text=str(i), font=("Helvetica", self.font_size))  # ユーザーが設定したフォントサイズを使用

    def draw_timer(self):
        # キャンバスの現在のサイズを取得
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        radius = min(width, height) / 2 * 0.85
        x_center = width / 2
        y_center = height / 2
        x0, y0, x1, y1 = x_center - radius, y_center - radius, x_center + radius, y_center + radius
        
        self.canvas.delete("all")
        self.canvas.create_oval(x0, y0, x1, y1, fill="white")
        self.draw_clock_marks(x_center, y_center, radius)

        angle = (self.remaining_time / self.total_time) * 360 if self.total_time > 0 else 0
        if angle > 0:
            self.canvas.create_arc(x0, y0, x1, y1, start=90, extent=-angle, fill="red")
        self.canvas.create_text(x_center, y_center, text=f"{int(self.remaining_time // 60):02d}:{int(self.remaining_time % 60):02d}", font=("Helvetica", self.font_size))

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
