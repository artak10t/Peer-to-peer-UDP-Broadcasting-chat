import tkinter as tk
from tkinter import messagebox
import broadcast

# Init
authorize_window = tk.Tk()
authorize_window.geometry('250x120')
authorize_window.resizable(False, False)
authorize_window.title('Authorize')
authorize_window.iconbitmap('key.ico')

# Authorize
authorize_name = tk.StringVar()
authorize_name.set('Unknown')
authorize_port = tk.IntVar()
authorize_port.set(25057)

def authorize():
    if(len(authorize_name.get()) == 0):
        messagebox.showinfo("Message", "Please enter your name")
        return

    if(authorize_port.get() <= 0 or authorize_port.get() > 40000):
        messagebox.showinfo("Message", "Please enter valid port number")
        return

    authorize_window.destroy()
    broadcast.init(authorize_name.get(), authorize_port.get())

name_label = tk.Label(authorize_window, text = 'Name', font=('calibre', 10, 'bold'))
name_label.pack()
name_entry = tk.Entry(authorize_window, textvariable = authorize_name, font=('calibre', 10,'normal'))
name_entry.pack()
port_label = tk.Label(authorize_window, text = 'Port', font = ('calibre', 10,'bold'))
port_label.pack()
port_entry = tk.Entry(authorize_window, textvariable = authorize_port, font = ('calibre', 10,'normal'))
port_entry.pack()
sub_btn = tk.Button(authorize_window, text = 'Authorize', command = authorize)
sub_btn.pack()

authorize_window.bind('<Return>', lambda event: authorize())

authorize_window.mainloop()