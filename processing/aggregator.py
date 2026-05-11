import json
import os


def load_all_chunks(folder_path="output/chunks"):
    all_data = []

    for file in os.listdir(folder_path):
        if file.startswith("chunk_") and file.endswith(".json"):
            with open(os.path.join(folder_path, file)) as f:
                data = json.load(f)
                all_data.extend(data)

    return all_data