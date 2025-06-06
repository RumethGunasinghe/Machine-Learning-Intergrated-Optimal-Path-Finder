import tkinter as tk
from tkinter import ttk
from tkinterweb import HtmlFrame
import os

map_file = os.path.abspath("map.html")

def load_map(frame, map_path):
    # This method loads the map into the given HtmlFrame
    frame.load_file(map_path)

def show_gui():
    def on_predict():
        input_values = {
            "algorithm": algo_var.get(),
            "model": int(model_var.get()),
            "origin": origin_var.get(),
            "destination": dest_var.get(),
            "time": time_var.get()
        }
        print(input_values)  # Or do something with inputs

    root = tk.Tk()
    root.title("Route Predictor")

    # Variables
    algo_var = tk.StringVar(value="A*")
    model_var = tk.StringVar(value=1)
    origin_var = tk.StringVar(value=971)
    dest_var = tk.StringVar(value=2000)
    time_var = tk.StringVar(value="Morning")

    # Input Frame
    input_frame = ttk.Frame(root)
    input_frame.pack(pady=10)

    ttk.Label(input_frame, text="Search Algorithm").grid(row=0, column=0)
    ttk.Combobox(input_frame, textvariable=algo_var, values=["AStar", "Dijkstra"]).grid(row=0, column=1)

    ttk.Label(input_frame, text="Data Model").grid(row=1, column=0)
    ttk.Combobox(input_frame, textvariable=model_var, values=["1", "2"]).grid(row=1, column=1)

    ttk.Label(input_frame, text="Origin").grid(row=2, column=0)
    ttk.Entry(input_frame, textvariable=origin_var).grid(row=2, column=1)

    ttk.Label(input_frame, text="Destination").grid(row=3, column=0)
    ttk.Entry(input_frame, textvariable=dest_var).grid(row=3, column=1)

    ttk.Label(input_frame, text="Time of Day").grid(row=4, column=0)
    ttk.Combobox(input_frame, textvariable=time_var, values=["Morning", "Night"]).grid(row=4, column=1)

    ttk.Button(input_frame, text="Predict", command=on_predict).grid(row=5, columnspan=2, pady=5)

    # Map Frame - create it but don't load the map yet
    map_frame = HtmlFrame(root, horizontal_scrollbar="auto")
    map_frame.pack(fill="both", expand=True)

    # Call the map loading function *after* GUI is setup
    root.after(100, lambda: load_map(map_frame, map_file))

    root.mainloop()


