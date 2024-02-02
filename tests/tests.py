from .bootstrap.recurse import Recurse

runner = Recurse()

passed = 0
total = 0

print("Test 1 (functions): ", end="")
result = runner.callFunction("test_one")