# agent.py
import sys
from roles import interpret, plan_project, architect, generate_code, fix_code, analyze_error
from builder import build_from_files

def run_pipeline(idea: str):
    print("[1/6] Interpretando idea...")
    spec = interpret(idea)
    print("Spec:", spec)

    print("[2/6] Planificando proyecto...")
    plan = plan_project(spec)
    print("Plan:", plan)

    print("[3/6] Arquitecturando...")
    arch = architect(plan)
    print("Architecture:", arch)

    print("[4/6] Generando código (coder)... Esto puede tardar...")
    files = generate_code(arch)
    if not files:
        print("El coder no devolvió archivos. Abortando.")
        return

    print(f"[5/6] Guardando proyecto localmente...")
    project_path = build_from_files(files, project_name=spec.get("goal","project"))
    print("Proyecto generado en:", project_path)

    # Aquí termina MVP de roles. No ejecutamos ni compilamos.
    print("[6/6] Pipeline completado. Revisar archivos y ejecutar manualmente.")
    return project_path

if __name__ == "__main__":
    if len(sys.argv) > 1:
        idea = " ".join(sys.argv[1:])
    else:
        idea = input("Describe la idea del programa: ").strip()
    run_pipeline(idea)
