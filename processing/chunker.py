from typing import List, Dict

MAX_CHUNK_SIZE = 20000

def build_chunk_text(files: List[Dict]) -> str:
    text = ""

    for f in files:
        entry = f"""
            FILE: {f['file_path']}
            LAYER: {f['layer']}
            CLASS: {f['structure']['class_name']}
            CLASS_TYPE: {f['structure']['class_type']}
            
            ANNOTATIONS: {f['structure']['annotations']}
            METHODS: {f['structure']['methods']}
            HTTP_MAPPINGS: {f['structure']['http_mappings']}
            DEPENDENCIES: {f['structure']['dependencies']}
            
            CODE:
            {f['cleaned_code']}
            
            ----------------------------------------
            """
        text += entry

    return text


def chunk_files(processed_files: List[Dict]) -> List[str]:
    # Sort for better locality
    processed_files = sorted(processed_files, key=lambda x: x["file_path"])

    chunks = []
    current = []
    current_size = 0

    for file_obj in processed_files:
        file_text = build_chunk_text([file_obj])
        size = len(file_text)

        if current and current_size + size > MAX_CHUNK_SIZE:
            chunks.append(build_chunk_text(current))
            current = []
            current_size = 0

        current.append(file_obj)
        current_size += size



    if current:
        chunks.append(build_chunk_text(current))

    return chunks