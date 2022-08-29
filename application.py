import tkinter as tk
import ff_functions as ff_functions
from PIL import ImageTk, Image
import urllib
import io
COL = 21
DARK_BLUE = "#192841"
def pull_data_id(character, entry_value):
    data = ff_functions.character_by_id(entry_value)
    character.data = data
    print(character.data["Character"]["Name"])

def pull_data_name(character, entry_value):
    data = ff_functions.character_by_name(entry_value)
    character.data = data
    print(character.data["Character"]["Name"])

def display_info(character, master):
    character.get_class_job_levels()
    portrait_url = character.data["Character"]["Portrait"]
    raw_data = urllib.request.urlopen(portrait_url).read()
    im = Image.open(io.BytesIO(raw_data))
    im = im.resize((420, 540), Image.Resampling.LANCZOS)
    image = ImageTk.PhotoImage(im)
    character.portrait = image
    label1 = tk.Label(master, image=character.portrait, borderwidth=0)
    label1.grid(row=1, sticky=tk.W, rowspan=16, columnspan=COL)
    row = 1
    for index, value in enumerate(character.all_classes_and_jobs):
        col  = COL
        for idx,classes in enumerate(value):
            if (idx==1):
                col = COL+7
            for each in classes:
                printed = each
                if(each == "Blue Mage (Limited Job)"):
                    printed = "Blue Mage"
                    col+=1
                filename=printed.replace(" ","").lower()
                image1 = Image.open(f"icons/{filename}.png")
                image1 = image1.resize((30, 30), Image.Resampling.LANCZOS)
                test = ImageTk.PhotoImage(image1)

                label1 = tk.Label(master, image=test, bg=DARK_BLUE)
                label1.image = test
                character.level_dict[each]
                # Position image
                label1.grid(row = row, column = col)
                tk.Label(master, text = f"{character.level_dict[each]:02}", font=("Courier New", 18), fg = "YELLOW", bg=DARK_BLUE).grid(row = row+1, column = col)
                col+=1
        row+=2
        if row == 5:
            row+=1
    
def main():
    data = None
    mommy = ff_functions.Character(data)
    # Create the master object
    master = tk.Tk()
    # bg_photo = tk.PhotoImage(file = "background.png")
    master.configure(bg=DARK_BLUE)
    # Create the label objects and pack them using grid
    tk.Label(master, text="Search",bg=DARK_BLUE,fg="YELLOW").grid(row=0, column=0)

    # Create the entry objects using master
    e1 = tk.Entry(master)

    # Pack them using grid
    e1.grid(row=0, column=1, columnspan=4)

    tk.Frame(master).columnconfigure(0, weight=3)
    
    

    button1 = tk.Button(master, text="Name", bg=DARK_BLUE, fg="YELLOW", command=lambda:pull_data_name(mommy, e1.get())).grid(row=0, column=5)
    button2 = tk.Button(master, text="ID", bg=DARK_BLUE, fg="YELLOW", command=lambda:pull_data_id(mommy, e1.get())).grid(row=0, column=6)
    display_button = tk.Button(master, text = "Display", bg=DARK_BLUE,fg="YELLOW", command = lambda:display_info(mommy, master)).grid(row=0, column=7)

    # The mainloop
    tk.mainloop()

if __name__ == "__main__":
    main()