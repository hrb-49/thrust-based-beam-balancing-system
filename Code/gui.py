import tkinter as tk
from tkinter import ttk
import serial
import threading
import re
from collections import deque

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# ================= SERIAL CONFIG =================
PORT = "COM3"
BAUD = 9600
ser = serial.Serial(PORT, BAUD, timeout=1)

# ================= REGEX PARSER ==================
pattern = re.compile(
    r"RPM1:(\d+)\s+RPM2:(\d+).*?"
    r"I1:([-\d.]+)\s+I2:([-\d.]+).*?"
    r"Roll:([-\d.]+)"
)

# ================= DATA BUFFERS ==================
MAX_POINTS = 120
rpm1_data = deque(maxlen=MAX_POINTS)
rpm2_data = deque(maxlen=MAX_POINTS)
i1_data   = deque(maxlen=MAX_POINTS)
i2_data   = deque(maxlen=MAX_POINTS)

# ================= GUI COLORS ====================
BG      = "#121212"
CARD    = "#1e1e1e"
ACCENT  = "#00ffd5"
TEXT    = "#ffffff"
GRID    = "#2f2f2f"

# ================= ROOT ==========================
root = tk.Tk()
root.title("TM4C123 Beam Balancing Dashboard")
root.geometry("1000x620")
root.configure(bg=BG)

# ================= HEADER ========================
header = tk.Label(
    root, text="TM4C123 Beam Balancing Telemetry",
    fg=ACCENT, bg=BG,
    font=("Segoe UI", 20, "bold")
)
header.pack(pady=10)

# ================= ROLL CARD =====================
roll_card = tk.Frame(root, bg=CARD, bd=0)
roll_card.pack(pady=10, padx=20, fill="x")

tk.Label(
    roll_card, text="ROLL ANGLE",
    fg="#aaaaaa", bg=CARD,
    font=("Segoe UI", 12)
).pack(pady=(10, 0))

roll_value = tk.Label(
    roll_card, text="0.0°",
    fg=ACCENT, bg=CARD,
    font=("Consolas", 40, "bold")
)
roll_value.pack(pady=(0, 10))

# ================= PLOTS =========================
fig = Figure(figsize=(9.5, 4), dpi=100)
fig.patch.set_facecolor(BG)

ax_rpm = fig.add_subplot(121)
ax_cur = fig.add_subplot(122)

for ax in (ax_rpm, ax_cur):
    ax.set_facecolor(CARD)
    ax.grid(True, color=GRID)
    ax.tick_params(colors=TEXT)
    ax.xaxis.label.set_color(TEXT)
    ax.yaxis.label.set_color(TEXT)
    ax.title.set_color(TEXT)

# RPM plot
rpm1_line, = ax_rpm.plot([], [], color="#00ffd5", label="Motor 1")
rpm2_line, = ax_rpm.plot([], [], color="#ff9f43", label="Motor 2")
ax_rpm.set_title("Motor RPM")
ax_rpm.set_xlabel("Samples")
ax_rpm.set_ylabel("RPM")
ax_rpm.legend(facecolor=CARD, edgecolor=GRID, labelcolor=TEXT)

# Current plot
i1_line, = ax_cur.plot([], [], color="#54a0ff", label="Motor 1")
i2_line, = ax_cur.plot([], [], color="#ee5253", label="Motor 2")
ax_cur.set_title("Motor Current")
ax_cur.set_xlabel("Samples")
ax_cur.set_ylabel("Current (A)")
ax_cur.legend(facecolor=CARD, edgecolor=GRID, labelcolor=TEXT)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

# ================= UPDATE PLOTS ==================
def update_plots():
    rpm1_line.set_data(range(len(rpm1_data)), rpm1_data)
    rpm2_line.set_data(range(len(rpm2_data)), rpm2_data)
    i1_line.set_data(range(len(i1_data)), i1_data)
    i2_line.set_data(range(len(i2_data)), i2_data)

    ax_rpm.relim()
    ax_rpm.autoscale_view()

    ax_cur.relim()
    ax_cur.autoscale_view()

    canvas.draw_idle()
    root.after(100, update_plots)

# ================= SERIAL THREAD =================
def read_serial():
    while True:
        try:
            line = ser.readline().decode(errors="ignore").strip()
            match = pattern.search(line)
            if match:
                rpm1, rpm2, i1, i2, roll = match.groups()

                rpm1_data.append(int(rpm1))
                rpm2_data.append(int(rpm2))
                i1_data.append(float(i1))
                i2_data.append(float(i2))

                roll_value.config(text=f"{float(roll):.1f}°")

        except Exception:
            roll_value.config(text="DISCONNECTED")
            break

# ================= START =========================
threading.Thread(target=read_serial, daemon=True).start()
update_plots()
root.mainloop()
