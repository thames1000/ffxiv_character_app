from PIL import Image, ImageTk
from io import BytesIO
import urllib
import os 
import tkinter as tk

PIP = "pip install {}"
try:
    import win32api
    import win32con
    import win32gui
except ModuleNotFoundError:
    os.system(PIP.format("pywin32"))
    import win32api
    import win32con
    import win32gui

try:
    import pyautogui
except ModuleNotFoundError:
    os.system(PIP.format("pyautogui"))
    import pyautogui

DARK_BLUE = "#192841"
COL = 21
TRANSPARENT = "#000000"

def set_transparent_background(widget):
    hwnd = widget.winfo_id()
    colorkey = win32api.RGB(0, 0, 0)
    wnd_exstyle = win32gui.GetWindowLong(
        hwnd, win32con.GWL_EXSTYLE)
    new_exstyle = wnd_exstyle | win32con.WS_EX_LAYERED
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_exstyle)
    win32gui.SetLayeredWindowAttributes(
        hwnd, colorkey, 255, win32con.LWA_COLORKEY)


def getter(widget, filename):
    x, y = widget.winfo_rootx(), widget.winfo_rooty()
    w, h = widget.winfo_width(), widget.winfo_height()
    pyautogui.screenshot(filename, region=(x, y+45, w, h-75))

class Character:
    def __init__(self, character_data=None):
        """
        Initialize the Character object.

        :param character_data: Dictionary containing character data
        """
        self.data = character_data or {}
        self.canvas_list = []  # To store associated canvases
        self.icons = []        # To store job icons
        self.portrait = None   # To store character portrait

    def set_data(self, character_data):
        """
        Update character data.

        :param character_data: Dictionary containing updated character data
        """
        self.data = character_data

    def get_name(self):
        """
        Get the character's name.

        :return: Character name as a string
        """
        return self.data.get("Character Name", "Unknown")

    def get_world_name(self):
        """
        Get the character's world name.

        :return: World name as a string
        """
        return self.data.get("World Name", "Unknown")

    def get_free_company(self):
        """
        Get the character's free company name.

        :return: Free company name as a string
        """
        return self.data.get("Free Company", "No Free Company")

    def get_levels(self):
        """
        Get the character's levels for all jobs.

        :return: Dictionary of jobs and levels
        """
        return self.data.get("Levels", {})

    def get_portrait_url(self):
        """
        Get the character's portrait URL.

        :return: URL as a string
        """
        return self.data.get("Character Image", None)

    def add_canvas(self, canvas):
        """
        Add a canvas to the list of associated canvases.

        :param canvas: Tkinter canvas widget
        """
        self.canvas_list.append(canvas)

    def clear_canvases(self):
        """
        Clear all associated canvases.
        """
        for canvas in self.canvas_list:
            canvas.grid_remove()
        self.canvas_list = []

    def update_portrait(self, portrait_image):
        """
        Update the character's portrait.

        :param portrait_image: Tkinter PhotoImage object
        """
        self.portrait = portrait_image

    def add_icon(self, icon_image):
        """
        Add a job icon to the list of icons.

        :param icon_image: Tkinter PhotoImage object
        """
        self.icons.append(icon_image)

    def clear_icons(self):
        """
        Clear all stored job icons.
        """
        self.icons = []
    
    def display_info(self, master):
        # Clear previous canvas elements
        self.clear_canvases()
        self.canvas_list = []
        last_jobs = ["Gunbreaker", "Sage",  "Viper","Dancer", "Blue Mage", "Culinarian"]
        skip_jobs = ["Pictomancer"]
        # Load character portrait
        portrait_url = self.get_portrait_url()
        try:
            raw_data = urllib.request.urlopen(portrait_url).read()
            im = Image.open(BytesIO(raw_data))
            im = im.resize((450, 600), Image.Resampling.LANCZOS)
            image = ImageTk.PhotoImage(im)
            self.update_portrait(image)

            # Display portrait
            portrait = tk.Label(master, image=self.portrait, borderwidth=1)
            portrait.grid(row=1, sticky=tk.N, rowspan=16, columnspan=COL)
            self.canvas_list.append(portrait)
        except Exception as e:
            print(f"Error loading portrait: {e}")
            portrait = tk.Label(master, text="Portrait not available", borderwidth=1)
            portrait.grid(row=1, sticky=tk.N, rowspan=16, columnspan=COL)
            self.canvas_list.append(portrait)

        # Display class/job levels and icons
        row = 3
        col = COL+1

        for job, details in self.get_levels().items():

            # Fetch job icon and level data
            job_level = details["Level"]
            job_icon_url = details["Icon"]

            # Load job icon
            try:
                raw_icon_data = urllib.request.urlopen(job_icon_url).read()
                icon_im = Image.open(BytesIO(raw_icon_data))
                icon_im = icon_im.resize((40, 40), Image.Resampling.LANCZOS)
                job_icon = ImageTk.PhotoImage(icon_im)
            except Exception as e:
                print(f"Error loading icon for {job}: {e}")
                job_icon = None

            # Display job icon
            if job_icon:
                label1 = tk.Canvas(master, width=40, height=40, highlightthickness=0, bg=TRANSPARENT)
                set_transparent_background(label1)
                label1.create_image(0, 0, anchor='nw', image=job_icon)
                label1.grid(row=row, column=col)
                self.add_icon(job_icon)
                self.canvas_list.append(label1)

            # Display job level
            text = tk.Canvas(master, width=40, height=30, highlightthickness=0, bg=TRANSPARENT)
            set_transparent_background(text)
            text.create_text(
                20, 15, text=f"{job_level}", anchor="center", font=("Courier New", 14, "bold"), fill="#dbc300"
            )
            text.grid(row=row + 1, column=col)
            self.canvas_list.append(text)

            col += 1

            if job in last_jobs:
                row += 2
                col = COL+1
            elif job in skip_jobs:
                col += 1

        # Export button
        picture_name = self.get_name().replace(" ", "_")
        button = tk.Button(
            master,
            text=f"Export to characters folder as {picture_name}.jpeg",
            fg="YELLOW",
            bg=DARK_BLUE,
            command=lambda: getter(master, f"characters/{picture_name}.jpeg"),
        )
        button.grid(row=row + 2, column=COL, columnspan=10)
        self.canvas_list.append(button)
