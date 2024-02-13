import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'controller'))
from controller import Controller

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import time

import json



class GuiBeautifulLiner:
    ENGLISH_INDEX = 0
    JAPANESE_INDEX = 1

    MENU_BAR_LABEL     = ["Language",          "言語"]
    FILE_SELECT_BUTTON = ["Choose svg file",   "ファイル"]
    LINEALIZE_PARAM    = ["linearize param",   "線形化近似の最小長さ"]
    DELETE_EDGE_RATIO  = ["delete edge ratio", "端部除去率"]
    BROAD_WIDTH        = ["broaden width",     "幅広化処理時の幅"]
    EXECUTE_BUTTON     = ["execute",           "実行"]

    def __create_main_window(self):
        self.window = tk.Tk()
        self.window.title("Beautiful Liner")

        self.entries = []

        self.current_row = 0
        self.current_culumn = 0
    
        self.controller = Controller()
        self.scale_index = 0
        self.scale_labels = []
        self.scales = []

        self.__add_file_select_button()
        self.__add_scale(label_text="linearize param", scale_from=0.01, scale_to=1.0, scale_resolution=0.01, scale_default=0.1)
        self.__add_scale(label_text="delete edge ratio",           scale_from=0.0,  scale_to=0.5, scale_resolution=0.01, scale_default=0.25)
        self.__add_scale(label_text="broad witdh", scale_from=0.1,  scale_to=5.0, scale_resolution=0.1,  scale_default=1.0)
        self.__add_execute_button(button_text="exece")
        self.__add_progress_bar()
        self.__add_menu_bar()
    #end

    def __create_init_setting_window(self):
        self.init_setting = tk.Tk()
        self.language_var = tk.StringVar(value="English")  # Default language

        self.label = tk.Label(self.init_setting, text="Select a language:")
        self.label.pack()

        self.english_button = tk.Radiobutton(self.init_setting, text="English", variable=self.language_var, value="English")
        self.english_button.pack()

        self.japanese_button = tk.Radiobutton(self.init_setting, text="日本語", variable=self.language_var, value="Japanese")
        self.japanese_button.pack()

        self.save_button = tk.Button(self.init_setting, text="OK", command=self.__save_language)
        self.save_button.pack()
    #end

    def __save_language(self):
        # Save selected language to a JSON file
        language_data = {"language": self.language_var.get()}
        with open("language_settings.json", "w") as json_file:
            json.dump(language_data, json_file)

        self.__create_main_window()

        if self.language_var.get() == "Japanese":
            self.__update_language(self.JAPANESE_INDEX)
        else: # English or ohter unknown settings
            self.__update_language(self.ENGLISH_INDEX)
        #end
        self.init_setting.destroy()

        self.window.mainloop()
    #end


    def __update_language(self, index):
#        self.menu_bar["label"]       = self.MENU_BAR_LABEL[index]j
        self.scale_labels[0].config(text=self.LINEALIZE_PARAM[index])
        self.file_select_button.config(text=self.FILE_SELECT_BUTTON[index])
        self.scale_labels[1].config(text=self.DELETE_EDGE_RATIO[index])
        self.scale_labels[2].config(text=self.BROAD_WIDTH[index])
        self.execute_button.config(text=self.EXECUTE_BUTTON[index])
    #end

    def __set_language_japanese(self):
        self.__update_language(self.JAPANESE_INDEX)
    #end
    def __set_language_english(self):
        self.__update_language(self.ENGLISH_INDEX)
    #end

    def __add_scale(self, label_text, scale_from, scale_to, scale_resolution, scale_default):
        label = tk.Label(self.window, text=label_text)
        label.grid(row=self.current_row, column=0, padx=10, pady=10)
        self.scale_labels.append(label)

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

    def __add_file_select_button(self):
        self.file_select_button = tk.Button(self.window, text="Choose svg file", command=lambda: entry.insert(tk.END, self.__select_file()))
        self.file_select_button.grid(row=self.current_row, column=0, padx=10, pady=10)

        entry = tk.Entry(self.window, width=100)
        entry.grid(row=self.current_row, column=1, padx=10, pady=10)
        self.entries.append(entry)

        self.current_row += 1
    #end

    def __execute(self):
        reading_file_path         = str( self.entries[0].get() )
        #reading_file_path         = f"./Futago.svg"
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

    def __add_execute_button(self, button_text):
        self.execute_button = tk.Button(self.window, text=button_text, command=lambda: self.__execute())
        self.execute_button.grid(row=self.current_row, column=0, columnspan=2, padx=10, pady=10)
        self.current_row += 1
    #end

    def __add_progress_bar(self):
        self.progress_bar = ttk.Progressbar(self.window, length=200, mode="determinate", maximum=100)
        self.progress_bar.grid(row=self.current_row, column=0, padx=10, pady=10)

        self.log_text = tk.Text(self.window, height=10)
        self.log_text.grid(row=self.current_row, column=1, padx=10, pady=10)
        self.current_row += 1
    #end

    def __add_menu_bar(self):
        self.menu_bar = tk.Menu(self.window)
        self.window.config(menu=self.menu_bar)

        language_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Language", menu=language_menu)
        language_menu.add_command( label="日本語", command=self.__set_language_japanese )
        language_menu.add_command( label="English", command=self.__set_language_english )
    #end

    def run_init_setting_window(self):
        self.__create_init_setting_window()
        self.init_setting.mainloop()
    #end

    def run_main_window(self, selected_language):
        self.__create_main_window()
        if selected_language == "Japanese":
            self.__update_language(self.JAPANESE_INDEX)
        else: # English or ohter unknown settings
            self.__update_language(self.ENGLISH_INDEX)
        #end
        self.window.mainloop()
    #end
#end

gui = GuiBeautifulLiner()
try:
    # Load saved language from JSON file
    with open("language_settings.json", "r") as json_file:
        language_data = json.load(json_file)
        selected_language = language_data.get("language", "English")
        gui.run_main_window(selected_language)
    #end
except FileNotFoundError:
    # If JSON file doesn't exist, default to English
    selected_language = "English"
    gui.run_init_setting_window()
#end


