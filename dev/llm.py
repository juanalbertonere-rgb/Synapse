# llm.py (reemplazar por completo)
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise RuntimeError("Pon tu OPENROUTER_API_KEY en .env (mira .env.example)")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Mapea las keys a los modelos que quieres usar
MODELS = {
    "interpret": "openai/gpt-oss-120b",
    "plan": "nous/hermes-3-405b",
    "architect": "nous/hermes-3-405b",
    "code": "qwen/qwen3-coder-480b-a35b",
    "fix": "mistralai/devstral-2-2512",
    "debug": "deepseek/deepseek-r1-0528"
}

def _parse_response(resp_json):
    """
    Intentos robustos de extraer el texto de la respuesta en los formatos más comunes.
    """
    # 1) OpenRouter estilo Chat completions: choices[0].message.content
    try:
        return resp_json["choices"][0]["message"]["content"]
    except Exception:
        pass
    # 2) Otro estilo: choices[0].text
    try:
        return resp_json["choices"][0]["text"]
    except Exception:
        pass
    # 3) Algunos endpoints usan 'output' o 'result'
    for key in ("output", "result", "response"):
        if key in resp_json:
            v = resp_json[key]
            if isinstance(v, str):
                return v
            if isinstance(v, list) and v:
                return v[0]
    # fallback: stringify entire body
    return json.dumps(resp_json, indent=2, ensure_ascii=False)

def call_model(prompt: str, model_key: str = "interpret", max_tokens: int = 2000,
               temperature: float = 0.0, fallback_once: bool = True):
    """
    Llama al modelo indicado en MODELS. Si falla con HTTP error, mostramos el body
    y (si fallback_once) reintentamos con el modelo 'interpret' para no bloquear el flujo.
    """
    model = MODELS.get(model_key, model_key)
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature
    }

    try:
        r = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=60)
    except requests.RequestException as e:
        # fallo de conexión (timeout, DNS, etc.)
        raise RuntimeError(f"Error de red al llamar OpenRouter: {e}")

    if r.status_code != 200:
        # mostrar info de diagnóstico para que sepas por qué falló
        body_preview = r.text[:4000]  # limitar tamaño
        err_msg = (
            f"OpenRouter HTTP {r.status_code}.\n"
            f"Modelo solicitado: {model} (key: {model_key})\n"
            f"Respuesta (primeros 4000 chars):\n{body_preview}"
        )
        # Si pedimos fallback, reintentar con interpret para no detener todo el pipeline
        if fallback_once and model_key != "interpret":
            try:
                # intenta fallback con modelo de interpretación (más robusto)
                return call_model(prompt, model_key="interpret", max_tokens=max_tokens,
                                  temperature=temperature, fallback_once=False)
            except Exception:
                # si fallback también falla, lanzar error con body
                raise RuntimeError(err_msg)
        else:
            raise RuntimeError(err_msg)

    # extraer y devolver el contenido útil
    try:
        resp_json = r.json()
    except Exception:
        return r.text

    return _parse_response(resp_json)
