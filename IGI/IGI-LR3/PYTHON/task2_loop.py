# task2_loop.py
# Task 2: count natural numbers entered until 0 is entered

from utils import input_int, simple_decorator

@simple_decorator
def count_natural_numbers():
    """
    Read integers until 0. Return the count of positive numbers (natural numbers).
    """
    count = 0
    print("Enter integers (0 to stop):")
    while True:
        num = input_int("> ")
        if num == 0:
            break
        if num > 0:        # natural numbers are positive
            count += 1
    return count

def run_task2():
    """Main entry for Task 2."""
    print("\n--- Task 2: Count Natural Numbers ---")
    result = count_natural_numbers()
    print(f"Number of natural numbers: {result}")