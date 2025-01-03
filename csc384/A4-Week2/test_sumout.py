from bnetbase import Factor, Variable
from naive_bayes import sum_out

def test_sum_out_with_example():
    # Define variables
    w = Variable("W", ["w", "¬w"])  # W has two states: w, ¬w
    a = Variable("A", ["a", "¬a"])  # A has two states: a, ¬a

    # Define the original factor
    factor = Factor("ExampleFactor", [w, a])
    factor.add_values([
        ["w", "a", 0.8],
        ["¬w", "a", 0.2],
        ["w", "¬a", 0.4],
        ["¬w", "¬a", 0.6]
    ])

    print("Test 1: Example Factor")
    print("Original Factor:")
    factor.print_table()

    # Step 1: Sum out A
    summed_out_a = sum_out(factor, a)
    if summed_out_a is not None:
        print("\nFactor after summing out A:")
        summed_out_a.print_table()
    else:
        print("\nSumming out A failed.")

    # Step 2: Sum out W
    summed_out_w = sum_out(summed_out_a, w)
    if summed_out_w is not None:
        print("\nFactor after summing out W:")
        summed_out_w.print_table()
    else:
        print("\nSumming out W failed.")

    # Edge Cases
    print("\nTest 2: Sum Out Variable Not in Scope")
    b = Variable("B", ["b1", "b2"])
    summed_out_invalid = sum_out(factor, b)
    if summed_out_invalid is None:
        print("Summing out a variable not in scope correctly returned None.")
    else:
        print("Failed: Summing out a variable not in scope should return None.")

    print("\nTest 3: Sum Out From Empty Factor")
    empty_factor = Factor("EmptyFactor", [])
    summed_out_empty = sum_out(empty_factor, a)
    if summed_out_empty is None:
        print("Summing out from an empty factor correctly returned None.")
    else:
        print("Failed: Summing out from an empty factor should return None.")

    print("\nTest 4: Factor with Single Variable")
    single_var_factor = Factor("SingleVarFactor", [a])
    single_var_factor.add_values([
        ["a", 0.5],
        ["¬a", 0.3]
    ])
    print("Original Single Variable Factor:")
    single_var_factor.print_table()

    summed_out_single = sum_out(single_var_factor, a)
    if summed_out_single is not None:
        print("\nSummed Out Single Variable Factor:")
        summed_out_single.print_table()
        # Expected output: [] = 0.8 (0.5 + 0.3)
    else:
        print("Summing out single variable factor failed.")

    print("\nTest 5: Factor with Uniform Values")
    uniform_factor = Factor("UniformFactor", [w, a])
    uniform_factor.add_values([
        ["w", "a", 1.0],
        ["¬w", "a", 1.0],
        ["w", "¬a", 1.0],
        ["¬w", "¬a", 1.0]
    ])
    print("Original Uniform Factor:")
    uniform_factor.print_table()

    summed_out_uniform = sum_out(uniform_factor, a)
    if summed_out_uniform is not None:
        print("\nSummed Out Uniform Factor (A):")
        summed_out_uniform.print_table()
        # Expected output: [W = w,] = 2.0; [W = ¬w,] = 2.0
    else:
        print("Summing out uniform factor failed.")

if __name__ == "__main__":
    test_sum_out_with_example()
