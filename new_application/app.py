import tkinter as tk
import data_get
import character

DARK_BLUE = "#192841"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FFXIV Character Data")
        self.geometry("850x675")  # Adjusted size for better layout
        self.resizable(False, False)
        # Set the background color of the app
        self.configure(bg=DARK_BLUE)

        self.character = character.Character()
        self.create_widgets()
        self.bind("<Return>", self.search_character)  # Bind Enter key to search_character method

    def create_widgets(self):
        # Entry for Character ID
        self.character_id_label = tk.Label(self, text="Character ID:", font=("Courier New", 11, "bold"), fg="#dbc300", bg=DARK_BLUE)
        self.character_id_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        self.character_id_entry = tk.Entry(self, width=30)
        self.character_id_entry.grid(row=0, column=1, padx=10, pady=10)

        # Search Button
        self.search_button = tk.Button(self, text="Search", command=self.search_character, font=("Courier New", 11, "bold"), fg="#dbc300", bg=DARK_BLUE)
        self.search_button.grid(row=0, column=2, padx=10, pady=10)

        # Labels for Character Information
        self.character_name = tk.Label(self, text="", font=("Courier New", 17, "bold"), fg="#dbc300", bg=DARK_BLUE)
        self.character_name.grid(row=1, column=character.COL,  columnspan=10, padx=10, pady=5, sticky=tk.W)

        self.world_name = tk.Label(self, text="", font=("Courier New", 13, "bold"), fg="#dbc300", bg=DARK_BLUE)
        self.world_name.grid(row=2, column=character.COL, columnspan=7,  pady=5, sticky=tk.W)

        self.free_company = tk.Label(self, text="", font=("Courier New", 13, "bold"), fg="#dbc300", bg=DARK_BLUE)
        self.free_company.grid(row=2, column=character.COL+6, columnspan=10, pady=5, sticky=tk.W)

        self.character_image = tk.Label(self, text="", bg=DARK_BLUE)
        self.character_image.grid(row=4, column=1, padx=30, pady=5, sticky=tk.W)


    def search_character(self, event=None):
        # Get the Character ID from the entry box
        character_id = self.character_id_entry.get()

        # Fetch the character data
        character_data = data_get.fetch_character_data(character_id)

        if character_data:
            # Save character data to JSON file
            data_get.save_character_data_to_json(character_data, "character_data.json")

            # Update the character instance with new data
            self.character.set_data(character_data)

            # Use the Character class's display_info method to show data in the GUI
            self.character.display_info(self)

            # Update the text labels with basic character info
            self.character_name.config(text=self.character.get_name())
            self.world_name.config(text=self.character.get_world_name())
            self.free_company.config(text=f"FC: " + self.character.get_free_company())
        else:
            # Reset labels if character not found
            self.character_name.config(text="Character not found.")
            self.world_name.config(text="")
            self.free_company.config(text="")
            self.character_image.config(image="")

if __name__ == "__main__":
    app = App()
    app.mainloop()
