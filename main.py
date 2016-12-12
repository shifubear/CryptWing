import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from CryptWing.cipher import Cipher
from CryptWing.classical_ciphers import TranspositionCipher

LARGE_FONT = ("Verdana", 12)


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Encrypt", command=lambda: controller.show_frame(EncryptPage))
        button1.pack()

        button2 = tk.Button(self, text="Decrypt", command=lambda: controller.show_frame(DecryptPage))
        button2.pack()

        button3 = tk.Button(self, text="Graph", command=lambda: controller.show_frame(PageThree))
        button3.pack()


class EncryptPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.ciphers = ('Transposition Cipher', 'Caesar Cipher', 'RSA Cipher')

        self.input_mode = tk.StringVar()
        self.file_path = tk.StringVar()
        self.cipher_name = tk.StringVar()
        self.cipher = Cipher()
        self.plain_text = ""
        self.cipher_text = ""

        self.grid_columnconfigure(2, minsize=550)

        rb_text = tk.Radiobutton(self, text="Input text", variable=self.input_mode, value="text_mode", command=self.rb_pushed)
        self.clear_button = tk.Button(self, text="Clear", command=self.clear_text)
        self.input_text = tk.Text(self)

        rb_file = tk.Radiobutton(self, text="Read File", variable=self.input_mode, value="file_mode", command=self.rb_pushed)
        self.open_button = tk.Button(self, text="Open", command=self.open_file)
        self.file_path_label = tk.Label(self, text="file path")

        cipher_label = tk.Label(self, text="Cipher")
        cipher_cbbox = ttk.Combobox(self, textvariable=self.cipher_name)
        cipher_cbbox['values'] = self.ciphers
        key_label = tk.Label(self, text="Key")
        key_entry = tk.Entry(self)
        encrypt_button = tk.Button(self, text="Encrypt", command=self.encrypt)

        preview_label = tk.Label(self, text="Preview")
        self.preview_message = tk.Message(self, text="Lorem Ipsum")
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
        key_entry.grid(row=7, column=0, sticky='nsew')
        encrypt_button.grid(row=7, column=1, sticky='nsew')

        preview_label.grid(row=0, column=2, columnspan=3, sticky='ns')
        self.preview_message.grid(row=1, column=2, rowspan=6, columnspan=3, sticky='nsew')
        fat_label.grid(row=7, column=2)
        back_button.grid(row=7, column=3)
        save_button.grid(row=7, column=4)

    def clear_text(self):
        self.input_text.delete(1.0, tk.END)

    def open_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")], initialdir='~', title="Title")
        self.file_path_label["text"] = self.file_path
        self.read_file()

    def read_file(self):
        self.plain_text = ""
        tfile = open(self.file_path)
        for line in tfile:
            self.plain_text += line
        self.plain_text.strip()

    def rb_pushed(self):
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
        name = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        text_to_save = str(self.cipher_text)
        name.write(text_to_save)
        name.close()

    def encrypt(self):
        # 'Transposition Cipher', 'Caesar Cipher', 'RSA Cipher')
        if self.cipher_name.get() == 'Transposition Cipher':
            self.cipher = TranspositionCipher()

        if self.input_mode.get() == "text_mode":
            self.plain_text = self.input_text.get(1.0, tk.END)
        else:
            self.read_file()
        self.cipher_text = self.cipher.encrypt(self.plain_text)
        self.preview_message['text'] = self.cipher_text


class DecryptPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.ciphers = ('Transposition Cipher', 'Caesar Cipher', 'RSA Cipher')
        self.cipher_name = tk.StringVar()

        file_path_label = tk.Label(self, text="file path")
        open_button = tk.Button(self, text="Open")

        analyze_button = tk.Button(self, text="Analyze")

        analysis_notebook = ttk.Notebook(self)

        cipher_label = tk.Label(self, text="Cipher")
        cipher_cbbox = ttk.Combobox(self, textvariable=self.cipher_name)
        cipher_cbbox['values'] = self.ciphers

        key_label = tk.Label(self, text="Key")
        key_entry = tk.Entry(self)
        decrypt_button = tk.Button(self, text="Decrypt")

        # Place widgets
        file_path_label.grid(row=0, column=0, sticky='nsw')
        open_button.grid(row=0, column=1, sticky='nsew')

        analyze_button.grid(row=1, column=0, columnspan=2, sticky='nsew')
        analysis_notebook.grid(row=2, column=0, columnspan=2, rowspan=2, sticky='nsew')

        cipher_label.grid(row=4, column=0, columnspan=2, sticky='nsew')
        cipher_cbbox.grid(row=5, column=0, columnspan=2, sticky='nsew')

        key_label.grid(row=6, column=0, columnspan=2, sticky='nsew')
        key_entry.grid(row=7, column=0, sticky='nsew')
        decrypt_button.grid(row=7, column=1, sticky='nsew')



class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Go Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()

        # f for figure
        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8], [5,1,2,5,7,3,8,4])

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class CryptWing(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "CryptWing")

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        self.frames = {}

        for F in (StartPage, EncryptPage, DecryptPage, PageThree):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


if __name__ == "__main__":
    app = CryptWing()
    app.geometry("1280x720")
    app.mainloop()