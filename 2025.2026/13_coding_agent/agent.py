import json
import os
import urllib.request


MODEL = "qwen2.5-coder:14b"
OLLAMA_URL = "http://localhost:11434/api/chat"
MAX_TOOL_STEPS = 8


SYSTEM_PROMPT = (
    "\n"
    "You are a tiny coding agent demo.\n"
    "\n"
    "You can use these tools by replying with exactly one JSON object and no markdown:\n"
    "\n"
    '{"tool": "list_files"}\n'
    '{"tool": "read_files", "paths": ["path/to/file.py"]}\n'
    '{"tool": "edit_files", "path": "path/to/file.py", "content": "full new file content"}\n'
    "\n"
    "When the user's task is complete, reply with:\n"
    '{"final": "short summary of what you did"}\n'
    "\n"
    "Use edit_files to overwrite the whole file. Assume paths and requests are valid.\n"
)


def call_ollama(messages):
    body = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "options": {"temperature": 0},
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )

    with urllib.request.urlopen(request) as response:
        data = json.loads(response.read().decode("utf-8"))
        return data["message"]["content"]


def parse_json(text):
    text = text.strip()

    if text.startswith("```"):
        text = text.strip("`")

        if text.startswith("json"):
            text = text[4:]

        text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}") + 1

        if start >= 0 and end > start:
            return json.loads(text[start:end])

        raise


def list_files():
    files = []

    for root, dirs, filenames in os.walk("."):
        for ignored in [".git", "__pycache__"]:
            if ignored in dirs:
                dirs.remove(ignored)

        for filename in filenames:
            path = os.path.join(root, filename)
            files.append(path[2:] if path.startswith("./") else path)

    if not files:
        return "(no files)"

    return "\n".join(sorted(files))


def read_files(paths):
    chunks = []

    for path in paths:
        with open(path, "r", encoding="utf-8") as file:
            chunks.append(f"--- {path} ---\n{file.read()}")

    return "\n\n".join(chunks)


def edit_files(path, content):
    parent = os.path.dirname(path)

    if parent:
        os.makedirs(parent, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        file.write(content)

    return f"Wrote {path}"


def run_tool(command):
    tool = command["tool"]

    if tool == "list_files":
        return list_files()

    if tool == "read_files":
        return read_files(command["paths"])

    if tool == "edit_files":
        return edit_files(command["path"], command["content"])

    return f"Unknown tool: {tool}"


def run_agent(user_message):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    for _ in range(MAX_TOOL_STEPS):
        reply = call_ollama(messages)
        print(f"\nassistant raw:\n{reply}\n")

        try:
            command = parse_json(reply)
        except json.JSONDecodeError:
            return reply

        messages.append({"role": "assistant", "content": reply})

        if "final" in command:
            return command["final"]

        result = run_tool(command)
        print(f"tool {command['tool']} result:\n{result}\n")

        messages.append(
            {
                "role": "user",
                "content": (
                    f"Tool result for {command['tool']}:\n{result}\n\n"
                    "Continue. If the task is complete, reply with final JSON."
                ),
            }
        )

    return "Stopped after max tool steps."


def main():
    print("Tiny Ollama coding agent")
    print("Model:", MODEL)
    print("Type a coding task, or 'exit' to quit.\n")

    while True:
        user_message = input("> ").strip()

        if user_message in {"exit", "quit"}:
            break

        if not user_message:
            continue

        answer = run_agent(user_message)
        print(f"\n{answer}\n")


if __name__ == "__main__":
    main()
