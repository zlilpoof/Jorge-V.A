import tkinter as tk
from tkinter import ttk
import threading
from config import settings
from users import user
import os

root = None
break_interface = threading.Event()
chat_text1 = None
chat_text2_top = None
chat_text2_bottom = None
mic_muted_button = None
sound_muted_button = None
user_input_entry = None
user_input = ""

def get_user_input():
    global user_input
    actual_input = user_input
    if actual_input != "":
        user_input = ""
        return actual_input
    

def open_menu():
    saved_questions = user.load_questions()
    saved_answers = user.load_answers()
    def save_data():
        questions = []
        answers = []
        for item in tree.get_children():
            if tree.item(item)["values"][0] != "": questions.append(tree.item(item)["values"][0])
            if tree.item(item)["values"][1] != "": answers.append(tree.item(item)["values"][1])
            settings.save(questions=questions, answers=answers)
        menu_window.destroy()

    menu_window = tk.Toplevel(root)
    menu_window.title("Menu")
    menu_window.geometry("600x400")

    tree = ttk.Treeview(menu_window, columns=("Pergunta", "Resposta"), show="headings")
    tree.heading("Pergunta", text="Pergunta")
    tree.heading("Resposta", text="Resposta")


    num_filled_lines = len(saved_questions)
    num_empty_lines = 10 + num_filled_lines - len(saved_questions)

    for i in range(num_filled_lines):
        question = saved_questions[i]
        answer = saved_answers[i]
        tree.insert("", "end", values=(question, answer))

    for _ in range(num_empty_lines):
        tree.insert("", "end", values=("", ""))

    tree.pack()

    def update_lists(event):
        if tree.selection():
            selected_item = tree.selection()[0]
            tree.item(selected_item, tags=('editable',))

    def edit_cell(event):
        cell = tree.focus()
        column = tree.identify_column(event.x)
        if column:
            col_index = int(column.replace("#", ""))
            bbox = tree.bbox(cell, column)
            if bbox:
                x, y, width, height = bbox
                entry = tk.Entry(menu_window, justify="center")
                entry.place(x=x, y=y, width=width, height=height)
                entry.insert(0, tree.item(cell, "values")[col_index - 1])
                entry.focus_set()
                entry.bind("<Return>", lambda _: update_cell(entry, cell, col_index - 1))
                entry.bind("<FocusOut>", lambda _: update_cell(entry, cell, col_index - 1))
                entry.bind("<Escape>", lambda _: entry.destroy())

    def update_cell(entry, cell, col_index):
        value = entry.get()
        tree.item(cell, values=(value if col_index == 0 else tree.item(cell, "values")[0],
                                 value if col_index == 1 else tree.item(cell, "values")[1]))
        entry.destroy()

    tree.bind("<FocusOut>", update_lists)
    tree.bind("<Double-1>", edit_cell)

    save_button = tk.Button(menu_window, text="Salvar", command=save_data)
    save_button.place(relx=0.5, rely=0.95, anchor=tk.CENTER)


def create_interface():
    global root, chat_text1, chat_text2_top, chat_text2_bottom, user_input_entry, mic_muted_button, sound_muted_button
    root = tk.Tk()
    root.title(f"{settings.assistant_name} {settings.assistant_lastname}")
    root.geometry("1400x400")
    icon_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'images', 'icone.ico'))
    root.iconbitmap(icon_path)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.configure(bg="gray")

    va_image_path = icon_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'images', 'jorge.png'))
    image = tk.PhotoImage(file=va_image_path)
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

    if settings.mic_muted:
        mic_muted_button = tk.Button(root, text="Microfone Muted", bg="red", command=mute_microfone)
        mic_muted_button.grid(row=3, column=2, pady=5, padx=100, sticky="w")
    else:
        mic_muted_button = tk.Button(root, text="Microfone Activated", bg="green", command=mute_microfone)
        mic_muted_button.grid(row=3, column=2, pady=5, padx=100, sticky="w")
    
    if settings.sound_muted:
        sound_muted_button = tk.Button(root, text="Sound Muted", bg="red", command=mute_sound)
        sound_muted_button.grid(row=3, column=2, pady=5, padx=100, sticky="e")
    else:
        sound_muted_button = tk.Button(root, text="Sound Activated", bg="green", command=mute_sound)
        sound_muted_button.grid(row=3, column=2, pady=5, padx=100, sticky="e")
    
    
    menu_button = tk.Button(root, text="Menu", command=open_menu)
    menu_button.grid(row=3, column=0, columnspan=1)

    root.mainloop()
    
def mute_microfone():
    global mic_muted_button
    _muted = settings.change_mic()
    if _muted:
        mic_muted_button.config(text="Microfone Muted", bg="red")
    else:
        mic_muted_button.config(text="Microfone Activated", bg="green")
        
def mute_sound():
    global sound_muted_button
    _muted = settings.change_sound()
    if _muted:
        sound_muted_button.config(text="Sound Muted", bg="red")
    else:
        sound_muted_button.config(text="Sound Activated", bg="green")

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
