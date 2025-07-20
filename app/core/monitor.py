from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time, os
import requests


class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(('.xlsx', '.csv')):
            print(f"Novo relatório detectado: {event.src_path}")
            enviar_relatorio(event.src_path)

def enviar_relatorio(arquivo):
    # Lê config.txt para saber se é email ou API
    modo_envio = 'E-mail'
    api_url = ''
    try:
        with open('config.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('envio='):
                    modo_envio = line.strip().split('=',1)[1]
                if line.startswith('api_url='):
                    api_url = line.strip().split('=',1)[1]
    except Exception as e:
        print(f'Erro ao ler config.txt: {e}')
        return

    if modo_envio.lower() == 'api' and api_url:
        if api_url.strip().upper() == 'SIMULACAO':
            print(f'[SIMULAÇÃO] Relatório {arquivo} seria enviado via API.')
            return
        try:
            with open(arquivo, 'rb') as f:
                files = {'file': (os.path.basename(arquivo), f, 'application/octet-stream')}
                response = requests.post(api_url, files=files)
            if response.status_code == 200:
                print('Relatório enviado via API com sucesso!')
            else:
                print(f'Falha ao enviar via API: {response.status_code} {response.text}')
        except Exception as e:
            print(f'Erro no envio via API: {e}')
    else:
        print('Envio por e-mail não implementado neste exemplo.')

def monitorar(path):
    observer = Observer()
    observer.schedule(Handler(), path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    pasta = ''
    try:
        with open('config.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('pasta='):
                    pasta = line.strip().split('=',1)[1]
    except Exception as e:
        print(f'Erro ao ler config.txt: {e}')
    if pasta:
        print(f'Monitorando pasta: {pasta}')
        monitorar(pasta)
    else:
        print('Caminho da pasta não configurado no config.txt')