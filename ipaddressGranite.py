import json
import os
import sys
import ctypes
import tkinter as tk
from tkinter import messagebox, font



#comment test
# Function to unhide a file
def unhide_file(file_path):
    try:
        attrs = ctypes.windll.kernel32.GetFileAttributesW(file_path)
        if attrs & 2:  # FILE_ATTRIBUTE_HIDDEN is 0x2
            ctypes.windll.kernel32.SetFileAttributesW(file_path, attrs & ~2)  # Remove hidden attribute
    except Exception as e:
        print(f"Failed to unhide file: {e}")

# Function to hide a file
def hide_file(file_path):
    try:
        ctypes.windll.kernel32.SetFileAttributesW(file_path, 2)  # FILE_ATTRIBUTE_HIDDEN is 0x2
    except Exception as e:
        print(f"Failed to hide file: {e}")

# Determine the storage path for both JSON files
def get_storage_path(file_name):
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), file_name)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)

STORAGE_FILE_1 = get_storage_path('selected_ip_id.json')
STORAGE_FILE_2 = get_storage_path('selected_ip_id_range2.json')

# Function to load selected IP and System ID pairs from a given JSON file
def load_selected_ip_id(file):
    unhide_file(file)  # Unhide the file before loading
    if os.path.exists(file):
        if os.path.getsize(file) > 0:
            with open(file, 'r') as f:
                try:
                    data = json.load(f)
                    hide_file(file)  # Hide again after successful reading
                    return data
                except json.JSONDecodeError:
                    print(f"Error: {file} is corrupted or empty. Initializing empty list.")
                    hide_file(file)  # Ensure hiding again even in case of failure
                    return []
        hide_file(file)  # Hide if the file is empty
        return []
    return []

# Function to save selected IP and System ID pairs to a given JSON file
def save_selected_ip_id(file, selected_pairs):
    unhide_file(file)  # Unhide the file before saving
    try:
        with open(file, 'w') as f:
            json.dump(selected_pairs, f)
        hide_file(file)  # Hide again after saving
    except Exception as e:
        print(f"Failed to save file: {e}")
        hide_file(file)  # Ensure it's hidden again even on failure

# Remaining code for GUI, IP generation, and interaction stays the same...


# Function to generate IP/ID array for the first range
def generate_ip_id_array_1(start_ip, end_ip, start_id, end_id):
    start_ip_parts = list(map(int, start_ip.split('.')))
    current_ip_parts = start_ip_parts[:]
    current_id = start_id
    ip_id_array = []

    while current_id <= end_id:
        current_ip = f"{current_ip_parts[0]}.{current_ip_parts[1]}.{current_ip_parts[2]}.{current_ip_parts[3]}"
        ip_id_array.append((current_ip, current_id))
        current_ip_parts[3] += 1
        if current_ip_parts[3] > 255:
            current_ip_parts[3] = 0
            current_ip_parts[2] += 1
        if current_ip_parts[2] > int(end_ip.split('.')[2]):
            break
        current_id += 1

    return ip_id_array

# Function to generate IP/ID array for the second range
def generate_ip_id_array_2(start_ip, end_ip, start_id, end_id):
    start_ip_parts = list(map(int, start_ip.split('.')))
    current_ip_parts = [start_ip_parts[0], start_ip_parts[1], 130, 229]
    current_id = 13229
    ip_id_array = []

    while current_id <= end_id:
        current_ip = f"{current_ip_parts[0]}.{current_ip_parts[1]}.{current_ip_parts[2]}.{current_ip_parts[3]}"
        ip_id_array.append((current_ip, current_id))
        current_ip_parts[3] += 1
        if current_ip_parts[3] > 238:
            break
        current_id += 1

    return ip_id_array

# Function to get the first available IP/ID pair for range 1
def get_first_available_ip_id_1():
    selected_pairs = load_selected_ip_id(STORAGE_FILE_1)
    start_ip = '20.200.200.76'
    end_ip = '20.200.200.237'
    start_id = 20076
    end_id = 20237
    ip_id_array = generate_ip_id_array_1(start_ip, end_ip, start_id, end_id)

    existing_pairs_set = set(tuple(pair) for pair in selected_pairs)
    available_ip_id = [pair for pair in ip_id_array if tuple(pair) not in existing_pairs_set]

    if available_ip_id:
        first_available = available_ip_id[0]
        selected_pairs.append(first_available)
        save_selected_ip_id(STORAGE_FILE_1, selected_pairs)
        return first_available
    return None

# Function to get the first available IP/ID pair for range 2
def get_first_available_ip_id_2():
    selected_pairs = load_selected_ip_id(STORAGE_FILE_2)
    start_ip = '10.100.120.195'
    end_ip = '10.100.130.238'
    start_id = 13229
    end_id = 13238
    ip_id_array = generate_ip_id_array_2(start_ip, end_ip, start_id, end_id)

    existing_pairs_set = set(tuple(pair) for pair in selected_pairs)
    available_ip_id = [pair for pair in ip_id_array if tuple(pair) not in existing_pairs_set]

    if available_ip_id:
        first_available = available_ip_id[0]
        selected_pairs.append(first_available)
        save_selected_ip_id(STORAGE_FILE_2, selected_pairs)
        return first_available
    return None

# GUI functions to display the first available IP/ID for each range
def show_first_available_1():
    first_available = get_first_available_ip_id_1()
    if first_available:
        display_value = f"System ID: {first_available[1]} -> IP: {first_available[0]}"
        output_label_1.config(text=display_value)
        root.clipboard_clear()
        root.clipboard_append(display_value)
        messagebox.showinfo("Copied to Clipboard", "The IP and System ID has been copied to the clipboard.")
    else:
        output_label_1.config(text="No available IP and System ID in the given range.")

def show_first_available_2():
    first_available = get_first_available_ip_id_2()
    if first_available:
        display_value = f"System ID: {first_available[1]} -> IP: {first_available[0]}"
        output_label_2.config(text=display_value)
        root.clipboard_clear()
        root.clipboard_append(display_value)
        messagebox.showinfo("Copied to Clipboard", "The IP and System ID has been copied to the clipboard.")
    else:
        output_label_2.config(text="No available IP and System ID in the given range.")

# Setting up the GUI
root = tk.Tk()
root.title("IP and System ID Tracker")
root.geometry("400x400")
root.configure(bg="#f0f0f0")

custom_font = font.Font(family="Helvetica", size=12)

# Create buttons and labels for the first range
button_1 = tk.Button(root, text="Show Next IP and System ID (PL)", command=show_first_available_1,
                     font=custom_font, bg="#4CAF50", fg="white", padx=10, pady=5, borderwidth=0)
button_1.pack(pady=20)
output_label_1 = tk.Label(root, text="", wraplength=300, bg="#f0f0f0", font=custom_font)
output_label_1.pack(pady=10)

# Create buttons and labels for the second range
button_2 = tk.Button(root, text="Show Next IP and System ID (PTL)", command=show_first_available_2,
                     font=custom_font, bg="#4CAF50", fg="white", padx=10, pady=5, borderwidth=0)
button_2.pack(pady=20)
output_label_2 = tk.Label(root, text="", wraplength=300, bg="#f0f0f0", font=custom_font)
output_label_2.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
