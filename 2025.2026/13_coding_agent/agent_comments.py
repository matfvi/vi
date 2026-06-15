# Imports Python's JSON library so the script can send JSON requests to Ollama
# and parse JSON tool commands returned by the model.
import json

# Imports operating-system helpers used for walking directories, joining paths,
# creating folders, and checking parent directories.
import os

# Imports the standard-library HTTP client so this file has no third-party
# dependencies; it is enough for a local Ollama POST request.
import urllib.request


# The exact local Ollama model name. This must match `ollama list`; using a
# constant keeps the model choice visible and easy to change for a demo.
MODEL = "qwen2.5-coder:14b"

# Ollama's chat API endpoint. `localhost` means the request stays on this
# machine, `11434` is Ollama's default port, and `/api/chat` is the chat route.
OLLAMA_URL = "http://localhost:11434/api/chat"

# Caps each agent turn at 8 tool/LLM iterations so a bad model response cannot
# loop forever during the presentation. Eight is arbitrary but enough for a few
# read/edit/list calls.
MAX_TOOL_STEPS = 8


# The system prompt is the agent's instruction manual. It tells the model which
# tools exist and forces a tiny JSON protocol instead of free-form tool text.
SYSTEM_PROMPT = (
    # Start with the same leading newline style as the original triple-quoted
    # prompt; it is not required, but it keeps the prompt visually separated.
    "\n"
    # Gives the model its role in one sentence.
    "You are a tiny coding agent demo.\n"
    # Blank line separates the identity from the tool protocol.
    "\n"
    # Tells the model the only acceptable tool-call format.
    "You can use these tools by replying with exactly one JSON object and no markdown:\n"
    # Blank line makes the examples easier for the model to copy.
    "\n"
    # `list_files` has no arguments because it always lists the current workspace.
    '{"tool": "list_files"}\n'
    # `read_files` takes a list because reading several files in one tool call is
    # simpler than making the model call the same tool repeatedly.
    '{"tool": "read_files", "paths": ["path/to/file.py"]}\n'
    # `edit_files` takes one path and full file content; full overwrite is much
    # easier to demo than diff parsing or patch application.
    '{"tool": "edit_files", "path": "path/to/file.py", "content": "full new file content"}\n'
    # Blank line separates tool calls from completion.
    "\n"
    # Explains the completion protocol so the outer Python loop knows when to stop.
    "When the user's task is complete, reply with:\n"
    # `final` is deliberately separate from `tool` so completion is explicit.
    '{"final": "short summary of what you did"}\n'
    # Blank line separates completion from final behavioral guidance.
    "\n"
    # Reinforces full overwrite semantics and the demo assumption that inputs are sane.
    "Use edit_files to overwrite the whole file. Assume paths and requests are valid.\n"
)


# Sends the current conversation to Ollama and returns the model's message text.
def call_ollama(messages):
    # Build the request body in the shape Ollama's `/api/chat` endpoint expects.
    body = {
        # `model` selects the local model configured above rather than hardcoding
        # the name in the request.
        "model": MODEL,
        # `messages` is the full conversation so the model sees prior tool results.
        "messages": messages,
        # `stream: False` asks Ollama for one complete JSON response instead of a
        # token stream; that keeps this beginner demo simple.
        "stream": False,
        # `temperature: 0` reduces randomness so the model is more likely to emit
        # valid JSON and repeatable demo behavior.
        "options": {"temperature": 0},
    }

    # Create a POST request object. The URL is the local Ollama endpoint; the
    # body must be encoded to UTF-8 bytes because HTTP sends bytes, not Python dicts.
    request = urllib.request.Request(
        # First positional argument: where to send the HTTP request.
        OLLAMA_URL,
        # `json.dumps(body)` turns the Python dict into JSON text; `.encode("utf-8")`
        # converts that text into bytes. UTF-8 is the normal JSON/web encoding.
        data=json.dumps(body).encode("utf-8"),
        # This header tells Ollama to parse the body as JSON instead of plain text.
        headers={"Content-Type": "application/json"},
    )

    # Open the HTTP request and close the response automatically afterward.
    with urllib.request.urlopen(request) as response:
        # Read raw bytes from the response, decode UTF-8 text, then parse JSON.
        data = json.loads(response.read().decode("utf-8"))
        # Ollama chat responses put the assistant content at message.content.
        return data["message"]["content"]


