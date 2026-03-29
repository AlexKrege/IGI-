import random

def input_int(prompt):
    """Read an integer from user with error handling."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Error: please enter an integer!")

def input_float(prompt):
    """Read a float from user with error handling."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Error: please enter a number!")

def input_nonempty_string(prompt):
    """Read a non-empty string."""
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("String cannot be empty!")

def simple_decorator(func):
    """Decorator that prints function name and result."""
    def wrapper(*args, **kwargs):
        print(f"\n[Decorator] Calling function: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[Decorator] Result: {result}")
        return result
    return wrapper

def generate_random_list(size, min_val=-100, max_val=100):
    """Generate a list of random floats."""
    return [random.uniform(min_val, max_val) for _ in range(size)]