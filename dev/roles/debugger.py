# roles/debugger.py
from llm import call_model
from utils import extract_json

PROMPT = """Eres un experto en debugging.
Analiza la traza o el mensaje de error y devuelve SOLO JSON:
{{
  "root_cause": "...",
  "affected_files": ["file1","file2"],
  "fix_strategy": "pasos concretos para solucionar"
}}
Error: {error}
"""

def analyze_error(error_text: str):
    prompt = PROMPT.format(error=error_text)
    out = call_model(prompt, model_key="debug")
    ok, parsed = extract_json(out)
    if ok:
        return parsed
    return {"root_cause": "unknown", "affected_files": [], "fix_strategy": "Revisar logs"}
