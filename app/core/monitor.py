from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time, os

# Função para configurar automaticamente o endereço da API no config.txt
def configure_api_url(api_url, config_path="config.txt"):
    lines = []
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    found = False
    for i, line in enumerate(lines):
        if line.startswith("api_url="):
            lines[i] = f"api_url={api_url}\n"
            found = True
            break
    if not found:
        lines.append(f"api_url={api_url}\n")
    with open(config_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
import requests
from api_client import excel_to_json, csv_to_json


class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(('.xlsx', '.csv')):
            print(f"Arquivo criado: {event.src_path}")
            enviar_relatorio(event.src_path)

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(('.xlsx', '.csv')):
            print(f"Arquivo modificado: {event.src_path}")
            enviar_relatorio(event.src_path)

    def on_moved(self, event):
        if not event.is_directory and event.dest_path.endswith(('.xlsx', '.csv')):
            print(f"Arquivo renomeado/movido: {event.dest_path}")
            enviar_relatorio(event.dest_path)

    def on_deleted(self, event):
        if not event.is_directory and event.src_path.endswith(('.xlsx', '.csv')):
            print(f"Arquivo removido: {event.src_path}")
            # Remove o JSON correspondente na API
            try:
                import requests
                import os
                filename = os.path.basename(event.src_path) + ".json"
                api_url = ''
                with open('config.txt', 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.startswith('api_url='):
                            api_url = line.strip().split('=',1)[1]
                if api_url:
                    delete_url = api_url.replace('/upload-json','/delete-json')
                    response = requests.delete(f"{delete_url}/{filename}")
                    print(f"Remoção do JSON na API: {response.status_code} {response.text}")
            except Exception as e:
                print(f"Erro ao remover JSON na API: {e}")

def enviar_relatorio(arquivo):
    # Lê config.txt para saber se é API
    modo_envio = 'API'
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
            # Extrai conteúdo para JSON
            if arquivo.endswith('.xlsx'):
                dados = excel_to_json(arquivo)
            elif arquivo.endswith('.csv'):
                dados = csv_to_json(arquivo)
            else:
                print(f'Formato não suportado: {arquivo}')
                return
            response = requests.post(api_url, json={"filename": os.path.basename(arquivo), "data": dados})
            if response.status_code == 200:
                print('Relatório enviado via API com sucesso!')
            else:
                print(f'Falha ao enviar via API: {response.status_code} {response.text}')
        except Exception as e:
            print(f'Erro no envio via API: {e}')
    else:
        print('Envio por API.')

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
    # Configura automaticamente o endereço da API
    api_url_padrao = "http://148.230.73.61:8000/upload-json"
    configure_api_url(api_url_padrao)

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