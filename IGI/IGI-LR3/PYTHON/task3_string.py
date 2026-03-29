# task3_string.py
# Task 3: check if a string represents an octal number

from utils import input_nonempty_string, simple_decorator

@simple_decorator
def is_octal(s):
    """
    Return True if s is a valid octal number (with optional 0o prefix).
    """
    s = s.strip().lower()
    if not s:
        return False
    # remove optional prefix
    if s.startswith('0o'):
        s = s[2:]
    # all characters must be 0-7
    return all(ch in '01234567' for ch in s)

def run_task3():
    """Main entry for Task 3."""
    print("\n--- Task 3: Check Octal String ---")
    s = input_nonempty_string("Enter a string: ")
    if is_octal(s):
        print(f"'{s}' is a valid octal number.")
    else:
        print(f"'{s}' is NOT a valid octal number.")