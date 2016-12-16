import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from CryptWing.cipher import Cipher
from CryptWing.classical_ciphers import TranspositionCipher, CaesarCipher, ViginereCipher

LARGE_FONT = ("Verdana", 12)


class CryptWing(tk.Tk):
    """
    The main app class.
    Controls the screens that the app must be showing and raises up the appropriate one.
    Because of this, all window classes must have a reference to this class if access to other pages is desired.
    (Which it probably is.)
    """
    def __init__(self, *args, **kwargs):
        """
        Creates container and dictionary of frames, then displays the StartPage.
        To add more windows, create a child class of tk.Frame, then put the class name in the pages tuple.
        """
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "CryptWing")

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # To add more windows, create a class the inherits tk.Frame, and put the class name in this tuple.
        pages = (StartPage, EncryptPage, DecryptPage)
        for F in pages:

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        """
        Displays the desired frame by passing in the class name
        :param cont: The desired frame class name
        """
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    """
    Displays 3 buttons each leading to one of the main other pages in the app.
    """
    def __init__(self, parent, controller):
        """
        Fills the frame with appropriate content.
        """
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Encrypt", command=lambda: controller.show_frame(EncryptPage))
        button1.pack()

        button2 = tk.Button(self, text="Decrypt", command=lambda: controller.show_frame(DecryptPage))
        button2.pack()


class EncryptPage(tk.Frame):
    """
    The encryption page.
    Users will have the option of typing in direct input or uploading a .txt file to encrypt.
    Following this, users will have the option of selecting a cipher from the combobox, and can save
    the output content into a .txt file.
    """
    def __init__(self, parent, controller):
        """
        Creates all GUI components and places them appropriately
        Also initializes required variables.
        :param parent: Reference to parent GUI element
        :param controller: Reference to main app class
        """
        tk.Frame.__init__(self, parent)

        self.ciphers = ('Transposition Cipher', 'Caesar Cipher', 'Viginere Cipher', 'RSA Cipher')

        self.input_mode = tk.StringVar()
        self.file_path = tk.StringVar()
        self.cipher_name = tk.StringVar()
        self.cipher = Cipher()
        self.plain_text = ""
        self.cipher_text = ""

        self.grid_columnconfigure(2, minsize=550)

        rb_text = tk.Radiobutton(self, text="Input text", variable=self.input_mode, value="text_mode", command=self.rb_pushed)
        self.clear_button = tk.Button(self, text="Clear", command=self.clear_text, state='disabled')
        self.input_text = tk.Text(self, state='disabled')

        rb_file = tk.Radiobutton(self, text="Read File", variable=self.input_mode, value="file_mode", command=self.rb_pushed)
        self.open_button = tk.Button(self, text="Open", command=self.open_file, state='disabled')
        self.file_path_label = tk.Label(self, text="file path")

        cipher_label = tk.Label(self, text="Cipher")
        cipher_cbbox = ttk.Combobox(self, textvariable=self.cipher_name)
        cipher_cbbox['values'] = self.ciphers
        key_label = tk.Label(self, text="Key")
        self.key_entry = tk.Entry(self)
        encrypt_button = tk.Button(self, text="Encrypt", command=self.encrypt)

        preview_label = tk.Label(self, text="Preview")
        self.preview_message = tk.Message(self, text="Provide text input or select a file to upload.")
        fat_label = tk.Label(self)
        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        save_button = tk.Button(self, text="Save", command=self.file_save)

        # Place elements
        rb_text.grid(row=0, column=0, sticky='nsew')
        self.clear_button.grid(row=0, column=1, sticky='nsew')
        self.input_text.grid(row=1, column=0, columnspan=2, sticky='nsew')

        rb_file.grid(row=2, column=0, sticky='nsew')
        self.open_button.grid(row=2, column=1, sticky='nsew')
        self.file_path_label.grid(row=3, column=0, columnspan=2, sticky='nsw')

        cipher_label.grid(row=4, column=0, columnspan=2, sticky='nsw')
        cipher_cbbox.grid(row=5, column=0, columnspan=2, sticky='nsew')
        key_label.grid(row=6, column=0, columnspan=2, sticky='nsw')
        self.key_entry.grid(row=7, column=0, sticky='nsew')
        encrypt_button.grid(row=7, column=1, sticky='nsew')

        preview_label.grid(row=0, column=2, columnspan=3, sticky='ns')
        self.preview_message.grid(row=1, column=2, rowspan=6, columnspan=3, sticky='nsew')
        fat_label.grid(row=7, column=2)
        back_button.grid(row=7, column=3)
        save_button.grid(row=7, column=4)

    def clear_text(self):
        """
        Method for self.clear_button
        Clears all input_text
        """
        self.input_text.delete(1.0, tk.END)

    def open_file(self):
        """
        Method for self.open_button
        Opens the file selector and returns selected file path into self.file_path_label
        """
        self.file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")], initialdir='~', title="Title")
        self.file_path_label["text"] = self.file_path
        self.read_file()

    def read_file(self):
        """
        Converts file content into a string.
        That content is saved into self.plain_text, then stripped of all white spaces.
        :return:
        """
        self.plain_text = ""
        tfile = open(self.file_path)
        for line in tfile:
            self.plain_text += line
        self.plain_text.strip()

    def rb_pushed(self):
        """
        Method bound to radio buttons.
        Disables/enables the corresponding widgets related to each radio button.
        """
        if self.input_mode.get() == "text_mode":
            self.clear_button['state'] = 'normal'
            self.input_text['state'] = 'normal'
            self.open_button['state'] = 'disabled'
            print("TEXT MODE")

        if self.input_mode.get() == "file_mode":
            self.clear_button['state'] = 'disabled'
            self.input_text['state'] = 'disabled'
            self.open_button['state'] = 'normal'
            print("FILE MODE")

    def file_save(self):
        """
        Method for self.save_button
        Allows user to save encrypted text with desired name
        """
        name = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        text_to_save = str(self.cipher_text)
        name.write(text_to_save)
        name.close()

    def encrypt(self):
        """
        Calls selected cipher's encrypt() method on the plain text,
        encrypts it into cipher text, then displays the cipher text on preview_message.
        """
        # 'Transposition Cipher', 'Caesar Cipher', 'RSA Cipher')

        if self.cipher_name.get() == 'Transposition Cipher':
            self.cipher = TranspositionCipher()
        elif self.cipher_name.get() == 'Caesar Cipher':
            self.cipher = CaesarCipher()
        elif self.cipher_name.get() == 'Viginere Cipher':
            self.cipher = ViginereCipher()

        if self.input_mode.get() == "text_mode":
            self.plain_text = self.input_text.get(1.0, tk.END)
        else:
            self.read_file()

        self.plain_text = "".join(self.plain_text.split())
        key = self.key_entry.get()
        self.cipher_text = self.cipher.encrypt(self.plain_text, key)
        self.preview_message['text'] = self.cipher_text


