import json
from typing import List
from openai import OpenAI
from string import Template

client = OpenAI()


def load_prompt() -> str:
    with open("prompt.txt", "r", encoding="utf-8") as f:
        return f.read()


def format_files(files: List[str]) -> str:
    """
    Converts file list into a readable string for the LLM.
    """
    return "\n".join(files)


def generate_plan(goal: str, files: List[str], root_dir: str):
    prompt_template = load_prompt()

    formatted_files = format_files(files)

    prompt = Template(prompt_template).substitute(
        root_dir=root_dir,
        files=formatted_files,
        goal=goal
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    content = response.choices[0].message.content
    return json.loads(content)