import io
import os
import tkinter as tk
import urllib

from PIL import Image, ImageTk, ImageGrab

import ff_functions as ff_functions
pip_format_string = "pip install {}"
try:
    import win32api
    import win32con
    import win32gui
except ModuleNotFoundError:
    os.system(pip_format_string.format("pywin32"))
    import win32api
    import win32con
    import win32gui

# try:
#     import tkFont as tkfont
# except ModuleNotFoundError:
#     os.system(pip_format_string.format("tkFont"))
#     import tkFont as tkfont
    
    
COL = 21
DARK_BLUE = "#192841"
TRANSPARENT = "#ab23ff"


def clear_canvas(canvases):
    for each in canvases:
        each.grid_remove()


def pull_data_id(character, entry_value):
    data = ff_functions.character_by_id(entry_value)
    character.data = data
    print(character.data["Character"]["Name"])


def pull_data_name(character, entry_value):
    data = ff_functions.character_by_name(entry_value)
    character.data = data
    print(character.data["Character"]["Name"])


def getter(widget, portrait, filename):
    x = portrait.winfo_rootx() + 2
    y = portrait.winfo_rooty() + 15
    print(x, y)
    x1 = x + widget.winfo_rootx() + widget.winfo_width()+200
    y1 = y + 660

    print(x1, y1)
    ImageGrab.grab().crop((x, y, x1, y1)).save(filename)


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
    portrait = tk.Label(master, image=character.portrait, borderwidth=0)
    portrait.grid(row=1, sticky=tk.W, rowspan=16, columnspan=COL)
    row = 1
    character.icons = []
    for index, value in enumerate(character.all_classes_and_jobs):
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
                    master, width=40, height=40, highlightthickness=0)

                hwnd = label1.winfo_id()
                colorkey = win32api.RGB(0, 0, 0)
                wnd_exstyle = win32gui.GetWindowLong(
                    hwnd, win32con.GWL_EXSTYLE)
                new_exstyle = wnd_exstyle | win32con.WS_EX_LAYERED
                win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_exstyle)
                win32gui.SetLayeredWindowAttributes(
                    hwnd, colorkey, 255, win32con.LWA_COLORKEY)
                label1.config(bg="#000000")

                label1.create_image(0, 0, anchor='nw', image=test)
                character.level_dict[each]
                # Position image
                label1.grid(row=row, column=col)
                character.icons.append(test)
                character.canvas_list.append(label1)

                text = tk.Canvas(master, width=30, height=30,
                                 highlightthickness=0)
                hwnd = text.winfo_id()
                colorkey = win32api.RGB(0, 0, 0)
                wnd_exstyle = win32gui.GetWindowLong(
                    hwnd, win32con.GWL_EXSTYLE)
                new_exstyle = wnd_exstyle | win32con.WS_EX_LAYERED
                win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_exstyle)
                win32gui.SetLayeredWindowAttributes(
                    hwnd, colorkey, 255, win32con.LWA_COLORKEY)
                text.config(bg="#000000")

                text.create_text(15, 15, text=f"{character.level_dict[each]:02}", font=(
                    "Courier New", 19, "bold"), fill="#dbc300")
                text.grid(row=row+1, column=col)
                character.canvas_list.append(text)
                col += 1
        row += 2
        if row == 5:
            row += 1
    picture_name = character.data["Character"]["Name"].replace(" ", "_")
    button = tk.Button(master, text="Export", bg=DARK_BLUE, fg="YELLOW",
                       command=lambda: getter(button, portrait, f"characters/{picture_name}.jpeg"))
    button.grid(row=row+1, column=COL+9)


def main():
    data = None
    mommy = ff_functions.Character(data)
    # Create the master object
    master = tk.Tk()
    master.overrideredirect(True)
    master.geometry("+0+0")
    bg_photo = ImageTk.PhotoImage(file="sample.jpg")
    bg_label = tk.Label(master, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    # Create the label objects and pack them using grid
    tk.Label(master, text="Search", bg=DARK_BLUE,
             fg="YELLOW").grid(row=0, column=0)

    # Create the entry objects using master
    e1 = tk.Entry(master)

    # Pack them using grid
    e1.grid(row=0, column=1, columnspan=4)

    button1 = tk.Button(master, text="Name", bg=DARK_BLUE, fg="YELLOW",
                        command=lambda: pull_data_name(mommy, e1.get()))
    button1.grid(row=0, column=5)
    button2 = tk.Button(master, text="ID", bg=DARK_BLUE, fg="YELLOW",
                        command=lambda: pull_data_id(mommy, e1.get()))
    button2.grid(row=0, column=6)
    display_button = tk.Button(master, text="Display", bg=DARK_BLUE,
                               fg="YELLOW", command=lambda: display_info(mommy, master))
    display_button.grid(row=0, column=7)
    display_button = tk.Button(master, text="X", bg=DARK_BLUE,
                               fg="YELLOW", command=lambda:master.destroy())
    display_button.grid(row=0, column=COL+9, sticky="E")
    # The mainloop
    tk.mainloop()


if __name__ == "__main__":
    main()
