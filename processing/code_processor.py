import re


def detect_layer(file_path: str) -> str:
    path = file_path.lower()

    if "controller" in path:
        return "controller"
    elif "service" in path:
        return "service"
    elif "repository" in path:
        return "repository"
    elif "entity" in path:
        return "entity"
    elif "config" in path:
        return "config"
    elif "dto" in path:
        return "dto"
    elif "security" in path:
        return "security"
    else:
        return "other"


def preprocess_code(code: str) -> str:
    if not code:
        return ""

    code = re.sub(r"//.*", "", code)
    code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)
    code = re.sub(r"import\s+.*?;", "", code)
    code = re.sub(r"package\s+.*?;", "", code)
    code = re.sub(r"\n\s*\n", "\n", code)

    return code.strip()


def extract_structure(code: str) -> dict:
    structure = {
        "class_name": None,
        "class_type": "class",
        "methods": [],
        "annotations": [],
        "http_mappings": [],
        "dependencies": []
    }

    if not code:
        return structure

    # Class name + type
    class_match = re.search(r"(class|interface|enum)\s+(\w+)", code)
    if class_match:
        structure["class_type"] = class_match.group(1)
        structure["class_name"] = class_match.group(2)

    # Annotations
    annotations = re.findall(r"@\w+", code)
    structure["annotations"] = list(set(annotations))

    # Methods with visibility
    method_pattern = r"(public|private|protected)\s+[\w<>\[\]]+\s+(\w+)\s*\("
    methods = re.findall(method_pattern, code)

    structure["methods"] = [
        {"name": m[1], "visibility": m[0]} for m in methods
    ]

    # HTTP mappings
    http = re.findall(r"@(GetMapping|PostMapping|PutMapping|DeleteMapping)\s*\((.*?)\)", code)
    structure["http_mappings"] = http

    # Dependencies (fields)
    fields = re.findall(r"private\s+(\w+)\s+(\w+);", code)
    structure["dependencies"] = [f[1] for f in fields]

    return structure


def process_file(file_path: str, code: str) -> dict:
    return {
        "file_path": file_path,
        "layer": detect_layer(file_path),
        "cleaned_code": preprocess_code(code),
        "structure": extract_structure(preprocess_code(code))
    }