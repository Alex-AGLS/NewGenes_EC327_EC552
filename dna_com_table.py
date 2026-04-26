import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import csv
# part_table = "parts_table.csv"
class left_down(tk.Frame):
    def __init__(self,root,part_table="parts_table.csv"):
        tk.Frame.__init__(self,root)
        self.part_table = part_table
        self.setup_dna()

    def load_csv(self, part_table,table):
        with open(part_table, 'r', newline = '') as file:
            csv_line = csv.reader(file)
            title_parts = next(csv_line)
            title = title_parts[1] + "'s DNA Components"
            sub_components = next(csv_line)   
            print (sub_components)
            table.delete(*table.get_children())
            #maybe need to clear the current data
            table["columns"] = sub_components
            table["show"] = "headings"
            for col in sub_components:
                table.heading(col, text=col)
                table.column(col, width=10)
            for row in csv_line:
                table.insert("", "end", values=row)
        return title


    def setup_dna(self):
        # root = tk.Tk()
        # #root.attributes('-fullscreen',True)
        # root.title("DNA Components")
        # root.geometry("800x500")
        self.title_label = tk.Label(self, text="", font=("Arial", 14))
        self.title_label.pack(pady = 5)   
        
        self.table = ttk.Treeview(self)
        self.table.pack(fill="both", expand=True)

        self.title = self.load_csv(self.part_table, self.table)
        self.title_label.config(text=self.title)

    # root.mainloop()
