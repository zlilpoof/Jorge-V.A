import tkinter as tk
import threading

root = None
encerrar_interface = threading.Event()
chat_text1 = None
chat_text2_top = None
chat_text2_bottom = None

def criar_interface_grafica():
    global root, chat_text1, chat_text2_top, chat_text2_bottom
    root = tk.Tk()
    root.title("Jorge Bagre")
    root.geometry("1400x400")
    root.iconbitmap("icone.ico")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.configure(bg="gray")

    imagem = tk.PhotoImage(file="jorge.png")
    imagem = imagem.subsample(3, 3)
    imagem_label = tk.Label(root, image=imagem, bg="white")
    imagem_label.grid(row=0, column=0, padx=10, pady=10, rowspan=3)

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

    fechar_button = tk.Button(root, text="Fechar", command=fechar_janela)
    fechar_button.grid(row=3, column=0, columnspan=3)

    root.mainloop()

def fechar_janela():
    root.destroy()
    encerrar_interface.set()

def exibir_mensagem(mensagem):
    chat_text1.config(state=tk.NORMAL)
    chat_text1.delete(1.0, tk.END)
    chat_text1.insert(tk.END, mensagem + "\n")
    chat_text1.config(state=tk.DISABLED)
    
def exibir_mensagem_chat2(mensagem):
    chat_text2_top.config(state=tk.NORMAL)
    chat_text2_top.delete(1.0, tk.END)
    chat_text2_top.insert(tk.END, mensagem + "\n")
    chat_text2_top.config(state=tk.DISABLED)

def exibir_mensagem_chat3(mensagem):
    chat_text2_bottom.config(state=tk.NORMAL)
    chat_text2_bottom.delete(1.0, tk.END)
    chat_text2_bottom.insert(tk.END, mensagem + "\n")
    chat_text2_bottom.config(state=tk.DISABLED)

interface_thread = threading.Thread(target=criar_interface_grafica)
interface_thread.daemon = True
interface_thread.start()