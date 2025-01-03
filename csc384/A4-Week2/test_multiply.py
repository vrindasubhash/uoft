from bnetbase import Factor, Variable
from naive_bayes import multiply

def test_multiply_with_example():
    # Define variables
    w = Variable("W", ["w", "¬w"])  # W has two states: w, ¬w
    a = Variable("A", ["a", "¬a"])  # A has two states: a, ¬a
    g = Variable("G", ["g", "¬g"])  # G has two states: g, ¬g

    # Verify variable domains
    print("Variable W Domain:", w.domain())
    print("Variable A Domain:", a.domain())
    print("Variable G Domain:", g.domain())

    # Define the first factor
    factor1 = Factor("Factor1", [w, a])
    factor1.add_values([
        ["w", "a", 0.8],
        ["¬w", "a", 0.2],
        ["w", "¬a", 0.4],
        ["¬w", "¬a", 0.6]
    ])

    # Define the second factor
    factor2 = Factor("Factor2", [a, g])
    factor2.add_values([
        ["a", "g", 0.4],
        ["a", "¬g", 0.6],
        ["¬a", "g", 0.04],
        ["¬a", "¬g", 0.96]
    ])

    print("Original Factor 1:")
    factor1.print_table()

    print("\nOriginal Factor 2:")
    factor2.print_table()

    # Multiply the two factors
    multiplied_factor = multiply([factor1, factor2])
    if multiplied_factor is not None:
        print("\nResult of Multiplication:")
        multiplied_factor.print_table()
    else:
        print("\nMultiplication failed.")

if __name__ == "__main__":
    test_multiply_with_example()
