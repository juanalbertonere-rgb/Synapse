# utils.py
import json
import re
import os
from typing import Dict, Tuple

def extract_json(text: str) -> Tuple[bool, object]:
    """
    Intenta extraer JSON de un texto. Devuelve (ok, parsed_or_raw).
    """
    # try direct parse
    try:
        parsed = json.loads(text)
        return True, parsed
    except Exception:
        pass

    # Buscar primer y último corchete/brace
    js_match = re.search(r'(\{[\s\S]*\}|\[[\s\S]*\])', text)
    if js_match:
        try:
            parsed = json.loads(js_match.group(1))
            return True, parsed
        except Exception:
            return False, js_match.group(1)
    return False, text

def parse_coder_output(text: str) -> Dict[str, str]:
    """
    Espera el formato:
    ### filename.ext
    <codigo>
    ### otherfile
    <codigo>
    Devuelve dict filename -> code
    """
    files = {}
    current = None
    buffer = []
    for line in text.splitlines():
        header = re.match(r"^###\s*(.+)$", line)
        if header:
            if current:
                files[current] = "\n".join(buffer).rstrip() + "\n"
            current = header.group(1).strip()
            buffer = []
        else:
            if current is None:
                # Ignorar texto fuera de bloques (puede pasar)
                continue
            buffer.append(line)
    if current:
        files[current] = "\n".join(buffer).rstrip() + "\n"
    return files

def write_project_files(base_path: str, files_dict: Dict[str, str]):
    os.makedirs(base_path, exist_ok=True)
    for fname, content in files_dict.items():
        fpath = os.path.join(base_path, fname)
        d = os.path.dirname(fpath)
        if d:
            os.makedirs(d, exist_ok=True)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)

def safe_filename(idea: str) -> str:
    name = re.sub(r'[^0-9a-zA-Z_\-]', '_', idea.strip())[:40]
    return name or "project"
