import os
import pandas as pd
# from PyPDF2 import PdfFileReader
from PyPDF2 import PdfReader
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        # List to store PDF data
        self.data = []

        # Create "+" button
        self.add_button = tk.Button(self, text="+", command=self.select_files)
        self.add_button.pack(side="left")

        # Create "Done" button
        self.done_button = tk.Button(self, text="Done", command=self.export_data)
        self.done_button.pack(side="left")

        # Create "Wipe" button
        self.wipe_button = tk.Button(self, text="Wipe", command=self.wipe_data)
        self.wipe_button.pack(side="left")

        # Bind drop event
        self.master.drop_target_register(DND_FILES)
        self.master.dnd_bind('<<Drop>>', self.drop_files)

    def select_files(self):
        files = filedialog.askopenfilenames(filetypes=[('PDF files', '*.pdf')])
        self.process_files(files)

    def drop_files(self, event):
        self.process_files(self.master.tk.splitlist(event.data))

    def process_files(self, files):
        for file in files:
            with open(file, 'rb') as f:
                reader = PdfReader(f)
                text = "".join(
                    reader.pages[page].extract_text()
                    for page in range(len(reader.pages))
                )
                self.data.append({'filename': os.path.basename(file), 'content': text})

    def export_data(self):
        if self.data:
            df = pd.DataFrame(self.data)
            df.to_csv('output.csv', index=False)
            messagebox.showinfo("Exported", "Data exported to output.csv")
            self.wipe_data()
        else:
            messagebox.showinfo("No Data", "No data to export")

    def wipe_data(self):
        self.data.clear()
        messagebox.showinfo("Wiped", "Data wiped")

    def extract_text_from_pdf(self):
        pdf = PdfReader(self)
        return "".join(page.extract_text() for page in pdf.pages)

root = TkinterDnD.Tk()
app = Application(master=root)
app.mainloop()
