import os
import pickle
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from ttkthemes import ThemedStyle

class NotepadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NoteS")
        self.theme_mode = tk.StringVar(value="dark")  # Initialize the default theme

        # Sidebar
        self.sidebar_frame = tk.Frame(root, width=150, bg="#EFEFEF")
        self.sidebar_frame.pack(fill="y", side="left")

        self.create_sidebar()

        # Text area
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12))
        self.text_area.pack(expand=True, fill='both')

        self.show_sidebar = True
        self.show_hide_button = tk.Button(root, text="Hide Sidebar", width=12, command=self.toggle_sidebar)
        self.show_hide_button.pack(pady=5, side="top")  # Specify the side to place the button at the top of the window.

        self.set_theme()

        self.cursor_color = "yellow"  # Default cursor color for dark theme
        self.blink_cursor()

    def create_sidebar(self):
        tk.Button(self.sidebar_frame, text="New", width=10, command=self.new_file).pack(pady=5)
        tk.Button(self.sidebar_frame, text="Open", width=10, command=self.open_file).pack(pady=5)
        tk.Button(self.sidebar_frame, text="Save", width=10, command=self.save_file).pack(pady=5)
        tk.Radiobutton(self.sidebar_frame, text="Light", variable=self.theme_mode, value="light", command=self.set_theme).pack(pady=5)
        tk.Radiobutton(self.sidebar_frame, text="Dark", variable=self.theme_mode, value="dark", command=self.set_theme).pack(pady=5)

    def toggle_sidebar(self):
        if self.show_sidebar:
            self.sidebar_frame.pack_forget()
            self.show_hide_button.config(text="Show Sidebar")
        else:
            self.create_sidebar()
            self.show_hide_button.config(text="Hide Sidebar")
        self.show_sidebar = not self.show_sidebar

    def set_theme(self):
        theme_mode = self.theme_mode.get()
        style = ThemedStyle(self.root)
        if theme_mode == "dark":
            style.theme_use("equilux")
            self.text_area.config(fg="white", bg="black")
            self.cursor_color = "yellow"  # Yellow for dark theme
        else:
            style.theme_use("default")
            self.text_area.config(fg="black", bg="white")
            self.cursor_color = "red"  # Red for light theme

    def new_file(self):
        if self.text_area.get(1.0, tk.END).strip():
            # Save the old data to a separate folder with .dat format
            self.save_old_data()

        # Clear the text area
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, file.read())
            except Exception as e:
                messagebox.showerror("Error", f"Error while opening the file: {e}")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(self.text_area.get(1.0, tk.END))
            except Exception as e:
                messagebox.showerror("Error", f"Error while saving the file: {e}")

    def save_old_data(self):
        old_data_folder = "Old_Data"
        if not os.path.exists(old_data_folder):
            os.makedirs(old_data_folder)

        # Generate a unique filename
        file_number = 1
        while os.path.exists(os.path.join(old_data_folder, f"old_data_{file_number}.dat")):
            file_number += 1

        # Save the old data in a .dat file
        with open(os.path.join(old_data_folder, f"old_data_{file_number}.dat"), "wb") as file:
            data_to_save = self.text_area.get(1.0, tk.END)
            pickle.dump(data_to_save, file)

    def blink_cursor(self):
        cursor_color = self.text_area.cget("insertbackground")
        if cursor_color == self.cursor_color:
            next_cursor_color = self.text_area.cget("foreground")
        else:
            next_cursor_color = self.cursor_color
        self.text_area.config(insertbackground=next_cursor_color)
        self.root.after(500, self.blink_cursor)

def main():
    root = tk.Tk()
    notepad_app = NotepadApp(root)
    root.mainloop()

if __name__ == "__main__":
    print("Running the application ")
    main()
