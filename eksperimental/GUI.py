import tkinter as tk
import requests
import socket

def perform_action():
    selection = selected_option.get()
    ip_address = get_server_ip() 

    if selection == "Cached Join":
        response = requests.get(f'http://{ip_address}:5000/cached_operations')
    else:
        response = requests.get(f'http://{ip_address}:5000/non_cached_operations')

    if response.status_code == 200:
        data = response.json()
        message = data.get('message', 'N/A')
        response_time = data.get('read_response_time', 'N/A')
        response_label.config(text=f"Operation Message: {message}\nRead Response Time: {response_time} seconds")
    else:
        response_label.config(text="Error occurred")

def get_server_ip():
    try:
        
        return socket.gethostbyname(socket.gethostname())
    except:
        return '127.0.0.1'  

# Tkinter GUI setup
root = tk.Tk()
root.title("Read Response Time Tester")

# Dropdown menu
options = ["Cached Join", "Non-Cached Join"]
selected_option = tk.StringVar(root)
selected_option.set(options[0]) 
dropdown = tk.OptionMenu(root, selected_option, *options)
dropdown.pack()


action_button = tk.Button(root, text="Start Action", command=perform_action)
action_button.pack()


response_label = tk.Label(root, text="Operation Message: -\nRead Response Time: -")
response_label.pack()

root.mainloop()
