# LLM API + tool calling

A Python script that calls the OpenAI API, lets the model use a local Python
function as a tool, and sends the result back to the model.

Homework for the VIP coding course.

## What it does

The tool is `calculate(a, b, operation)`, which does `add`, `subtract`,
`multiply` or `divide`.

The model never runs the code itself:

1. The script sends the question plus the tool description to the API.
2. The model replies with a tool call, for example
   `calculate(a=1234.56, b=7, operation="divide")`.
3. The script runs that Python function locally and gets `176.36...`.
4. The result goes back as a message with `role: "tool"`, and the model writes
   the final answer using the real number.

## Files

**`main.py`** is the assignment itself. One fixed question, one tool call, one
answer, written as four steps you can read top to bottom. Change the `question`
line to ask something else.

**`chat.py`** is the interactive version. It asks for input in a loop and keeps
the whole conversation, so follow up questions like "now multiply that by 12"
work. It also repeats steps 2 and 3 until the model stops asking for tools, so
it can handle problems that need several calculations. It imports the tool from
`main.py` instead of copying it.

**`test_tools.py`** checks the `calculate` function without calling the API, so
it costs nothing.

## Run

```bash
cp .env.example .env    # then paste your OpenAI API key into .env
uv run main.py
uv run chat.py
uv run test_tools.py
```
