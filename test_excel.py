from app.core.api_client import download_file, excel_to_json, csv_to_json

# Nome dos arquivos para testar
excel_filename = "teste.xlsx"
csv_filename = "teste.csv"

# Baixa os arquivos da API (se já estiver local, pode pular estas linhas)
download_file(excel_filename, excel_filename)
download_file(csv_filename, csv_filename)

# Extrai o conteúdo para JSON
print("Conteúdo do Excel:")
print(excel_to_json(excel_filename))

print("Conteúdo do CSV:")
print(csv_to_json(csv_filename))