class DecryptPage(tk.Frame):
    """
    The decryption page.
    Users will upload a (hopefully) encrypted file, then can run an analysis on the file,
    which will display information like a letter count, etc.
    Then, a decryption algorithm can be selected to attempt a decryption of the file.
    The output of this can be saved as well.
    """
    def __init__(self, parent, controller):
        """
        Creates all GUI components and places them appropriately
        Also initializes required variables.
        :param parent: Reference to parent GUI element
        :param controller: Reference to main app class
        """
        tk.Frame.__init__(self, parent)

        self.file_path = tk.StringVar()
        self.cipher = Cipher()
        self.cipher_text = ""
        self.plain_text = ""
        self.key_entry = ""

        self.ciphers = ('Transposition Cipher', 'Caesar Cipher', 'Viginere Cipher', 'RSA Cipher')
        self.cipher_name = tk.StringVar()

        self.grid_columnconfigure(0, minsize=400)
        self.grid_columnconfigure(2, minsize=650)
        self.grid_rowconfigure(2, minsize=150)
        self.grid_rowconfigure(3, minsize=400)

        # GUI elements
        self.file_path_label = tk.Label(self, text="file path")
        open_button = tk.Button(self, text="Open", command=self.open_file)

        analyze_button = tk.Button(self, text="Analyze", command=self.analyze)

        analysis_notebook = ttk.Notebook(self)

        cipher_label = tk.Label(self, text="Cipher")
        cipher_cbbox = ttk.Combobox(self, textvariable=self.cipher_name)
        cipher_cbbox['values'] = self.ciphers

        key_label = tk.Label(self, text="Key")
        self.key_entry = tk.Entry(self)
        decrypt_button = tk.Button(self, text="Decrypt", command=self.decrypt)

        preview_label = tk.Label(self, text="Preview")
        self.preview_message = tk.Message(self, text="Provide text input or select a file to upload.")
        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        save_button = tk.Button(self, text="Save", command=self.file_save)

        # Place widgets
        self.file_path_label.grid(row=0, column=0, sticky='nsw')
        open_button.grid(row=0, column=1, sticky='nsew')

        analyze_button.grid(row=1, column=0, columnspan=2, sticky='nsew')
        analysis_notebook.grid(row=2, column=0, columnspan=2, rowspan=2, sticky='nsew')

        cipher_label.grid(row=4, column=0, columnspan=2, sticky='nsew')
        cipher_cbbox.grid(row=5, column=0, columnspan=2, sticky='nsew')

        key_label.grid(row=6, column=0, columnspan=2, sticky='nsew')
        self.key_entry.grid(row=7, column=0, sticky='nsew')
        decrypt_button.grid(row=7, column=1, sticky='nsew')

        preview_label.grid(row=0, column=2, sticky='ns')
        self.preview_message.grid(row=1, column=2, rowspan=6, columnspan=3, sticky='nsew')
        back_button.grid(row=7, column=3, sticky='nsew')
        save_button.grid(row=7, column=4, sticky='nsew')

    def open_file(self):
        """
        Method for self.open_button
        Opens the file selector and returns selected file path into self.file_path_label
        """
        self.file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")], initialdir='~', title="Title")
        self.file_path_label["text"] = self.file_path
        self.read_file()

    def analyze(self):
        pass

    def read_file(self):
        """
        Converts file content into a string.
        That content is saved into self.plain_text, then stripped of all white spaces.
        :return:
        """
        self.cipher_text = ""
        tfile = open(self.file_path)
        for line in tfile:
            self.cipher_text += line
        self.cipher_text.strip()

    def decrypt(self):
        if self.cipher_name.get() == 'Transposition Cipher':
            self.cipher = TranspositionCipher()
        elif self.cipher_name.get() == 'Caesar Cipher':
            self.cipher = CaesarCipher()
        elif self.cipher_name.get() == 'Viginere Cipher':
            self.cipher = ViginereCipher()

        key = self.key_entry.get()
        self.plain_text = self.cipher.decrypt(self.cipher_text, key)

        self.preview_message['text'] = self.plain_text

    def file_save(self):
        """
        Method for self.save_button
        Allows user to save encrypted text with desired name
        """
        name = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        text_to_save = str(self.plain_text)
        name.write(text_to_save)
        name.close()


if __name__ == "__main__":
    app = CryptWing()
    app.geometry("1280x720")
    app.mainloop()