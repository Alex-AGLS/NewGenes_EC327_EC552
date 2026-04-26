import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import csv
part_table = "parts_table.csv"
def load_csv(part_table,table):
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


def main():
    root = tk.Tk()
    #root.attributes('-fullscreen',True)
    root.title("DNA Components")
    root.geometry("800x500")
    title_label = tk.Label(root, text="", font=("Arial", 14))
    title_label.pack(pady = 5)   
    
    table = ttk.Treeview(root)
    table.pack(fill="both", expand=True)

    title = load_csv(part_table, table)
    title_label.config(text=title)

    root.mainloop()
if __name__ == '__main__':
    main()