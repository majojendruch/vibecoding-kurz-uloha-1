"""
LLM API + tool calling.

The model cannot calculate reliably, so it asks this script to run a Python
function instead. The script runs it, sends the result back, and the model
writes the final answer.
"""

import json
import os

from dotenv import load_dotenv
from openai import OpenAI

MODEL = "gpt-4o"


# --- The tool: an ordinary Python function -------------------------------
def calculate(a: float, b: float, operation: str) -> dict:
    """Add, subtract, multiply or divide two numbers."""
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        if b == 0:
            return {"error": "Cannot divide by zero."}
        result = a / b
    else:
        return {"error": f"Unknown operation: {operation}"}

    return {"result": result}


# --- Description of the tool for the model -------------------------------
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calculate with two numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                    "operation": {
                        "type": "string",
                        "enum": ["add", "subtract", "multiply", "divide"],
                        "description": "Which operation to use",
                    },
                },
                "required": ["a", "b", "operation"],
            },
        },
    }
]


# --- The conversation ----------------------------------------------------
if __name__ == "__main__":
    load_dotenv()  # reads OPENAI_API_KEY from the .env file
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Change this line to ask something else.
    question = "What is 1234.56 divided by 7?"

    messages = [
        {"role": "system", "content": "Always use the calculate tool for math."},
        {"role": "user", "content": question},
    ]

    print("Question:", question)

    # 1. Send the question and the tool description to the model.
    response = client.chat.completions.create(
        model=MODEL, messages=messages, tools=tools
    )
    message = response.choices[0].message

    if not message.tool_calls:
        print("The model answered without a tool:", message.content)
        raise SystemExit

    # 2. Run the function the model asked for.
    tool_call = message.tool_calls[0]
    arguments = json.loads(tool_call.function.arguments)  # they arrive as JSON text
    print("Model wants:", tool_call.function.name, arguments)

    result = calculate(**arguments)
    print("Function returned:", result)

    # 3. Send the result back to the model.
    messages.append(message)
    messages.append(
        {
            "role": "tool",
            "tool_call_id": tool_call.id,  # links the result to the request
            "content": json.dumps(result),
        }
    )

    # 4. The model writes the final answer using that result.
    final = client.chat.completions.create(model=MODEL, messages=messages)
    print("Final answer:", final.choices[0].message.content)
