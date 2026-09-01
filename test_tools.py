"""Quick check of the calculate function. Run with: uv run test_tools.py"""

from main import calculate

assert calculate(2, 3, "add") == {"result": 5}
assert calculate(10, 4, "subtract") == {"result": 6}
assert calculate(1250, 1.23, "multiply") == {"result": 1537.5}
assert calculate(10, 4, "divide") == {"result": 2.5}
assert "error" in calculate(10, 0, "divide")

print("All tests passed.")
