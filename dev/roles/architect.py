# roles/architect.py
import json
from llm import call_model
from utils import extract_json

PROMPT = """Eres un arquitecto de software.
Diseña la estructura mínima del proyecto y devuelve SOLO JSON:
{{
 "language": "python|csharp|cpp|js",
 "framework": "tkinter|winforms|qt|none|flask",
 "folders": ["src","tests"],
 "files": [{{"name":"main.py","responsibility":"..."}}],
 "dependencies": ["..."]
}}
Nada más.
Plan: {plan}
"""

def architect(plan: dict):
    prompt = PROMPT.format(plan=json.dumps(plan))
    out = call_model(prompt, model_key="architect")
    ok, parsed = extract_json(out)
    if ok:
        return parsed
    # fallback
    return {
        "language": "python",
        "framework": "tkinter" if plan.get("flow") else "none",
        "folders": ["project"],
        "files": [{"name":"main.py","responsibility": plan.get("features",[{}])[0].get("description","core")}],
        "dependencies": []
    }

