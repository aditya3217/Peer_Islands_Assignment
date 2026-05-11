from openai import OpenAI
import os
import json
import re

from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o-mini"


def build_project_summary(file_analyses: list):



    # Reduce payload (important!)
    summaries = [
        {
            "class_name": f.get("class_name"),
            "layer": f.get("layer"),
            "methods_count": len(f.get("methods", [])),
            "dependencies": f.get("dependencies"),
            "complexity_score": f.get("complexity_score"),
            "summary": f.get("summary")
        }
        for f in file_analyses
    ]

    summaries = sorted(
        summaries,
        key=lambda x: x.get("complexity_score", 0),
        reverse=True
    )

    prompt = f"""
    You are a senior software architect.

    IMPORTANT RULES:
    - Only use information present in the input data
    - Do NOT hallucinate class names or modules
    - Infer modules from package structure or common prefixes
    - Be precise and grounded in the data

    Return STRICT JSON:

    {{
      "project_name": "spring-rest-sakila",
      "project_purpose": "",
      "tech_stack": [],
      "architecture_pattern": "",
      "modules": [
        {{
          "name": "",
          "description": ""
        }}
      ],
      "security_model": "",
      "key_design_patterns": [],
      "complexity_overview": {{
        "average_complexity": 0,
        "overall_assessment": ""
      }}
    }}

    DATA:
    {json.dumps(summaries[:300], indent=2)}
    """


    response = client.responses.create(
        model=MODEL,
        max_output_tokens=2000,
        input=[
            {"role": "system", "content": "Expert software architect"},
            {"role": "user", "content": prompt}
        ]
    )

    content = response.output[0].content[0].text.strip()

    content = re.sub(r"^```json", "", content)
    content = re.sub(r"```$", "", content)

    try:
        return json.loads(content)
    except:
        return {"error": content}