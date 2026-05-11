from openai import OpenAI
import os
import json
import re

from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-4o-mini"


FILE_SCHEMA = """
Return a JSON array with objects:

{
  "file_path": "",
  "class_name": "",
  "layer": "",
  "class_type": "class|interface|enum",
  "annotations": [],
  "methods": [
    {
      "name": "",
      "signature": "",
      "http_method": "GET|POST|PUT|DELETE|PATCH|null",
      "path": null,
      "visibility": "",
      "description": ""
    }
  ],
  "dependencies": [],
  "complexity_score": 1,
  "complexity_notes": "",
  "summary": ""
}

Rules:
- STRICT JSON ONLY
- No explanation
"""


def analyze_chunk(chunk: str):
    prompt = f"""
            You are a senior Java architect.
            
            Analyze this codebase chunk.
            
            {FILE_SCHEMA}
            
            CODE:
            {chunk}
            """

    response = client.responses.create(
        model=MODEL,
        input=[
            {"role": "system", "content": "You are an expert Java code analyzer."},
            {"role": "user", "content": prompt}
        ]
    )
    content = response.output[0].content[0].text.strip()
    # content = response.choices[0].message.content.strip()

    content = re.sub(r"^```json", "", content)
    content = re.sub(r"```$", "", content)

    try:
        parsed = json.loads(content)
        return parsed if isinstance(parsed, list) else [parsed]
    except:
        return [{"error": content}]