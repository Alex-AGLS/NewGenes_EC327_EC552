import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import tkhtmlview
from tkhtmlview import HTMLLabel
import markdown
import pandas as pd
import csv
csv_file = "summary.csv"
table_title = "Protocol's data"
protocol_file = "full_protocol.md"
def summary_table(filename, table):
    with open(filename, 'r', newline = '') as file:
        cvs_line = csv.reader(file)
        type_name = next(cvs_line)
        table["column"] = type_name
        table["show"] = "headings"
        for col in type_name:
            table.heading(col, text = col)
            table.column(col, width = 20)
        data = next(cvs_line)
        table.insert("","end", value = data)

def protocol(filename, proto):
    with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
    proto.insert(tk.END,content)
    proto.config(state=tk.DISABLED)
    # text_area.insert()

def main():
    root = tk.Tk()
    root.geometry("800x500")
    table_label = tk.Label(root, text = table_title, font=("Arial", 14))
    table_label.pack(pady = 5) 

    table_sum = ttk.Treeview(root)
    table_sum.pack(fill = "both", expand = True)
    summary_table(csv_file,table_sum)
    
    proto =  tk.Text(root, wrap =  "word")
    proto.pack(expand = True, fill = "both")
    protocol(protocol_file,proto)
    
    # CANVAS WAY
    # proto = tk.Canvas(root)
    # scrollbar = tk.Scrollbar(root,orient = "vertical", command = proto.yview)
    # scroll_frame= tk.Frame(proto)
    # scroll_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    # proto.create_window((0, 0), window=scroll_frame, anchor="nw")
    # proto.configure(yscrollcommand=scrollbar.set)


    # text_area = scrolledtext.ScrolledText(root, background = "white",font = "Times New Roman")
    # text_area.pack(padx = 10, pady = 10, fill = 'BOTH', expand = True)
    # protocol(protocol_file,text_area)
    root.mainloop()

if __name__ == '__main__':
    main()