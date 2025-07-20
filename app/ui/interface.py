
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

def selecionar_pasta():
    caminho = filedialog.askdirectory()
    pasta_var.set(caminho)

def salvar_config():
    config = {
        'sistema': sistema_var.get(),
        'sistema_outro': sistema_outro_var.get(),
        'pasta': pasta_var.get(),
        'frequencia': freq_var.get(),
        'envio': envio_var.get()
    }
    try:
        with open('config.txt', 'w', encoding='utf-8') as f:
            for k, v in config.items():
                f.write(f'{k}={v}\n')
        messagebox.showinfo('Configuração', 'Configuração salva com sucesso!')
    except Exception as e:
        messagebox.showerror('Erro', f'Falha ao salvar: {e}')

def iniciar():
    global sistema_var, sistema_outro_var, pasta_var, freq_var, envio_var
    root = tk.Tk()
    root.title('Instalador Clearwave')
    root.geometry('400x350')

    sistema_var = tk.StringVar()
    sistema_outro_var = tk.StringVar()
    pasta_var = tk.StringVar()
    freq_var = tk.StringVar()
    envio_var = tk.StringVar()

    # Sistema operacional
    tk.Label(root, text='Qual sistema você usa?').pack(anchor='w', padx=20, pady=(15,0))
    sistemas = ['Windows', 'Linux', 'MacOS', 'Outro']
    sistema_menu = ttk.Combobox(root, textvariable=sistema_var, values=sistemas, state='readonly')
    sistema_menu.pack(fill='x', padx=20)

    def sistema_selecionado(event):
        if sistema_var.get() == 'Outro':
            outro_entry.pack(fill='x', padx=20)
        else:
            outro_entry.pack_forget()
    sistema_menu.bind('<<ComboboxSelected>>', sistema_selecionado)
    outro_entry = tk.Entry(root, textvariable=sistema_outro_var)

    # Pasta dos relatórios
    tk.Label(root, text='Caminho onde os relatórios são salvos?').pack(anchor='w', padx=20, pady=(15,0))
    tk.Entry(root, textvariable=pasta_var).pack(fill='x', padx=20)
    tk.Button(root, text='Selecionar pasta', command=selecionar_pasta).pack(padx=20, pady=5)

    # Frequência
    tk.Label(root, text='Com que frequência os relatórios são salvos?').pack(anchor='w', padx=20, pady=(15,0))
    ttk.Combobox(root, textvariable=freq_var, values=['Diário', 'Semanal'], state='readonly').pack(fill='x', padx=20)

    # Envio
    tk.Label(root, text='Envio via API').pack(anchor='w', padx=20, pady=(15,0))
    ttk.Combobox(root, textvariable=envio_var, values=['API'], state='readonly').pack(fill='x', padx=20)

    tk.Button(root, text='Salvar configuração', command=salvar_config).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    iniciar()