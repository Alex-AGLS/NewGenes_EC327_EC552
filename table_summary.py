import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import tkhtmlview
from tkhtmlview import HTMLLabel
import markdown
import pandas as pd
import csv
class right_down_pane(tk.Frame):
    def __init__(self,root, protocol_file = "full_protocol.md"):
        tk.Frame.__init__(self, root)
        self.protocol_file = protocol_file
        self.setup_protocol()
    def protocol(self,filename, proto):
        with open(filename, "r", encoding="utf-8") as file:
                content = file.read()
        proto.insert(tk.END,content)
        proto.config(state=tk.DISABLED)
        # text_area.insert()
    def setup_protocol(self):
        self.proto =  tk.Text(self, wrap =  "word")
        self.proto.pack(expand = True, fill = "both")
        self.protocol(self.protocol_file,self.proto)

    