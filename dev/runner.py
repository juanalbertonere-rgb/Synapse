# runner.py
import os
import sys
import subprocess
import time
from roles import analyze_error, fix_code
from utils import safe_filename

def read_py_files(project_path):
    files = {}
    for root, _, fnames in os.walk(project_path):
        for f in fnames:
            if f.endswith(".py"):
                full = os.path.join(root, f)
                rel = os.path.relpath(full, project_path).replace("\\", "/")
                with open(full, "r", encoding="utf-8") as fh:
                    files[rel] = fh.read()
    return files

def write_fixed_files(project_path, fixes: dict):
    for fname, content in fixes.items():
        # fname puede venir como "src/main.py" o "main.py"
        target = os.path.join(project_path, fname)
        d = os.path.dirname(target)
        if d and not os.path.exists(d):
            os.makedirs(d, exist_ok=True)
        with open(target, "w", encoding="utf-8") as fh:
            fh.write(content)

def run_entry(project_path, entry_rel="src/main.py", timeout=20):
    entry = os.path.join(project_path, entry_rel)
    if not os.path.exists(entry):
        # intentar con main.py en root
        candidate = os.path.join(project_path, "main.py")
        if os.path.exists(candidate):
            entry = candidate
        else:
            raise FileNotFoundError(f"No se encontró el entry point ({entry_rel}) en {project_path}")
    proc = subprocess.run([sys.executable, entry], cwd=project_path,
                          capture_output=True, text=True, timeout=timeout)
    return proc.returncode, proc.stdout, proc.stderr

def auto_fix_loop(project_path, entry_rel="src/main.py", max_attempts=3):
    print("Runner: iniciando loop de ejecución y autocorrección en:", project_path)
    for attempt in range(1, max_attempts + 1):
        print(f"\n=== Attempt {attempt}/{max_attempts} ===")
        try:
            code, out, err = run_entry(project_path, entry_rel=entry_rel)
        except subprocess.TimeoutExpired:
            print("Ejecución excedió timeout.")
            err = "TimeoutExpired"
            code = 1
            out = ""
        if code == 0:
            print("✅ Programa se ejecutó sin errores (exit 0).")
            return True
        # si hubo error, analizar
        trace = err if err else out
        print("✖ Error detectado. Enviando a debugger...")
        analysis = analyze_error(trace)
        print("Debugger output:", analysis)
        # leer archivos actuales y enviar a fixer
        current_files = read_py_files(project_path)
        print(f"Enviando {len(current_files)} archivos al fixer...")
        fixes = fix_code(current_files, trace)
        if not fixes:
            print("El fixer no devolvió cambios. Abortando.")
            return False
        # escribir fixes y reintentar
        print(f"Aplicando {len(fixes)} archivos corregidos...")
        write_fixed_files(project_path, fixes)
        time.sleep(1)
    print("❌ Falló después de máximos intentos.")
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python runner.py <project_path> [entry_rel] [max_attempts]")
        sys.exit(1)
    proj = sys.argv[1]
    entry = sys.argv[2] if len(sys.argv) > 2 else "src/main.py"
    attempts = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    ok = auto_fix_loop(proj, entry_rel=entry, max_attempts=attempts)
    print("Resultado final:", "OK" if ok else "FAILED")
