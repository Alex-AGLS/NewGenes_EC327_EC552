import tkinter as tk
from turtle import width

HEIGHT = 600
WIDTH = 800

class XMLViewer(tk.Frame):
    def __init__(self, master):
        super().__init__(master, background="red")
        label = tk.Label(self, text="pane1: xml viewer")
        label.pack()

class OPReader(tk.Frame):
    def __init__(self, master):
        super().__init__(master, background="blue")
        label = tk.Label(self, text="pane2: reader")
        label.pack()
        

        

class Screen(tk.PanedWindow):
    def __init__(self, master):
        super().__init__(master, orient=tk.HORIZONTAL)  # put on parent widget
        self.pack(fill=tk.BOTH, expand=True)
        # instantiate viewer and reader frames
        self.left = XMLViewer(self)

        self.right = OPReader(self)

        self.add(self.left, width=0.5*WIDTH)
        self.add(self.right)

class MenuBtn(tk.Button):
    def __init__(self, master):
        super().__init__(master, text="menu", command=self.show_menu)
        self.place(anchor='nw')
        self.lift()

        self.menu = tk.Menu(master, tearoff=0)
        self.menu.add_command(label="Refresh", command=self.refresh)
        self.menu.add_command(label="Settings", command=lambda: print("Opening Settings..."))
        self.menu.add_separator()
        self.menu.add_command(label="Exit", command=root.quit)
    def show_menu(self):
        self.menu.tk_popup(self.winfo_rootx(), self.winfo_rooty()+self.winfo_height())
    def refresh(self):
        print("refreshing")
        pass
        
        





root = tk.Tk()
root.title("SBOL XML -> Wet Lab Protocol")

root.geometry(str(WIDTH) + "x" + str(HEIGHT))
myapp = Screen(root)
ui = MenuBtn(root)
root.mainloop()