import tkinter as tk
from . import state

class ChanSecurityGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ChanSecurity V1")
        self.root.geometry("800x600")
        self.root.configure(bg="#121212")

        self.current_view = "CPU"

        self.top_frame = tk.Frame(root, bg="#121212")
        self.top_frame.pack(pady=20, fill="x", padx=40)

        self.card_cpu = tk.Button(self.top_frame, text="CPU\n\n[ Mini Grafik ]", font=("Arial", 11, "bold"), bg="#1e1e1e", fg="white", bd=1, relief="solid", width=20, height=5, command=lambda: self.switch_view("CPU"))
        self.card_cpu.pack(side="left", expand=True, padx=10)

        self.card_ram = tk.Button(self.top_frame, text="RAM\n\n[ Mini Grafik]", font=("Arial", 11, "bold"), bg="#1e1e1e", fg="white", bd=1, relief="solid", width=20, height=5, command=lambda: self.switch_view("RAM"))
        self.card_ram.pack(side="left", expand=True, padx=10)

        self.card_net = tk.Button(self.top_frame, text="NETWORK\n\n[ Mini Grafik ]", font=("Arial", 11, "bold"), bg="#1e1e1e", fg="white", bd=1, relief="solid", width=20, height=5, command=lambda: self.switch_view("NETWORK"))
        self.card_net.pack(side="left", expand=True, padx=10)

        self.time_label = tk.Label(root, text="Waktu", font=("Arial", 10), bg="#121212", fg="#777777")
        self.time_label.pack(pady=5)

        self.bottom_frame = tk.Frame(root, bg="#1e1e1e", bd=1, relief="solid")
        self.bottom_frame.pack(pady=10, fill="both", expand=True, padx=30)

        self.main_title = tk.Label(self.bottom_frame, text="GRAFIK CPU", font=("Arial", 14, "bold"), bg="#1e1e11", fg="#deff9a")
        self.main_title.pack(pady=10)

        self.main_canvas = tk.Canvas(self.bottom_frame, width=700, height=250, bg="#151515", highlightthickness=0)
        self.main_canvas.pack(pady=10)

        self.poll_state()

    def switch_view(self, view_name):
        self.current_view = view_name
        self.main_title.config(text=f"GRAFIK DETAIL {view_name}")
        for card, name in [(self.card_cpu, "CPU"), (self.card_ram, "RAM"), (self.card_net, "NETWORK")]:
            card.config(bg="#2d2d2d" if name == view_name else "#1e1e1e",
                        fg="#deff9a" if name == view_name else "white")

    def poll_state(self):
        data = state.read_state()
        if data is None:
            self.time_label.config(text="Menunggu daemon...")
        else:
            self.card_cpu.config(text=f"CPU\n{data['cpu']}%")
            self.card_ram.config(text=f"RAM\n{data['ram']}%")
            self.card_net.config(text=f"NETWORK\n{data['net']}%")
            self.time_label.config(text=f"Last Check: {data['timestamp']}")
            self.draw_main_chart(data["history"][self.current_view])

        self.root.after(1000, self.poll_state)

    def draw_main_chart(self, active_history):
        self.main_canvas.delete("all")
        canvas_height = 250
        bar_width = 25
        gap = 8
        start_x = 30

        for i, val in enumerate(active_history):
            x1 = start_x + i * (bar_width + gap)
            x2 = x1 + bar_width
            bar_height = (val / 100) * 200
            y1 = canvas_height - bar_height - 20
            y2 = canvas_height - 20

            color = "#deff9a"
            if self.current_view == "CPU" and val > 80:
                color = "#ff4d4d"
            elif self.current_view == "RAM" and val > 85:
                color = "#ffaa00"
            self.main_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

            if i == len(active_history) - 1:
                self.main_canvas.create_text(x1 + 12, y1 - 10, text=f"{int(val)}%", fill="white", font=("Arial", 8))

def launch():
    root = tk.Tk()
    app = ChanSecurityGUI(root)
    app.switch_view("CPU")
    root.mainloop()
