from bnetbase import Variable, Factor, BN
from naive_bayes import ve, restrict, sum_out, multiply, normalize

def test_ve_with_example():
    # Step 1: Define Variables
    w = Variable("W", ["w", "¬w"])
    a = Variable("A", ["a", "¬a"])
    g = Variable("G", ["g", "¬g"])
    b = Variable("B", ["b", "¬b"])

    # Step 2: Define Factors
    # Factor 1: P(W | A)
    factor1 = Factor("P(W|A)", [w, a])
    factor1.add_values([
        ["w", "a", 0.8],
        ["¬w", "a", 0.2],
        ["w", "¬a", 0.4],
        ["¬w", "¬a", 0.6]
    ])

    # Factor 2: P(G | A)
    factor2 = Factor("P(G|A)", [g, a])
    factor2.add_values([
        ["g", "a", 0.4],
        ["¬g", "a", 0.6],
        ["g", "¬a", 0.04],
        ["¬g", "¬a", 0.96]
    ])

    # Factor 3: P(A)
    factor3 = Factor("P(A)", [a])
    factor3.add_values([
        ["a", 0.5],
        ["¬a", 0.5]
    ])

    # Factor 4: P(B)
    factor4 = Factor("P(B)", [b])
    factor4.add_values([
        ["b", 0.1],
        ["¬b", 0.9]
    ])

    # Step 3: Create Bayesian Network
    bayes_net = BN("ExampleBayesNet", [w, a, g, b], [factor1, factor2, factor3, factor4])

    # Step 4: Execute VE
    print("\nTest 1: Compute P(W) using VE")
    result_factor = ve(bayes_net, w, [b])
    if result_factor is not None:
        print("Resulting Factor:")
        result_factor.print_table()
    else:
        print("VE failed.")

if __name__ == "__main__":
    test_ve_with_example()
