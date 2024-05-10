import random
import string
import tkinter as tk
import pyperclip


class PasswordGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("Password Generator")

        self.length_label = tk.Label(master, text="Desired password length:")
        self.length_label.grid(row=0, column=0, sticky="w")
        self.length_entry = tk.Entry(master)
        self.length_entry.grid(row=0, column=1)

        self.lowercase_var = tk.BooleanVar()
        self.lowercase_var.set(True)  # Default to include lowercase letters
        self.lowercase_checkbutton = tk.Checkbutton(master, text="Include lowercase letters", variable=self.lowercase_var)
        self.lowercase_checkbutton.grid(row=1, column=0, columnspan=2, sticky="w")

        # Similar check buttons for uppercase, numbers, symbols can be added here

        self.complexity_label = tk.Label(master, text="Select complexity:")
        self.complexity_label.grid(row=2, column=0, sticky="w")

        self.complexity_var = tk.StringVar(value="Medium")
        self.complexity_options = ["Simple", "Medium", "Hard"]
        self.complexity_menu = tk.OptionMenu(master, self.complexity_var, *self.complexity_options)
        self.complexity_menu.grid(row=2, column=1, sticky="ew")
        self.generate_button = tk.Button(master, text="Generate Password", command=self.generate_password)
        self.generate_button.grid(row=3, columnspan=2)

        self.password_label = tk.Label(master, text="")
        self.password_label.grid(row=4, columnspan=2)
        self.copy_button = tk.Button(master, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.grid(row=5, columnspan=2)

    def generate_password(self):
        length = int(self.length_entry.get())
        lowercase = string.ascii_lowercase if self.lowercase_var.get() else ''

        complexity = self.complexity_var.get()
        if complexity == "Simple":
            chars = string.ascii_letters + string.digits
        elif complexity == "Medium":
            chars = string.ascii_letters + string.digits + string.punctuation
        else:  # Hard
            chars = string.ascii_letters + string.digits + string.punctuation + string.whitespace

        password = self.generate_strong_password(length, chars)
        self.password_label.config(text="Your generated password is: " + password)

    def generate_strong_password(self, length, chars):
        return ''.join(random.choice(chars) for _ in range(length))

    def copy_to_clipboard(self):
        password = self.password_label.cget("text").split(": ")[1]
        pyperclip.copy(password)
        print("Password copied to clipboard!")


def main():
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
