from email.headerregistry import HeaderRegistry
from pydoc import text
import tkinter as tk
from tkinter import messagebox
import left_pane
import structure
import sv_ttk
from tkinter import HORIZONTAL, filedialog

HEIGHT = 600
WIDTH = 800
BACKGROUND_COLOR = "#2A2A3E"
FONT = ("Helvetica", 10)

def refresh():
    print("refreshing")
    myapp.refresh()

class OPReader(tk.Frame):
    def __init__(self, master):
        super().__init__(master, background="blue")
        self.label = tk.Label(self, text="pane2: reader")
        self.label.pack()
    def change_text(self, new_text):
        self.label.config(text=new_text)


class Screen(tk.PanedWindow):
    def __init__(self, master):
        super().__init__(master, orient=tk.VERTICAL)  # put on parent widget
        self.pack(fill=tk.BOTH, expand=True)
        
        content = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        
        # instantiate viewer and reader frames
        left = tk.PanedWindow(content, orient=tk.VERTICAL)
        self.viewer = left_pane.XMLViewer(left)
        left.add(self.viewer)
        left.add(OPReader(left))
        
        self.right = OPReader(content)

        content.add(left, width=0.5*WIDTH)
        content.add(self.right)

        self.xml = self.viewer.get_xml_path()
        self.right.change_text(self.xml)
        header = Header(self, self)
        self.add(header)
        self.add(content)
    
    def refresh(self):
        self.right.change_text("ghj")
        self.viewer.refresh()
        self.xml = None

    def get_viewer(self):
        return self.viewer
    
    def process_xml(self, csv="parts.csv"):
        xml = self.viewer.get_xml_path()
        try:
            structure.get_table(xml,csv)
            structure.get_pcr_info("data.json", "sample.txt", "summary.csv")
        except TypeError:
            messagebox.showerror("XML Input Error", "empty or invalid SBOL XML file")
        

class MenuBtn(tk.Button):
    def __init__(self, master):
        super().__init__(master, text="Menu",
            relief="flat", bg=BACKGROUND_COLOR,
            font=FONT,
            cursor="hand2", command=self.show_menu)
        self.menu = tk.Menu(master, tearoff=0)
        self.menu.add_command(label="Refresh", command=refresh)
        self.menu.add_command(label="Settings", command=lambda: print("Opening Settings..."))
        self.menu.add_separator()
        self.menu.add_command(label="Exit", command=root.quit)
    def show_menu(self):
        self.menu.tk_popup(self.winfo_rootx(), self.winfo_rooty()+self.winfo_height())

class UploadButton(tk.Button):
    def __init__(self, master, screen) -> None:
        super().__init__(master, text="Upload", 
                         command=self.on_upload_click, relief="flat", bg=BACKGROUND_COLOR,
            font=FONT,
            cursor="hand2")
        self.viewer = screen.get_viewer()
    def on_upload_click(self):
        path = filedialog.askopenfilename(
            title="Select an SBOL XML file",
            filetypes=[("SBOL XML files", "*.xml"), ("All files", "*.*")],
        )
        if not path:
            return  # user cancelled
        self.viewer._load_and_display(path)

class RunButton(tk.Button):
    def __init__(self, master, screen):
        super().__init__(master, text="Run",relief="flat",
                          font=FONT, bg=BACKGROUND_COLOR, command=self.on_run_clicked)
        self.screen = screen
    def on_run_clicked(self):
        self.screen.process_xml()

class Header(tk.Frame):
    def __init__(self, master, screen, orient=HORIZONTAL):
        super().__init__(master)
        menu_btn = MenuBtn(self)
        menu_btn.grid(row=0, column=1)
        upload_btn = UploadButton(self, screen)
        upload_btn.grid(row=0, column=2)
        run_btn = RunButton(self, screen)
        run_btn.grid(row=0, column=3)
        self.place(anchor='nw')



root = tk.Tk()
root.title("SBOL XML -> Wet Lab Protocol")
root.geometry(str(WIDTH) + "x" + str(HEIGHT))
myapp = Screen(root)
sv_ttk.set_theme("dark")
root.mainloop()