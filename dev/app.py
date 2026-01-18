# app.py (Flask version)
import os
from flask import Flask, request, jsonify, send_from_directory, abort
from llm import call_model
from storage import new_chat, list_chats, load_chat, save_chat, load_memory, save_memory, save_project_files, zip_project
from roles import interpret, plan_project, architect, generate_code

app = Flask(__name__, static_folder="web", static_url_path="/")

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/api/new_chat", methods=["POST"])
def api_new_chat():
    body = request.get_json(silent=True) or {}
    title = body.get("title", "Chat")
    chat_id = new_chat(title)
    return jsonify({"chat_id": chat_id})

@app.route("/api/chats", methods=["GET"])
def api_list_chats():
    chats = list_chats()
    return jsonify(chats)

@app.route("/api/chat/<chat_id>", methods=["GET"])
def api_get_chat(chat_id):
    try:
        return jsonify(load_chat(chat_id))
    except FileNotFoundError:
        abort(404, "Chat no encontrado")

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json(force=True)
    chat_id = data.get("chat_id")
    text = data.get("text", "")
    if not chat_id:
        chat_id = new_chat("Chat rápido")
    chat = load_chat(chat_id)
    chat["messages"].append({"role":"user","text":text})
    save_chat(chat)

    memory = load_memory(chat_id)
    recent = chat["messages"][-8:]
    prompt = f"""Eres un asistente que ayuda a generar proyectos de software.
Memoria breve: {memory.get('summary','')}
Conversación reciente:
"""
    for m in recent:
        prompt += f"{m['role']}: {m['text']}\n"
    prompt += "\nResponde como asistente profesional y conciso. Si se da una idea, sugiere el siguiente paso para generar el proyecto."

    reply = call_model(prompt, model_key="interpret", max_tokens=800, temperature=0.0)
    chat["messages"].append({"role":"assistant","text":reply})
    save_chat(chat)

    # resumir y guardar memoria (intento silencioso)
    try:
        mem_prompt = f"Resume en 1-2 frases lo más importante de esta conversación para usar en futuros chats: {text}"
        mem_short = call_model(mem_prompt, model_key="interpret", max_tokens=200, temperature=0.0)
    except Exception:
        mem_short = memory.get("summary","")
    memory["summary"] = mem_short
    save_memory(chat_id, memory)

    return jsonify({"chat_id": chat_id, "reply": reply})

@app.route("/api/generate", methods=["POST"])
def api_generate():
    data = request.get_json(force=True)
    idea = data.get("idea","")
    chat_id = data.get("chat_id")
    spec = interpret(idea)
    plan = plan_project(spec)
    arch = architect(plan)
    files = generate_code(arch)
    if not files:
        abort(500, "El coder no devolvió archivos")
    project_path = save_project_files(files, project_name=spec.get("goal","project"))
    zip_path = zip_project(project_path)
    if chat_id:
        try:
            chat = load_chat(chat_id)
            chat["messages"].append({"role":"system","text":f"Se generó proyecto: {os.path.basename(zip_path)}"})
            save_chat(chat)
        except Exception:
            pass
    return jsonify({"zip": os.path.basename(zip_path)})

@app.route("/download/<zipname>", methods=["GET"])
def api_download(zipname):
    path = os.path.join(os.path.dirname(__file__), "storage", "zips", zipname)
    if not os.path.exists(path):
        abort(404, "Zip no encontrado")
    return send_from_directory(os.path.dirname(path), os.path.basename(path), as_attachment=True)

if __name__ == "__main__":
    # puerto 8000 para paridad con instrucciones anteriores
    app.run(host="127.0.0.1", port=8000, debug=True)
