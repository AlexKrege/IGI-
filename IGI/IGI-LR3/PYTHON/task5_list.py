# task5_list.py
# Task 5: list processing (variant 13)

from utils import input_int, generate_random_list, simple_decorator

def get_list_from_user(size):
    """Let the user enter a list of floats."""
    lst = []
    print(f"Enter {size} floating point numbers:")
    for i in range(size):
        while True:
            try:
                val = float(input(f"Element {i+1}: "))
                lst.append(val)
                break
            except ValueError:
                print("Invalid input. Please enter a number.")
    return lst

def sum_odd_positions(lst):
    """
    Sum of elements at odd positions (1-indexed).
    In Python (0-indexed), odd positions correspond to indices 0,2,4,...
    """
    return sum(lst[i] for i in range(0, len(lst), 2))

def sum_between_first_last_negative(lst):
    """
    Sum of elements between the first and last negative elements.
    Returns None if there are fewer than two negatives.
    """
    indices = [i for i, val in enumerate(lst) if val < 0]
    if len(indices) < 2:
        return None
    first = indices[0]
    last = indices[-1]
    if first + 1 > last - 1:
        return 0
    return sum(lst[first+1:last])

@simple_decorator
def process_list(lst):
    """Print results for the given list."""
    print(f"\nList: {lst}")
    odd_sum = sum_odd_positions(lst)
    print(f"Sum of elements at odd positions (1‑based): {odd_sum}")

    between_sum = sum_between_first_last_negative(lst)
    if between_sum is None:
        print("Not enough negative elements (need at least two).")
    else:
        print(f"Sum of elements between first and last negative: {between_sum}")

def run_task5():
    """Main entry for Task 5."""
    print("\n--- Task 5: List Processing ---")
    size = input_int("Enter the size of the list: ")
    if size <= 0:
        print("Size must be positive.")
        return

    print("Choose initialization method:")
    print("1 - Enter manually")
    print("2 - Generate random numbers")
    choice = input_int("Your choice (1 or 2): ")

    if choice == 1:
        lst = get_list_from_user(size)
    elif choice == 2:
        lst = generate_random_list(size)
        print("Generated list:", lst)
    else:
        print("Invalid choice.")
        return

    process_list(lst)