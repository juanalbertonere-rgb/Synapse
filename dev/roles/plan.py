# roles/plan.py
import json
from llm import call_model
from utils import extract_json

PROMPT = """Eres un project manager técnico.
Divide el proyecto en fases y devuelve SOLO JSON:
{{
  "features": [{{"name": "...", "description":"..."}}],
  "flow": ["step1","step2", "..."],
  "priorities": ["must","should","could"]
}}
Nada de texto extra.
IdeaSpec: {spec}
"""

def plan_project(spec: dict):
    # serializamos spec a JSON para inyectarlo seguro en el prompt
    prompt = PROMPT.format(spec=json.dumps(spec))
    out = call_model(prompt, model_key="plan")
    ok, parsed = extract_json(out)
    if ok:
        return parsed
    # fallback simple si no parsea
    return {
        "features": [{"name": "core", "description": spec.get("goal", "")}],
        "flow": ["start", "run"],
        "priorities": ["must"]
    }

