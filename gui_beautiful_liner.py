import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'controller'))
from controller import Controller

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import time

class GuiBeautifulLiner:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Beautiful Liner")

        self.entries = []

        self.current_row = 0
        self.current_culumn = 0
    
        self.controller = Controller()
    #end

    def add_scale(self, label_text, scale_from, scale_to, scale_resolution, scale_default):
        label = tk.Label(self.window, text=label_text)
        label.grid(row=self.current_row, column=0, padx=10, pady=10)

        scale = tk.Scale(self.window, from_=scale_from, to=scale_to, resolution=scale_resolution, orient=tk.HORIZONTAL, length=400)
        scale.grid(row=self.current_row, column=1, padx=10, pady=10)
        scale.set(scale_default)
        self.entries.append(scale)

        self.current_row += 1
    #end


    def __select_file(self):
        initial_dir = os.getcwd()
        file_types = [("SVG Files", "*.svg")]
        return filedialog.askopenfilename(initialdir=initial_dir, filetypes=file_types)
    #end

    def add_file_select_button(self, button_text):
        button = tk.Button(self.window, text=button_text, command=lambda: entry.insert(tk.END, self.__select_file()))
        button.grid(row=self.current_row, column=0, padx=10, pady=10)

        entry = tk.Entry(self.window, width=100)
        entry.grid(row=self.current_row, column=1, padx=10, pady=10)
        self.entries.append(entry)

        self.current_row += 1
    #end

    def do_something(self, pb):
        sum = 0
        for i in range(1, 10):
            sum += i
            pb.configure(value=i)
            pb.update()
            self.log_text.insert(tk.END, f"{i+1}\n")
            self.log_text.see(tk.END)
            time.sleep(0.1)
        print("The sum is", sum)


    def execute(self):
        #reading_file_path         = str( self.entries[0].get() )
        reading_file_path         = f"C:/Users/taichi-kodama/BeautifulLiner/Futago.svg"
        linear_approximate_length = float( self.entries[1].get() )
        delete_ratio              = float( self.entries[2].get() )
        broad_width               = float( self.entries[3].get() )

        if not os.path.exists(reading_file_path):
            self.log_text.insert(tk.END, f"File not found\n")
            self.log_text.see(tk.END)
        else:
            self.log_text.delete(1.0, tk.END)

            self.execute_button.config(state=tk.DISABLED)
            #self.do_something(self.progress_bar)
            self.controller.run("GUI", reading_file_path, linear_approximate_length, delete_ratio, broad_width, self.progress_bar, self.log_text)
            self.execute_button.config(state=tk.NORMAL)

            self.progress_bar["value"] = 0
            self.progress_bar.update()
            self.log_text.insert(tk.END, "Create " + reading_file_path.replace(".svg", "_BeauL.svg") + "\n" )
            self.log_text.insert(tk.END, "END OF JOB\n")
            self.log_text.see(tk.END)
        #end
    #end

    def add_execute_button(self, button_text):
        self.execute_button = tk.Button(self.window, text=button_text, command=lambda: self.execute())
        self.execute_button.grid(row=self.current_row, column=0, columnspan=2, padx=10, pady=10)
        self.current_row += 1
    #end

    def add_progress_bar(self):
        self.progress_bar = ttk.Progressbar(self.window, length=200, mode="determinate", maximum=100)
        self.progress_bar.grid(row=self.current_row, column=0, padx=10, pady=10)

        self.log_text = tk.Text(self.window, height=10)
        self.log_text.grid(row=self.current_row, column=1, padx=10, pady=10)
        self.current_row += 1
    #end

    def mainloop(self):
        self.window.mainloop()
    #end
#end

gui = GuiBeautifulLiner()

gui.add_file_select_button(button_text="ファイル選択")
gui.add_scale(label_text="xxx",             scale_from=0.01, scale_to=1.0, scale_resolution=0.01, scale_default=0.1)
gui.add_scale(label_text="param",           scale_from=0.0,  scale_to=0.5, scale_resolution=0.01, scale_default=0.25)
gui.add_scale(label_text="paramparamparam", scale_from=0.1,  scale_to=5.0, scale_resolution=0.1,  scale_default=1.0)
gui.add_execute_button(button_text="exe")
gui.add_progress_bar()

gui.mainloop()

