import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import tkhtmlview
from tkhtmlview import HTMLLabel
import markdown
import pandas as pd
import csv
# csv_file = "summary.csv"
# table_title = "Protocol's data"
# protocol_file = "full_protocol.md"

class right_up_pane(tk.Frame):
    def __init__(self,root,csv_file = "summary.csv", table_title = "Protocol's data" ):
        tk.Frame.__init__(self, root)
        self.csv_file = csv_file
        self.table_title = table_title
        self.setup_table()

    def summary_table(self,filename, table):
        with open(filename, 'r', newline = '') as file:
            cvs_line = csv.reader(file)
            type_name = next(cvs_line)
            table["columns"] = type_name
            table["show"] = "headings"
            for col in type_name:
                table.heading(col, text = col)
                table.column(col, width = 20)
            data = next(cvs_line)
            table.insert("","end", values = data)




    def setup_table(self):
        # root = tk.Tk()
        # root.geometry("800x500")
        self.table_label = tk.Label(self, text = self.table_title, font=("Arial", 14))
        self.table_label.pack(pady = 5) 

        self.table_sum = ttk.Treeview(self)
        self.table_sum.pack(fill = "both", expand = True)
        self.summary_table(self.csv_file,self.table_sum)
        
        

#     root.mainloop()

# if __name__ == '__main__':
#     main()