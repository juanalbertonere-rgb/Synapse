# roles/fixer.py
from llm import call_model
from utils import parse_coder_output

PROMPT = """Eres un ingeniero de software.
Tienes un archivo con un error. Corrige el/los archivos y devuelve SOLO el código corregido en el mismo formato:
### filename
<codigo>

No expliques nada.
ErrorContext: {error}
Files: {files}
"""

def fix_code(files: dict, error: str):
    # serializar files en texto para pasarlo al modelo
    files_text = ""
    for k,v in files.items():
        files_text += "### " + k + "\n" + v + "\n"
    prompt = PROMPT.format(error=error, files=files_text)
    out = call_model(prompt, model_key="fix", max_tokens=3000)
    return parse_coder_output(out)