# Converts the model's text into a Python dict tool command.
def parse_json(text):
    # Remove surrounding whitespace because models often add leading/trailing newlines.
    text = text.strip()

    # The prompt asks for no markdown, but models often wrap JSON in fenced code blocks.
    if text.startswith("```"):
        # Strip backtick fence characters from both ends. This is intentionally
        # simple for the demo, not a complete markdown parser.
        text = text.strip("`")

        # If the fence was ```json, remove the `json` language label. The index
        # `4` is the length of the string "json".
        if text.startswith("json"):
            text = text[4:]

        # Strip whitespace left after removing fences or the `json` label.
        text = text.strip()

    # First try the ideal case: the whole model reply is valid JSON.
    try:
        return json.loads(text)

    # If the ideal parse fails, try extracting the first JSON-looking object.
    except json.JSONDecodeError:
        # Find the first opening brace because a JSON object starts with `{`.
        start = text.find("{")
        # Find the last closing brace because the command may be surrounded by
        # extra text. `+ 1` converts the closing-brace index into a slice endpoint,
        # since Python slices stop before the end index.
        end = text.rfind("}") + 1

        # Only slice if both braces exist and the closing brace comes after the opening.
        if start >= 0 and end > start:
            # Parse just the object-looking substring.
            return json.loads(text[start:end])

        # Re-raise the original JSON error if no object can be recovered.
        raise


# Tool: returns a simple newline-separated list of files in the workspace.
def list_files():
    # Accumulates relative file paths before sorting them for stable output.
    files = []

    # Walk from "." because the script is intended to run from the demo workspace.
    for root, dirs, filenames in os.walk("."):
        # These directories are hidden from the agent to keep demo output focused.
        for ignored in [".git", "__pycache__"]:
            # `os.walk` lets us mutate `dirs` in-place to prevent descending into
            # ignored folders.
            if ignored in dirs:
                # Remove only the ignored directory name currently being checked.
                dirs.remove(ignored)

        # Visit every file name in the current directory.
        for filename in filenames:
            # Join the current root and file name using OS-correct path separators.
            path = os.path.join(root, filename)
            # `os.walk(".")` returns paths like `./agent.py`; `path[2:]` removes
            # the leading "./" because it is noisy in a presentation. The `2`
            # means skip the dot and slash characters.
            files.append(path[2:] if path.startswith("./") else path)

    # If the directory is empty, return a clear string instead of an empty response.
    if not files:
        return "(no files)"

    # Sort for deterministic output, then join with newlines for readable tool results.
    return "\n".join(sorted(files))


# Tool: reads one or more files and returns their contents with filename headers.
def read_files(paths):
    # Collect each file's labeled content before joining them into one result string.
    chunks = []

    # `paths` is a list so the model can read related files in one call.
    for path in paths:
        # Open text files as UTF-8 for normal Python/source-code files; `"r"` means read.
        with open(path, "r", encoding="utf-8") as file:
            # Prefix each content block with its path so the model knows which file
            # each chunk came from. `file.read()` reads the whole file for simplicity.
            chunks.append(f"--- {path} ---\n{file.read()}")

    # Separate files by a blank line so multiple file contents do not run together.
    return "\n\n".join(chunks)


# Tool: overwrites a single file with new full content.
def edit_files(path, content):
    # Extract the parent directory, if any. For `agent.py`, this is empty; for
    # `project/app.py`, this is `project`.
    parent = os.path.dirname(path)

    # Only create directories when the path actually has a parent directory.
    if parent:
        # `exist_ok=True` means the command succeeds if the folder already exists,
        # which is convenient for repeated demos.
        os.makedirs(parent, exist_ok=True)

    # Open the target as UTF-8 text in write mode. `"w"` overwrites the whole file,
    # matching the simple `edit_files` contract in the prompt.
    with open(path, "w", encoding="utf-8") as file:
        # Write exactly the content supplied by the model.
        file.write(content)

    # Return a short result so the model can see that the write happened.
    return f"Wrote {path}"


