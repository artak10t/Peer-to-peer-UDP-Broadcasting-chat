import tkinter as tk
from tkinter import messagebox
import socket
import threading
import time
import chat
import chat_serverside
from dataclasses import dataclass

BROADCAST_PORT = 25056

# Node struct
@dataclass
class Node:
    ip: str
    port: int
    name: str

global current_nodes
current_nodes = []

# Broadcast Socket
def broadcast():
    global is_window_destroyed
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcast_socket.settimeout(0.2)

    # Message
    global my_name
    global my_port
    broadcast_message = str(my_name + ':' + str(my_port)).encode('utf-8')

    while not is_window_destroyed:
        broadcast_socket.sendto(broadcast_message, ('<broadcast>', BROADCAST_PORT))
        time.sleep(0.2)

    print('Closing broadcast socket')
    broadcast_socket.close()

# Listen Socket
def listen():
    global is_window_destroyed
    global listen_socket
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    listen_socket.bind(("", BROADCAST_PORT))

    while not is_window_destroyed:
        data = ''
        addr = '0.0.0.0'
        try:
            data, addr = listen_socket.recvfrom(1024, )
        except:
            print('Closing listen socket')
            break

        exist_in_nodes = False

        # Decode data
        decoded_data = data.decode('utf-8')
        decoded_data = decoded_data.split(':')

        # Check if getting self broadcast
        global my_ip
        global my_port
        if (my_ip == addr[0] and str(my_port) == decoded_data[1]):
            exist_in_nodes = True

        # Check if node exists in current list
        for node in current_nodes:
            if(node.ip == addr[0] and node.port == decoded_data[1]):
                exist_in_nodes = True
                break

        # Add into current nodes list
        if not exist_in_nodes:
            node = Node(addr[0], decoded_data[1], decoded_data[0])
            current_nodes.append(node)

# Chat Server
def chat_server():
    global my_port
    global my_name
    global is_window_destroyed
    global client_socket
    global broadcast_window
    client_connections = 0

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.bind(("", my_port))
        client_socket.listen()
    except:
        print('Port in use')
        return
    
    while not is_window_destroyed:
        if(client_connections != 1):
                try:
                    client, address = client_socket.accept()
                    client_connections = 1
                    client_name = client.recv(1024).decode()
                    result = messagebox.askquestion("Accept Chat?", client_name + ' wants to chat')

                    if(result == 'no'):
                        data = 'NOTALLOWED'
                        client.send(data.encode())
                        client.close()
                        client_connections = 0
                    elif(result == 'yes'):
                        data = 'ALLOWED'
                        client.send(data.encode())
                        broadcast_window.withdraw()
                        chat_serverside.init(broadcast_window, my_name, client_name, client)
                except:
                    print('Closing chat socket')


# Open chat window on Chat With click
def chat_with(ip, port, name):
    global broadcast_window
    global my_name
    broadcast_window.withdraw()
    
    chat.init(broadcast_window, my_name, name, ip, port)

# Update UI with current nodes
def display_nodes():
    global broadcast_window
    global current_nodes

    # Clear Display
    for child in broadcast_window.winfo_children():
        child.destroy()

    # Populate Display
    for node in current_nodes:
        b = tk.Button(broadcast_window, 
                      text = 'Chat with ' + node.name + ' | ' + node.ip + ':' + str(node.port), 
                      command=lambda: chat_with(node.ip, node.port, node.name),
                      width=500)
        b.pack()
    
    current_nodes.clear()
    broadcast_window.after(1000, display_nodes)

def on_destroy():
    # Notify that window destroyed
    global is_window_destroyed
    global broadcast_window
    is_window_destroyed = True

    # Join Threads
    global thread_listen
    global thread_broadcast
    global thread_chat_server
        
    if thread_listen.is_alive():
        global listen_socket
        listen_socket.close()
        thread_listen.join()

    if thread_broadcast.is_alive():
        thread_broadcast.join()

    if thread_chat_server.is_alive():
        global client_socket
        client_socket.close()
        thread_chat_server.join()

    broadcast_window.destroy()

# Create broadcast window
def init(name, port):
    global my_name
    my_name = name

    global my_port
    my_port = port

    global my_ip
    my_ip = socket.gethostbyname(socket.gethostname())

    # Create Window
    global broadcast_window
    global is_window_destroyed
    is_window_destroyed = False
    broadcast_window = tk.Tk()
    broadcast_window.geometry('400x500')
    broadcast_window.resizable(False, False)
    broadcast_window.title('Welcome ' + name)
    broadcast_window.iconbitmap('broadcast.ico')
    broadcast_window.protocol("WM_DELETE_WINDOW", on_destroy)

    # Start Listening
    global thread_listen
    thread_listen = threading.Thread(target=listen)
    thread_listen.start()

    # Start Broadcasting
    global thread_broadcast
    thread_broadcast = threading.Thread(target=broadcast)
    thread_broadcast.start()

    # Start Chat Server
    global thread_chat_server
    thread_chat_server = threading.Thread(target=chat_server)
    thread_chat_server.start()

    # Update Nodes GUI Every 1 Seconds
    broadcast_window.after(1000, display_nodes)

    broadcast_window.mainloop()