"""
Interactive version: chat with the model in the terminal.

Same tool as main.py, but it keeps asking you for input and remembers the
conversation, so you can ask follow up questions.

    uv run chat.py
"""

import json
import os

from dotenv import load_dotenv
from openai import OpenAI

# Reuses the tool and its description from main.py.
# This works because main.py keeps its demo inside "if __name__ == '__main__'",
# so importing it does not run the demo.
from main import MODEL, calculate, tools

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# The model may need several calculations before it can answer.
MAX_TOOL_ROUNDS = 5

# The whole conversation lives here. Every turn gets added to it, and the
# full list is sent on each request, because the API has no memory of its own.
messages = [
    {
        "role": "system",
        "content": "Always use the calculate tool for math. Answer briefly.",
    }
]

print("Ask a math question. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ("exit", "quit", ""):
        break

    messages.append({"role": "user", "content": user_input})

    for _ in range(MAX_TOOL_ROUNDS):
        response = client.chat.completions.create(
            model=MODEL, messages=messages, tools=tools
        )
        message = response.choices[0].message
        messages.append(message)

        # No tool requested means this is the final answer.
        if not message.tool_calls:
            print("AI:", message.content, "\n")
            break

        # Run every calculation the model asked for and send the results back.
        for tool_call in message.tool_calls:
            arguments = json.loads(tool_call.function.arguments)
            result = calculate(**arguments)
            print(f"  [tool] calculate({arguments}) -> {result}")

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                }
            )
    else:
        # Only runs if the loop above never reached "break".
        print("AI: too many tool calls in a row, giving up.\n")
