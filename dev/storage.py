# storage.py
import os
import json
import uuid
import shutil
from typing import Dict, Any
from builder import build_from_files

BASE = os.path.abspath(os.path.dirname(__file__))
STORAGE_DIR = os.path.join(BASE, "storage")
CHATS_DIR = os.path.join(STORAGE_DIR, "chats")
PROJECTS_DIR = os.path.join(STORAGE_DIR, "projects")
ZIPS_DIR = os.path.join(STORAGE_DIR, "zips")
MEM_DIR = os.path.join(STORAGE_DIR, "memory")

for d in (STORAGE_DIR, CHATS_DIR, PROJECTS_DIR, ZIPS_DIR, MEM_DIR):
    os.makedirs(d, exist_ok=True)

def new_chat(title: str = "Chat") -> str:
    chat_id = str(uuid.uuid4())
    path = os.path.join(CHATS_DIR, f"{chat_id}.json")
    data = {
        "id": chat_id,
        "title": title,
        "messages": []  # {"role":"user"|"assistant"|"system","text": "..."}
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    # create empty memory
    save_memory(chat_id, {"summary": "", "notes": []})
    return chat_id

def list_chats() -> Dict[str, Any]:
    chats = []
    for fname in os.listdir(CHATS_DIR):
        if fname.endswith(".json"):
            with open(os.path.join(CHATS_DIR, fname), "r", encoding="utf-8") as f:
                chats.append(json.load(f))
    return chats

def load_chat(chat_id: str) -> Dict[str, Any]:
    path = os.path.join(CHATS_DIR, f"{chat_id}.json")
    if not os.path.exists(path):
        raise FileNotFoundError("Chat no encontrado")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_chat(chat: Dict[str, Any]):
    path = os.path.join(CHATS_DIR, f"{chat['id']}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(chat, f, ensure_ascii=False, indent=2)

def load_memory(chat_id: str) -> Dict[str, Any]:
    path = os.path.join(MEM_DIR, f"{chat_id}.json")
    if not os.path.exists(path):
        return {"summary": "", "notes": []}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(chat_id: str, memory: Dict[str, Any]):
    path = os.path.join(MEM_DIR, f"{chat_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

def save_project_files(files_dict: Dict[str, str], project_name: str):
    """
    Usa builder.build_from_files para crear la estructura y devuelve path del proyecto.
    """
    # builder.build_from_files(files_dict, base_folder="projects", project_name=None)
    # Queremos guardar en storage/projects para el SaaS
    return build_from_files(files_dict, base_folder=PROJECTS_DIR, project_name=project_name)

def zip_project(project_path: str) -> str:
    """
    Crea un zip en storage/zips y devuelve la ruta absoluta al zip.
    """
    abs_proj = os.path.abspath(project_path)
    base_name = os.path.join(ZIPS_DIR, os.path.basename(project_path))
    # make_archive agrega .zip automáticamente
    zip_path = shutil.make_archive(base_name, 'zip', root_dir=abs_proj)
    return zip_path
