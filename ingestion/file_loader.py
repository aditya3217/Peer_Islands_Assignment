import os
from config import REPO_PATH, ALLOWED_EXTENSIONS, IGNORE_DIRS


def collect_java_files():
    files = []

    for root, dirs, filenames in os.walk(REPO_PATH):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in filenames:
            if any(file.endswith(ext) for ext in ALLOWED_EXTENSIONS):
                files.append(os.path.join(root, file))

    return sorted(files)

def read_file_content(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""