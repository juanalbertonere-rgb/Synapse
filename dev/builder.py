# builder.py
from utils import write_project_files, safe_filename
import os

def build_from_files(files_dict, base_folder="projects", project_name=None):
    if project_name is None:
        project_name = "project"
    safe = safe_filename(project_name)
    base_path = os.path.join(base_folder, safe)
    write_project_files(base_path, files_dict)
    return base_path
