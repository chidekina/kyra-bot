import os
from dotenv import load_dotenv
import requests
import pandas as pd

load_dotenv()
API_URL = os.getenv("API_URL")

def upload_file(file_path):
    url = f"{API_URL}/upload"
    with open(file_path, "rb") as f:
        files = {"file": (file_path, f)}
        response = requests.post(url, files=files)
    return response.json()

def download_file(filename, save_path):
    url = f"{API_URL}/download/{filename}"
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        return True
    return False

# Função para ler Excel e extrair para JSON
def excel_to_json(file_path):
    df = pd.read_excel(file_path, engine="openpyxl")
    return df.to_dict(orient="records")

# Função para ler CSV e extrair para JSON
def csv_to_json(file_path):
    df = pd.read_csv(file_path)
    return df.to_dict(orient="records")
