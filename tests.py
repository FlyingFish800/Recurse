import recurse

runner = recurse.Recurse()

passed = 0
total = 0

runner.loadFile("tests/test_cases.rc")

def test_fn(expected, name, args):
    global total
    global passed
    total += 1
    print(f"Test {total} ({name}): ", end="")
    result = runner.callFunction(name, args)
    if result != expected:
        print("\33[31mFAIL\x1b[0m")
        print(f"Expected: '{expected}'")
        print(f"Evaluated: '{result}'")
    else: 
        print("\33[32mPASS\x1b[0m")
        passed += 1

def status():
    global total
    global passed

    print(f"Passed {passed}/{total} tests ({(passed/total)*100:3.2f}%)")

test_fn(1, "test_one", [])
test_fn(2, "test_two", [])
test_fn(5, "test_three", [5])


status()
