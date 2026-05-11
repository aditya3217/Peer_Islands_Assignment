from ingestion.file_loader import collect_java_files, read_file_content
from processing.code_processor import process_file
from processing.chunker import chunk_files
from processing.aggregator import load_all_chunks
from llm.summarizer import build_project_summary
from llm.analyzer import analyze_chunk

import time
import json
import os


def main():

    files = collect_java_files()

    processed = []
    for file in files:
        code = read_file_content(file)
        processed.append(process_file(file, code))

    # print(f"Processed files: {len(processed)}")

    chunks = chunk_files(processed)
    # print(f"Chunks created: {len(chunks)}")

    results = []
    for i, chunk in enumerate(chunks):
        print(f"Chunk size: {len(chunk)}")
        print(f"Analyzing chunk {i+1}/{len(chunks)}")
        res = analyze_chunk(chunk)
        results.extend(res)

        with open(f"output/chunk_{i}.json", "w") as f:
            json.dump(res, f, indent=2)

        time.sleep(1)

    print(f"Total classes extracted: {len(results)}")

    # print("\nLoading chunk outputs...")
    all_data = load_all_chunks()

    print("\nGenerating project summary...")
    summary = build_project_summary(all_data)

    # Final output
    final_output = {
        "project_summary": summary,
        "files": all_data
    }

    with open("output/analysis_output_final.json", "w") as f:
        json.dump(final_output, f, indent=2)

    print("Final output generated: analysis_output_final.json")




if __name__ == "__main__":
    main()