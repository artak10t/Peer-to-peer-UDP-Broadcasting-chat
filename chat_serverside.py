import tkinter as tk
import threading

def recieve():
    global other_name
    global current_client

    while True:
        try:
            message = current_client.recv(1024).decode()
            if(message == 'DSCN'):
                messages_text.config(state=tk.NORMAL)
                messages_text.insert(tk.END, other_name + ': Disconnected\n')
                messages_text.config(state=tk.DISABLED)
                break
        
            messages_text.config(state=tk.NORMAL)
            messages_text.insert(tk.END, other_name + ': ' + message + '\n')
            messages_text.config(state=tk.DISABLED)
        except:
            break

def send_message(my_name, input_field):
    if(len(input_field.get()) == 0):
        return

    global messages_text
    global current_client

    try:
        current_client.send(input_field.get().encode())
    except:
        print('Timeout: Cannot send message')

    messages_text.config(state=tk.NORMAL)
    messages_text.insert(tk.END, my_name + ': ' + input_field.get() + '\n')
    messages_text.config(state=tk.DISABLED)
    input_field.delete(0, tk.END)

def on_destroy():
    global back_window
    global chat_window
    global current_client
    global thread_recieve

    if(current_client):
        try:
            final_message = 'DSCN'
            current_client.send(final_message.encode())
        except:
            print('Client already disconnected')
        current_client.close()

    thread_recieve.join()
    chat_window.destroy()
    back_window.deiconify()

def init(broadcast_window, my_name, name, client):
    global other_name
    global back_window
    global current_client
    other_name = name
    back_window = broadcast_window
    current_client = client

    # Create Window
    global chat_window
    chat_window = tk.Tk()
    chat_window.geometry('400x500')
    chat_window.resizable(False, False)
    chat_window.iconbitmap('chat.ico')
    chat_window.title('Chat with ' + name)
    chat_window.protocol("WM_DELETE_WINDOW", on_destroy)

    # Create and configure the main frame
    main_frame = tk.Frame(chat_window)
    main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Create and configure the messages text widget
    global messages_text
    messages_text = tk.Text(main_frame, height=15, width=50)
    messages_text.config(state=tk.DISABLED)
    messages_text.pack(fill=tk.BOTH, expand=True)

    # Create a frame for input field and send button
    input_frame = tk.Frame(main_frame)
    input_frame.pack(side=tk.BOTTOM, fill=tk.X)

    # Create and configure the input field
    input_field = tk.Entry(input_frame, width=50)
    input_field.pack(side=tk.LEFT, padx=5, pady=5)
    input_field.bind('<Return>', lambda event: send_message(my_name, input_field))

    # Create and configure the send button
    send_button = tk.Button(input_frame, text="Send", command=lambda: send_message(my_name, input_field))
    send_button.pack(side=tk.RIGHT, padx=5, pady=5)

    messages_text.config(state=tk.NORMAL)
    messages_text.insert(tk.END, name + ': ' + 'Connected\n')
    messages_text.config(state=tk.DISABLED)

    # Recieve upcoming messsages
    global thread_recieve
    thread_recieve = threading.Thread(target=recieve)
    thread_recieve.start()

    chat_window.mainloop()