# Dispatches one parsed model command to the matching Python tool function.
def run_tool(command):
    # Read the requested tool name from the parsed JSON object.
    tool = command["tool"]

    # Route `list_files` commands to the no-argument list tool.
    if tool == "list_files":
        return list_files()

    # Route `read_files` commands and pass through the model-provided path list.
    if tool == "read_files":
        return read_files(command["paths"])

    # Route `edit_files` commands and pass through the target path plus full content.
    if tool == "edit_files":
        return edit_files(command["path"], command["content"])

    # This should not happen if the model follows the prompt, but it makes unknown
    # tool names visible instead of silently doing nothing.
    return f"Unknown tool: {tool}"


# Runs one user request through the agent/tool loop.
def run_agent(user_message):
    # Start a fresh conversation for each REPL request. This keeps the demo simple
    # and avoids long context history.
    messages = [
        # The system message always comes first and defines the tool protocol.
        {"role": "system", "content": SYSTEM_PROMPT},
        # The user message is the task typed at the REPL prompt.
        {"role": "user", "content": user_message},
    ]

    # Run at most MAX_TOOL_STEPS model/tool cycles for this single user request.
    # `_` is used because the loop counter value itself is not needed.
    for _ in range(MAX_TOOL_STEPS):
        # Ask Ollama what to do next, given the current messages and tool results.
        reply = call_ollama(messages)
        # Print the raw model output so the presentation can show the tool protocol.
        print(f"\nassistant raw:\n{reply}\n")

        # Parse the model's JSON command.
        try:
            command = parse_json(reply)

        # If parsing fails, return the raw text instead of crashing; this is the
        # simplest fallback for a demo where the model sometimes ignores formatting.
        except json.JSONDecodeError:
            return reply

        # Add the model reply to conversation history so the next turn sees it.
        messages.append({"role": "assistant", "content": reply})

        # A `final` command means the model believes the user request is done.
        if "final" in command:
            return command["final"]

        # Execute the selected tool and capture its text result.
        result = run_tool(command)
        # Print the tool output so the audience can see the local action happen.
        print(f"tool {command['tool']} result:\n{result}\n")

        # Feed the tool result back to the model as the next user message. This is
        # the core agent loop: model chooses tool, Python runs it, model sees result.
        messages.append(
            {
                # `role: user` is used because Ollama's simple chat API does not need
                # a special tool-result role for this demo.
                "role": "user",
                # The content names the tool, includes its result, and reminds the
                # model to finish with `final` when there is nothing else to do.
                "content": (
                    f"Tool result for {command['tool']}:\n{result}\n\n"
                    "Continue. If the task is complete, reply with final JSON."
                ),
            }
        )

    # If the model never calls `final`, stop after the fixed cap instead of looping.
    return "Stopped after max tool steps."


# Starts the interactive command-line interface.
def main():
    # Display a small title so the user knows the REPL started.
    print("Tiny Ollama coding agent")
    # Print the model constant so the demo audience can see which local model is used.
    print("Model:", MODEL)
    # Print usage guidance; the newline at the end leaves space before the prompt.
    print("Type a coding task, or 'exit' to quit.\n")

    # Keep reading user tasks until the user exits.
    while True:
        # `input("> ")` shows a simple prompt. `.strip()` removes accidental spaces
        # and the trailing newline from the terminal input.
        user_message = input("> ").strip()

        # Accept either common exit word. A set is used because membership checks are
        # clearer than `user_message == "exit" or user_message == "quit"`.
        if user_message in {"exit", "quit"}:
            # Leave the infinite REPL loop.
            break

        # Ignore blank lines so pressing Enter does not call the model.
        if not user_message:
            # Jump back to the start of the REPL loop for another input.
            continue

        # Run the agent loop for this one user request.
        answer = run_agent(user_message)
        # Print the final answer with blank lines around it for readability.
        print(f"\n{answer}\n")


# This guard means `main()` only runs when executing `python3 agent.py`, not when
# importing the file for tests or helper checks. `__main__` is Python's standard
# name for the directly executed script module.
if __name__ == "__main__":
    # Start the REPL.
    main()
