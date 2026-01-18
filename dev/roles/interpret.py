# roles/interpret.py
from llm import call_model
from utils import extract_json

PROMPT = """Eres un analista de software senior.
Interpreta la idea del usuario y devuelve SOLO JSON válido con estos campos:
- goal (string)
- platform (one of: windows, linux, cross)
- app_type (one of: cli, gui, service, library)
- constraints (list of strings)
- assumptions (list of strings)

No expliques nada, devuelve solamente JSON.
Usuario: {idea}
"""

def interpret(idea: str):
    prompt = PROMPT.format(idea=idea)
    out = call_model(prompt, model_key="interpret")
    ok, parsed = extract_json(out)
    if ok:
        return parsed
    # si no parsea, devolvemos un fallback
    return {
        "goal": idea,
        "platform": "cross",
        "app_type": "cli",
        "constraints": [],
        "assumptions": []
    }
