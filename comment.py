#https://github.com/qpit/thorlabs_apt/blob/master/thorlabs_apt/core.py
import thorlabs_apt as apt
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import time
import threading

# Serial number for your specific Thorlabs motor
serial_number = 83839619

# Initialise the motor with the given serial number
motor = apt.Motor(serial_number)

# Function to run the motor control functions in a separate thread
def run_in_thread(target):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=target, args=args, kwargs=kwargs)
        thread.start()
    return wrapper

# Function to stop the motor in a controlled manner
@run_in_thread
def end():
    motor.stop_profiled()

# Function to move the motor to a specific position entered by the user
@run_in_thread
def print_value():
    value = float(entry_field.get())
    motor.move_to(value, blocking=True)

# Function to get the current position of the motor
def current():
    return motor.position

@run_in_thread
def speedf():
    v = float(speed.get())
    a = float(acc.get())
    motor.set_velocity_parameters(0, a, v)
    print("v and a set   ")
    print(motor.get_velocity_parameters())

# Function to move the motor to its home/initial position
@run_in_thread
def home():
    motor.move_home(True)

@run_in_thread
def scan():
    clock = float(clocks_entry.get())
    moves = int(moves_entry.get())
    dist = float(distance_entry.get())
    scanning_command(motor, dist, moves, clock)

@run_in_thread
def moveby():
    m = float(jog.get())
    motor.move_by(m, blocking=True)

@run_in_thread
def scanning_command(motor, dist, moves, clock):
    dist = dist / moves
    delay_event = threading.Event()

    def non_blocking_delay():
        for _ in range(moves):
            time.sleep(clock)
            delay_event.set()
            delay_event.clear()

    delay_thread = threading.Thread(target=non_blocking_delay)
    delay_thread.start()

    for _ in range(moves):
        motor.move_by(dist)
        delay_event.wait()

    delay_thread.join()

def update_data():
    data.set(round(current(), 5))  # current is the angle and then round puts it to 5s.f
    root.after(1, update_data)

root = ThemedTk(theme="radiance")
root.geometry("1920x1080")


data = tk.StringVar()

# Current Position Label
label = ttk.Label(root, textvariable=data)
label.grid(row=0, column=0, columnspan=7)

# Move To Function
move_to_label = ttk.Label(root, text="Move To Position")
move_to_label.grid(row=2, column=0)
entry_field = ttk.Entry(root)
entry_field.grid(row=2, column=2, columnspan=2)
print_button = ttk.Button(root, text='Move to', command=print_value)
print_button.grid(row=2, column=5)

# Move By Function
move_by_label = ttk.Label(root, text="Move By Distance")
move_by_label.grid(row=4, column=0)
jog = ttk.Entry(root)
jog.grid(row=4, column=2, columnspan=2)
moveb = ttk.Button(root, text="Move By", command=moveby)
moveb.grid(row=4, column=5)

# Speed Function
speed_label = ttk.Label(root, text="Speed Value")
speed_label.grid(row=6, column=0)
speed = ttk.Entry(root)
speed.grid(row=8, column=2, columnspan=2)
speedb = ttk.Button(root, text="Set Speed", command=speedf)
speedb.grid(row=8, column=5)

# Acceleration Function
acc_label = ttk.Label(root, text="Acceleration Value")
acc_label.grid(row=10, column=0)
acc = ttk.Entry(root)
acc.grid(row=10, column=2, columnspan=2)

# Scan Function
scan_label = ttk.Label(root, text="Scan Settings,Time, T dist,  rotations")
scan_label.grid(row=20, column=0)
clocks_entry = ttk.Entry(root)
clocks_entry.grid(row=22, column=2, columnspan=2)
distance_entry = ttk.Entry(root)
distance_entry.grid(row=24, column=2, columnspan=2)
moves_entry = ttk.Entry(root)
moves_entry.grid(row=25, column=2, columnspan=2)
test = ttk.Button(root,text="Scan", command=scan)
test.grid(row=20, column=5, rowspan=3)

# Stop Button
end_b = ttk.Button(root,text="End",command=end)
end_b.grid(row=26, column=2)

# Home Button
home_b = ttk.Button(root, text="Home", command=home)
home_b.grid(row=14, column=5)

update_data()

root.mainloop()
# for accerlation and vecolicity you have to plug in both v and a 

#max is 25 acceleration is the bottom one