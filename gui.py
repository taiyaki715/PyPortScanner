import tkinter as tk
from tkinter import LEFT
import tkinter.ttk as ttk

import scanner


class Window:
    def __init__(self):
        self.init_elements()

    def init_elements(self):
        self.root = tk.Tk()

        # First Row
        self.frame_1 = ttk.Frame(self.root)
        self.frame_1.pack(pady=5)
        self.label_target = ttk.Label(self.frame_1, text="Target")
        self.label_target.pack(padx=5, side=LEFT)
        self.entry_target = ttk.Entry(self.frame_1)
        self.entry_target.pack(side=LEFT)

        # Second Row
        self.frame_2 = ttk.Frame(self.root)
        self.frame_2.pack(pady=5)
        self.label_start = ttk.Label(self.frame_1, text="Min Port")
        self.label_start.pack(padx=5, side=LEFT)
        self.entry_start = ttk.Entry(self.frame_1, width=5)
        self.entry_start.pack(side=LEFT)
        self.label_end = ttk.Label(self.frame_1, text="Max Port")
        self.label_end.pack(padx=5, side=LEFT)
        self.entry_end = ttk.Entry(self.frame_1, width=5)
        self.entry_end.pack(side=LEFT)

        # Third Row
        self.frame_3 = ttk.Frame(self.root)
        self.frame_3.pack(pady=5)
        self.execute_button = ttk.Button(self.frame_3, text="Execute", command=run_scan)
        self.execute_button.pack(side=LEFT)

        # Result Area
        self.table_result = ttk.Treeview(self.root)
        self.table_result["columns"] = (1, 2, 3)
        self.table_result["show"] = "headings"
        self.table_result.heading(1, text="Protocol")
        self.table_result.heading(2, text="Port")
        self.table_result.heading(3, text="Status")
        self.table_result.pack()

    def show(self):
        self.entry_start.mainloop()

    def show_data(self, result_list):
        for result in result_list:
            if result.state == "UP":
                self.table_result.insert("", "end", values=(result.protocol, result.port_no, result.state))


def run_scan():
    s = scanner.Scanner(w.entry_target.get(), int(w.entry_start.get()), int(w.entry_end.get()))
    res = s.run()
    w.show_data(res)


if __name__ == "__main__":
    w = Window()
    w.show()
