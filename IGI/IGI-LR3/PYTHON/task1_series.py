# task1_series.py
# Task 1: compute ln(1+x) using series expansion (variant 13)

import math
from utils import input_float, simple_decorator

@simple_decorator
def ln_series(x, eps, max_iter=500):
    """
    Compute ln(1+x) = x - x^2/2 + x^3/3 - ... for |x| < 1.
    Returns: (approx, number_of_terms)
    """
    if x <= -1:
        raise ValueError("x must be > -1 (ln(1+x) undefined or series diverges)")
    if abs(x) >= 1 and x != 1:
        print("Warning: series converges slowly or may diverge. |x| should be < 1.")

    term = x          # first term (n=1)
    total = term
    n = 1             # number of terms summed

    while abs(term) > eps and n < max_iter:
        n += 1
        # recurrence: term_n = - term_{n-1} * x * (n-1)/n
        term = -term * x * (n-1) / n
        total += term

    return total, n

def run_task1():
    """Main entry for Task 1."""
    print("\n--- Task 1: Series Expansion for ln(1+x) ---")
    x = input_float("Enter x (|x| < 1, but x > -1): ")
    eps = input_float("Enter accuracy (e.g., 0.0001): ")

    try:
        approx, terms = ln_series(x, eps)
        exact = math.log(1 + x)
        print(f"\nResults:")
        print(f"x = {x}")
        print(f"Approximation F(x) = {approx}")
        print(f"Number of terms used = {terms}")
        print(f"Exact math.log(1+x) = {exact}")
        print(f"Difference = {abs(approx - exact)}")
    except ValueError as e:
        print(f"Error: {e}")