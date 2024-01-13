import tkinter as tk
import threading
import config

root = None
break_interface = threading.Event()
chat_text1 = None
chat_text2_top = None
chat_text2_bottom = None
user_input_entry = None
user_input = ""

def get_user_input():
    global user_input
    actual_input = user_input
    user_input = ""
    return actual_input

def create_interface():
    global root, chat_text1, chat_text2_top, chat_text2_bottom, user_input_entry
    root = tk.Tk()
    root.title(f"{config.assistant_name} {config.assistant_lastname}")
    root.geometry("1400x400")
    root.iconbitmap("icone.ico")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.configure(bg="gray")

    image = tk.PhotoImage(file="jorge.png")
    image = image.subsample(3, 3)
    image_label = tk.Label(root, image=image, bg="white")
    image_label.grid(row=0, column=0, padx=10, pady=10, rowspan=3)

    chat_frame1 = tk.Frame(root, bg="black")
    chat_frame1.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    chat_frame2 = tk.Frame(root, bg="black")
    chat_frame2.grid(row=0, column=2, padx=10, pady=10, rowspan=3, sticky="nsew")

    chat_text_font = ("Arial", 16)

    chat_text1 = tk.Text(chat_frame1, wrap=tk.WORD, width=40, height=10, bg="black", fg="white", font=chat_text_font)
    chat_text1.config(state=tk.DISABLED)
    chat_text1.pack(expand=True, fill="both")

    chat_text2_top = tk.Text(chat_frame2, wrap=tk.WORD, width=40, height=5, bg="black", fg="white", font=chat_text_font)
    chat_text2_top.config(state=tk.DISABLED)
    chat_text2_top.pack(expand=True, fill="both")

    chat_text2_bottom = tk.Text(chat_frame2, wrap=tk.WORD, width=40, height=5, bg="black", fg="white", font=chat_text_font)
    chat_text2_bottom.config(state=tk.DISABLED)
    chat_text2_bottom.pack(expand=True, fill="both")

    user_input_entry = tk.Entry(root, font=chat_text_font, bg="black", fg="white")
    user_input_entry.grid(row=3, column=1, pady=10, padx=10, sticky="ew")
    user_input_entry.bind("<Return>", send_message)

    send_button = tk.Button(root, text="Enviar", command=send_message)
    send_button.grid(row=3, column=1, pady=10, padx=0, sticky="e")

    fechar_button = tk.Button(root, text="Fechar", command=close_window)
    fechar_button.grid(row=3, column=0, columnspan=1)

    root.mainloop()

def close_window():
    root.destroy()
    break_interface.set()

def send_message(event=None):
    global user_input
    user_input = user_input_entry.get()
    user_input_entry.delete(0, tk.END)

def show_message_assistant(message):
    chat_text1.config(state=tk.NORMAL)
    chat_text1.delete(1.0, tk.END)
    chat_text1.insert(tk.END, message + "\n")
    chat_text1.config(state=tk.DISABLED)

def show_message_user(message):
    chat_text2_top.config(state=tk.NORMAL)
    chat_text2_top.delete(1.0, tk.END)
    chat_text2_top.insert(tk.END, message + "\n")
    chat_text2_top.config(state=tk.DISABLED)

def show_message_search_result(message):
    chat_text2_bottom.config(state=tk.NORMAL)
    chat_text2_bottom.delete(1.0, tk.END)
    chat_text2_bottom.insert(tk.END, message + "\n")
    chat_text2_bottom.config(state=tk.DISABLED)

interface_thread = threading.Thread(target=create_interface)
interface_thread.daemon = True
interface_thread.start()
