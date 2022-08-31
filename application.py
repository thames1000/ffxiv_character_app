import io
import os
import tkinter as tk
import urllib
from PIL import Image, ImageTk
import ff_functions
from ff_functions import PIP, SERVERS_LIST, DROP_DOWN_DEFAULT

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

    
COL = 21
DARK_BLUE = "#192841"
TRANSPARENT = "#000000"


def clear_canvas(canvases):
    for each in canvases:
        each.grid_remove()

def set_transparent_background(widget):
    hwnd = widget.winfo_id()
    colorkey = win32api.RGB(0, 0, 0)
    wnd_exstyle = win32gui.GetWindowLong(
        hwnd, win32con.GWL_EXSTYLE)
    new_exstyle = wnd_exstyle | win32con.WS_EX_LAYERED
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_exstyle)
    win32gui.SetLayeredWindowAttributes(
        hwnd, colorkey, 255, win32con.LWA_COLORKEY)

def pull_data_id(character, entry_value):
    data = ff_functions.character_by_id(entry_value)
    character.data = data
    print(character.data["Character"]["Name"])


def pull_data_name(character, entry_value, server):
    data = ff_functions.character_by_name(entry_value, server)
    character.data = data
    print(character.data["Character"]["Name"])

def getter(widget, filename):
    x, y = widget.winfo_rootx(), widget.winfo_rooty()
    w, h = widget.winfo_width(), widget.winfo_height()
    pyautogui.screenshot(filename, region=(x, y+35, w, h-70))


def display_info(character, master):
    clear_canvas(character.canvas_list)
    character.canvas_list = []
    character.get_class_job_levels()
    portrait_url = character.data["Character"]["Portrait"]
    raw_data = urllib.request.urlopen(portrait_url).read()
    im = Image.open(io.BytesIO(raw_data))
    im = im.resize((420, 540), Image.Resampling.LANCZOS)
    image = ImageTk.PhotoImage(im)
    character.portrait = image
    portrait = tk.Label(master, image=character.portrait, borderwidth=1)
    portrait.grid(row=1, sticky=tk.W, rowspan=16, columnspan=COL)
    row = 1
    character.canvas_list.append(portrait)
    character.icons = []
    for value in character.all_classes_and_jobs:
        col = COL
        for idx, classes in enumerate(value):
            if (idx == 1):
                col = COL+7
            for each in classes:
                printed = each
                if (each == "Blue Mage (Limited Job)"):
                    printed = "Blue Mage"
                    col += 1
                filename = printed.replace(" ", "").lower()
                icon = Image.open(f"icons/{filename}.png")
                icon = icon.resize((40, 40))
                test = ImageTk.PhotoImage(icon)

                label1 = tk.Canvas(
                    master, width=40, height=40, highlightthickness=0,bg=TRANSPARENT)
                set_transparent_background(label1)
                label1.create_image(0, 0, anchor='nw', image=test)
                character.level_dict[each]
                # Position image
                label1.grid(row=row, column=col)
                character.icons.append(test)
                character.canvas_list.append(label1)

                text = tk.Canvas(master, width=30, height=30,
                                 highlightthickness=0,bg=TRANSPARENT)
                set_transparent_background(text)
                text.create_text(15, 15, text=f"{character.level_dict[each]:02}", font=(
                    "Courier New", 17, "bold"), fill="#dbc300")
                text.grid(row=row+1, column=col)
                character.canvas_list.append(text)
                col += 1
        row += 2
        if row == 5:
            row += 1
    picture_name = character.data["Character"]["Name"].replace(" ", "_")
    button = tk.Button(master, text=f"Export to characters folder as {picture_name}.jpeg", fg="YELLOW", bg=DARK_BLUE,
                       command=lambda: getter(master, f"characters/{picture_name}.jpeg"))
    button.grid(row=row+1, column=COL, columnspan=10)
    character.canvas_list.append(button)


def main():
    data = None
    mommy = ff_functions.Character(data)
    # Create the master object
    master = tk.Tk()
    master.title("FFXIV Character Sheet")
    master.geometry("+0+0")
    bg_photo = ImageTk.PhotoImage(file="sample.jpg")
    bg_label = tk.Label(master, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    # Create the label objects and pack them using grid
    search = tk.Label(master, text="Search",fg="YELLOW",bg="#000000")

    # Create the entry objects using master
    e1 = tk.Entry(master)

    # Pack them using grid
    e1.grid(row=0, column=1, columnspan=4)

    clicked = tk.StringVar()
    clicked.set(DROP_DOWN_DEFAULT)
    button1 = tk.Button(master, text="Name", bg=DARK_BLUE, fg="YELLOW",
                        command=lambda: pull_data_name(mommy, e1.get(), clicked))
    
    button2 = tk.Button(master, text="ID", bg=DARK_BLUE, fg="YELLOW",
                        command=lambda: pull_data_id(mommy, e1.get(), clicked))
    
    display_button = tk.Button(master, text="Display", bg=DARK_BLUE,
                               fg="YELLOW", command=lambda: display_info(mommy, master))
    
    server_dropdown = tk.OptionMenu(master,clicked,DROP_DOWN_DEFAULT,*SERVERS_LIST)
    server_dropdown.config(bg=DARK_BLUE, fg="YELLOW", highlightthickness=0)
    quit_button = tk.Button(master, text="Quit", bg=DARK_BLUE,
                               fg="YELLOW", command=lambda:master.destroy())
    
    set_transparent_background(search)
    ######################################################
    #  Currently Erases Previous Button/Label if called  #
    ######################################################
    # set_transparent_background(button1)
    # set_transparent_background(button2)
    # set_transparent_background(display_button)
    # set_transparent_background(quit_button)
    ######################################################
    
    search.grid(row=0, column=0)
    button1.grid(row=0, column=5)
    button2.grid(row=0, column=6)
    display_button.grid(row=0, column=7)
    quit_button.grid(row=0, column=COL+9, sticky="E")
    server_dropdown.grid(row=0, column=8, columnspan = 3)
    # The mainloop
    tk.mainloop()


if __name__ == "__main__":
    main()
