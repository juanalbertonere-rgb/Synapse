# roles/coder.py
from llm import call_model
from utils import parse_coder_output

PROMPT = """Eres un programador senior.
Genera SOLO código funcional.
Entrega varios archivos con este formato EXACTO:

### filename
<codigo>

### another_file
<codigo>

No expliques, no uses markdown, no pongas texto fuera de bloques.
ProjectSpec: {spec}
"""

def generate_code(spec: dict):
    prompt = PROMPT.format(spec=spec)
    out = call_model(prompt, model_key="code", max_tokens=4000, temperature=0.0)
    files = parse_coder_output(out)
    return files
