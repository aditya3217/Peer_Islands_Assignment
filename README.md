# Codebase Analyzer — Spring REST Sakila

A modular system for analyzing Java/Spring Boot codebases using Large Language Models (LLMs).
The tool processes source files, extracts structured metadata, and generates a machine-readable JSON knowledge base.

---

## Overview

This project analyzes the **spring-rest-sakila** repository, a Spring Boot REST API built on the Sakila database schema.

The system extracts:

* Project purpose and architectural overview
* Domain modules inferred from package structure
* Per-class metadata (type, layer, annotations, methods, dependencies)
* API endpoint definitions (HTTP method and path)
* Complexity scores and summaries
* Design patterns used across the codebase

---

## Architecture

The solution follows a two-pass LLM pipeline:

```
Codebase
  ↓
File Ingestion
  ↓
Preprocessing and Structure Extraction
  ↓
Chunking (token-safe batching)
  ↓
LLM Pass 1 — Class-level analysis
  ↓
Intermediate JSON (persisted locally)
  ↓
LLM Pass 2 — Project-level synthesis
  ↓
Final Output (analysis_output.json)
```

---

## Methodology

### Step 1 — File Ingestion

* Traverse repository directory
* Collect `.java` files from `src/main`
* Exclude test and build directories

---

### Step 2 — Code Processing

* Remove comments, imports, and package declarations
* Extract structural elements:

  * Class name and type
  * Method names and visibility
  * Annotations
  * Dependencies
  * Layer classification (controller, service, repository, etc.)
  * Package/module information

This preprocessing reduces token usage and improves LLM accuracy.

---

### Step 3 — Chunking

* Greedy bin-packing strategy
* Maximum ~20,000 characters per chunk
* Files are not split across chunks
* Files are processed in sorted order to preserve package locality

This ensures efficient use of the LLM context window.

---

### Step 4 — LLM Pass 1 (Extraction)

Each chunk is sent to the LLM to extract structured information:

* Class purpose
* Method signatures and descriptions
* API endpoints
* Dependencies
* Complexity score and notes

Outputs are stored as individual chunk files:

```
chunk_0.json
chunk_1.json
...
```

This enables reuse and avoids recomputation.

---

### Step 5 — LLM Pass 2 (Synthesis)

Instead of raw code, summarized class-level data is used to generate:

* Project purpose
* Architecture pattern
* Domain modules (based on package structure)
* Technology stack
* Security model
* Design patterns
* Complexity overview

This approach minimizes token usage and improves synthesis quality.

---

## Token Management Strategy

| Concern            | Approach                               |
| ------------------ | -------------------------------------- |
| Context limit      | Chunking (~20k characters per chunk)   |
| Token efficiency   | Preprocessing and structured summaries |
| Cost optimization  | Intermediate results persisted         |
| Output consistency | Schema-driven prompts                  |

---

## Output Schema

The final output is a JSON object:

```json
{
  "project_summary": {
    "project_name": "...",
    "project_purpose": "...",
    "tech_stack": [],
    "architecture_pattern": "...",
    "modules": [],
    "security_model": "...",
    "key_design_patterns": [],
    "complexity_overview": {}
  },
  "files": [
    {
      "file_path": "...",
      "class_name": "...",
      "class_type": "...",
      "layer": "...",
      "annotations": [],
      "methods": [],
      "dependencies": [],
      "complexity_score": 0,
      "summary": "..."
    }
  ]
}
```

---

## Setup

### Prerequisites

* Python 3.9+
* OpenAI API key

---

### Installation

```bash
pip install openai python-dotenv
```

---

### Configuration

Create a `.env` file:

```
OPENAI_API_KEY=your_api_key
```

---

### Run

```bash
python main.py
```

---

## Design Decisions

### Two-pass LLM pipeline

Separates extraction (Pass 1) and synthesis (Pass 2) to improve accuracy and reduce cost.

---

### Preprocessing before LLM

Reduces noise and improves signal quality by extracting structural features deterministically.

---

### Chunk-based processing

Ensures large codebases can be analyzed within model context limits.

---

### Intermediate persistence

Stores Pass 1 outputs locally to enable reuse, debugging, and cost optimization.

---

### Package-aware module detection

Modules are inferred using package structure instead of relying solely on LLM inference.

---

## Limitations

* Analysis is static; runtime behavior is not captured
* Complexity scores are heuristic (LLM-derived)
* Output may vary slightly across runs
* Very large files may produce partial analysis

---

## Future Enhancements

* Vector database (FAISS) for semantic search
* Codebase Q&A interface
* Dependency graph generation
* Automated architecture diagrams

---

## Conclusion

This project demonstrates a scalable approach to codebase analysis using LLMs, combining preprocessing, structured prompting, and multi-stage reasoning to produce a consistent and machine-readable knowledge base.
