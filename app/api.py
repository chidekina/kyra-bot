
from fastapi import FastAPI, UploadFile, File, Request, status
from fastapi.responses import FileResponse, JSONResponse
import os
import json

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/view-json/{filename}")
def view_json(filename: str):
    json_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return JSONResponse(content=data)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JSONResponse({"error": "Arquivo não encontrado."}, status_code=status.HTTP_404_NOT_FOUND)

@app.delete("/delete-json/{filename}")
def delete_json(filename: str):
    json_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(json_path):
        try:
            os.remove(json_path)
            return JSONResponse({"message": f"Arquivo {filename} removido."}, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JSONResponse({"error": "Arquivo não encontrado."}, status_code=status.HTTP_404_NOT_FOUND)

@app.get("/list-files")
def list_files():
    try:
        files = os.listdir(UPLOAD_DIR)
        return {"files": files}
    except Exception as e:
        return {"error": str(e)}

# Recebe arquivo para upload
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"filename": file.filename}

# Recebe JSON extraído do Excel/CSV
@app.post("/upload-json")
async def upload_json(request: Request):
    data = await request.json()
    filename = data.get("filename", "data.json")
    content = data.get("data", {})
    # Salva o JSON recebido em arquivo
    json_path = os.path.join(UPLOAD_DIR, filename + ".json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
    return JSONResponse({"message": "JSON recebido e salvo", "filename": filename + ".json"})

@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename)
    return {"error": "Arquivo não encontrado"}

@app.get("/")
def root():
    return {"message": "API do Kyra Bot está rodando!"}

@app.get("/list-files")
def list_files():
    try:
        files = os.listdir(UPLOAD_DIR)
        return {"files": files}
    except Exception as e:
        return {"error": str(e)}

# Recebe arquivo para upload
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"filename": file.filename}

# Recebe JSON extraído do Excel/CSV
@app.post("/upload-json")
async def upload_json(request: Request):
    data = await request.json()
    filename = data.get("filename", "data.json")
    content = data.get("data", {})
    # Salva o JSON recebido em arquivo
    json_path = os.path.join(UPLOAD_DIR, filename + ".json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
    return JSONResponse({"message": "JSON recebido e salvo", "filename": filename + ".json"})

@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename)
    return {"error": "Arquivo não encontrado"}

@app.get("/")
def root():
    return {"message": "API do Kyra Bot está rodando!"}
