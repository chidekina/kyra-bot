import tkinter as tk
from tkinter import filedialog, scrolledtext
import threading, time, os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuração inicial
user_config = {
    'sistema': '',
    'pasta': '',
    'envio': '',
    'api_url': '',
}



# Monitoramento
class Handler(FileSystemEventHandler):
    def __init__(self, chat_callback):
        self.chat_callback = chat_callback
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(('.xlsx', '.csv')):
            self.chat_callback(f"Novo relatório detectado: {event.src_path}")
            # Aqui pode chamar envio por API

class MonitorThread(threading.Thread):
    def __init__(self, pasta, chat_callback):
        super().__init__()
        self.pasta = pasta
        self.chat_callback = chat_callback
        self._stop_event = threading.Event()
    def run(self):
        observer = Observer()
        observer.schedule(Handler(self.chat_callback), self.pasta, recursive=False)
        observer.start()
        self.chat_callback(f"Monitorando pasta: {self.pasta}")
        try:
            while not self._stop_event.is_set():
                time.sleep(1)
        finally:
            observer.stop()
            observer.join()
    def stop(self):
        self._stop_event.set()

# Interface
class App:
    def __init__(self, root):
        self.root = root
        self.root.title('Clearwave Agente Interativo')
        self.root.geometry('600x500')
        self.chat_box = scrolledtext.ScrolledText(root, state='disabled', wrap='word')
        self.chat_box.pack(fill='both', expand=True, padx=10, pady=10)
        self.entrada = tk.Entry(root)
        self.entrada.pack(fill='x', padx=10, pady=(0,10))
        self.entrada.bind('<Return>', lambda event: self.enviar())
        self.btn = tk.Button(root, text='Enviar', command=self.enviar)
        self.btn.pack(pady=(0,10))
        self.monitor_thread = None
        self.perguntar_config()
    def chat_append(self, msg):
        self.chat_box.config(state='normal')
        self.chat_box.insert(tk.END, msg + '\n')
        self.chat_box.config(state='disabled')
        self.chat_box.see(tk.END)
    def perguntar_config(self):
        self.chat_append('Olá! Sou o agente Clearwave. Vamos configurar o sistema.')
        self.chat_append('Qual sistema você usa? (Windows, Linux, MacOS, Outro)')
    def enviar(self):
        texto = self.entrada.get().strip().lower()
        if not texto:
            return
        self.chat_append(f'Você: {texto}')
        self.entrada.delete(0, tk.END)
        if not user_config['sistema']:
            user_config['sistema'] = texto
            self.chat_append('Qual pasta deseja monitorar? (Clique em "Selecionar pasta")')
            btn_pasta = tk.Button(self.root, text='Selecionar pasta', command=self.selecionar_pasta)
            btn_pasta.pack(pady=5)
            self.btn.config(state='disabled')
            return
        if not user_config['pasta']:
            self.chat_append('Por favor, selecione a pasta usando o botão acima.')
            return
        if not user_config['envio']:
            user_config['envio'] = texto
            self.chat_append('Informe o endpoint da API.')
            return
        envio = user_config['envio'].lower()
        # Aceita apenas API para iniciar monitoramento
        if envio == 'api' and not user_config['api_url']:
            user_config['api_url'] = texto
            self.chat_append('Configuração concluída! Monitoramento iniciado.')
            self.iniciar_monitoramento()
            return
        if envio == 'API':
            self.chat_append('Configuração concluída! Monitoramento iniciado.')
            self.iniciar_monitoramento()
            return
        # ...apenas interface e monitoramento, sem chat GPT...
    def selecionar_pasta(self):
        pasta = filedialog.askdirectory()
        if pasta:
            user_config['pasta'] = pasta
            self.chat_append(f'Pasta selecionada: {pasta}')
            self.chat_append('Deseja enviar por API?')
            self.btn.config(state='normal')
    def iniciar_monitoramento(self):
        self.monitor_thread = MonitorThread(user_config['pasta'], self.chat_append)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
