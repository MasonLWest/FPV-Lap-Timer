from tkinter import Tk, Label, Entry, Button, Toplevel, Scrollbar, Listbox, messagebox
from PIL import Image, ImageTk
import io
import requests
import re

class LapTracker:
    def __init__(self, root):
        # Initialize the LapTracker class with a Tkinter root window
        self.root = root
        # Initialize empty list to store lap times for each racer
        self.lap_times = []
        # Initialize Toplevel window for displaying lap times and setting its value to None
        self.lap_time_window = None
        self.lap_time_display_window = None
        # Initialize list of racer names with empty strings
        self.racer_names = ["", "", "", ""]
        # Initialize lists to store racer name labels and entry widgets
        self.racer_labels = []
        self.racer_entries = []
        # Create racer name labels and entry widgets for each racer
        for i in range(4):
            racer_name_label = Label(root, text=f"Racer {i+1} Name:")
            racer_name_entry = Entry(root)
            racer_name_entry.insert(0, "NAME")
            racer_name_label.grid(row=i, column=0, padx=5, pady=5, sticky="W")
            racer_name_entry.grid(row=i, column=1, padx=5, pady=5, sticky="E")
            self.racer_labels.append(racer_name_label)
            self.racer_entries.append(racer_name_entry)

            lap_time_label = Label(root, text=f"Racer {i+1} Lap Time:")
            lap_time_entry = Entry(root)
            lap_time_entry.insert(0, "01.00")
            lap_time_label.grid(row=i+4, column=0, padx=5, pady=5, sticky="W")
            lap_time_entry.grid(row=i+4, column=1, padx=5, pady=5, sticky="E")
            self.racer_entries.append(lap_time_entry)

        # Create a lap time instruction label
        lap_time_instruction_label = Label(root, text="Edit the name and times (e.g. 23.456)")
        lap_time_instruction_label.grid(row=4, column=2, padx=3, pady=3, sticky="W")
        lap_time_instruction_label = Label(root, text=" Leave name and time alone if not in use")
        lap_time_instruction_label.grid(row=5, column=2, padx=3, pady=3, sticky="W")
        lap_time_instruction_label = Label(root, text=" I want to say thanks to Ryan and Emily for their time and dedication to teaching programming")
        lap_time_instruction_label.grid(row=6, column=2, padx=3, pady=3, sticky="W")
        # Create a submit button to submit lap times
        self.submit_button = Button(root, text="Submit", command=self.submit_lap_times)
        self.submit_button.grid(row=9, column=1, pady=5, sticky="E")
        # Load an image from a URL using the requests and PIL libraries and display it in a Label widget
        img_url = "https://i.ibb.co/3T2QgC3/45.png"
        img_bytes = requests.get(img_url).content
        img = Image.open(io.BytesIO(img_bytes))
        img = img.resize((300, 200), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        label = Label(root, image=photo)
        label.image = photo
        label.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

        # Create an exit button to close the application window
        exit_button = Button(root, text="Exit", command=root.destroy)
        exit_button.grid(row=11, column=1, pady=5, sticky="E")

    def is_valid_lap_time(self, lap_time):
        if lap_time == "":
            return False
        try:
            return float(lap_time) > 0
        except ValueError:
            return False
    def is_valid_name(self, name):
        # Check if name contains only letters
        return bool(re.match("^[a-zA-Z]*$", name))
    def show_error_message(self, message):
        messagebox.showerror("Error", message)
    def submit_lap_times(self):
        # Get racer names and lap times from the entry widgets and add them to the lap_times list
        lap_times = []
        for i in range(len(self.racer_entries)):
            if i % 2 == 0:
                racer_name = self.racer_entries[i].get()
                if not racer_name:
                    # If racer name is empty, show an error message and return
                    self.show_error_message("Racer name cannot be empty.")
                    return
                else:
                    self.racer_names[i // 2] = racer_name
            else:
                lap_time = self.racer_entries[i].get()
                if not self.is_valid_lap_time(lap_time):
                    # If lap time is invalid, show an error message and return
                    self.show_error_message("Invalid lap time format. Lap time should be in the format mm:ss.ms (e.g. 23.456).")
                    return
                elif lap_time:
                    lap_times.append((self.racer_names[i // 2], lap_time))
       # If the lap time display window has not been created, create it and display the lap times
        if self.lap_time_display_window is None:
            self.lap_time_display_window = Toplevel(self.root)
            self.lap_time_display_window.title("Lap Times")
            self.lap_time_display_window.geometry("400x300")
        # Load an image from a URL using the requests and PIL libraries and display it in a Label widget
            img_url = "https://i.ibb.co/3mMYs96/69.png"
            img_bytes = requests.get(img_url).content
            img = Image.open(io.BytesIO(img_bytes))
            img = img.resize((300, 200), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(img)
            label = Label(self.lap_time_display_window, image=photo)
            label.image = photo
            label.pack()
            
            scrollbar = Scrollbar(self.lap_time_display_window)
            scrollbar.pack(side="right", fill="y")
            self.lap_time_listbox = Listbox(self.lap_time_display_window, yscrollcommand=scrollbar.set)
            self.lap_time_listbox.pack(fill="both", expand=True)
            scrollbar.config(command=self.lap_time_listbox.yview)
         
            copy_button = Button(self.lap_time_display_window, text="Copy to Clipboard", command=lambda: self.copy_to_clipboard(lap_times))
            copy_button.pack()
    # Iterate over the lap times and add each one to the Listbox widget with alternating colors
        for i, (racer_name, lap_time) in enumerate(lap_times):
            color = "blue" if i % 2 == 0 else "red"
            self.lap_time_listbox.insert("end", f"{racer_name}: {lap_time}")
    def copy_to_clipboard(self, lap_times):
       # Convert the lap times to a string with each lap time on a new line
        lap_times_string = ""
        for i, (racer_name, lap_time) in enumerate(lap_times):
            lap_times_string += f"{racer_name}: {lap_time}\n"
       
        self.root.clipboard_clear()
        self.root.clipboard_append(lap_times_string)
    def add_racer(self):
        if len(self.racer_labels) < 4:
     # Add a new racer to the window with a name label and an entry field for their lap time
            racer_name_label = Label(self.root, text="Racer Name:")
            racer_name_label.pack()
            racer_name_entry = Entry(self.root)
            racer_name_entry.pack()
            self.racer_names.append("")
            self.racer_labels.append(racer_name_label)
            self.racer_entries.append(racer_name_entry)
       
            lap_time_label = Label(self.root, text="Enter Lap Time:")
            lap_time_label.pack()
            lap_time_entry = Entry(self.root)
            lap_time_entry.pack()
            self.racer_entries.append(lap_time_entry)

root = Tk()
root.title("Drone Race Lap Tracker")
lap_tracker = LapTracker(root)
root.mainloop()