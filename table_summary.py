import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import tkhtmlview
from tkhtmlview import HTMLLabel
import markdown
import pandas as pd
import csv
WHITE = "#FFFFFF"
class right_down_pane(tk.Frame):
    def __init__(self,root, color, protocol_file = "full_protocol.md"):
        tk.Frame.__init__(self, root, bg=color,pady=0)
        self.protocol_file = protocol_file
        self.proto =  tk.Text(self, wrap =  "word", background=color)
        self.empty = True
    def protocol(self,filename, proto):
        with open(filename, "r", encoding="utf-8") as file:
                content = file.read()
        proto.insert(tk.END,content)
        proto.config(state=tk.DISABLED)
        # text_area.insert()
    def refresh(self):
         self.empty = True
         self.setup_protocol()
    def set_file(self, md="full_protocol.md"):
         self.protocol_file = md
         self.empty = False
         self.setup_protocol()
    def setup_protocol(self):
        if (self.empty):
             self.proto.pack_forget()
             return
        self.proto.pack(expand = True, fill = "both")
        self.proto.config(background=WHITE)
        self.protocol(self.protocol_file,self.proto)

    