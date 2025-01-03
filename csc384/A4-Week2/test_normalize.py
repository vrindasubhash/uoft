from bnetbase import Factor, Variable
from naive_bayes import normalize

def test_normalize():
    print("Test 1: Normal Factor")
    # Test Case 1: Normal Factor
    var1 = Variable("A", [1, 2])
    var2 = Variable("B", ['x', 'y'])
    factor = Factor("ExampleFactor", [var1, var2])

    # Add values to the factor manually
    factor.add_values([
        [1, 'x', 2.0],
        [1, 'y', 3.0],
        [2, 'x', 5.0],
        [2, 'y', 0.0]
    ])

    print("Original Factor Values:")
    factor.print_table()

    # Normalize the factor
    normalized_factor = normalize(factor)

    # Verify and display the results
    if normalized_factor is not None:
        print("\nNormalized Factor Values:")
        normalized_factor.print_table()
    else:
        print("\nNormalization returned None (check for empty or zero-sum factor).")

    print("\nTest 2: Empty Factor")
    # Test Case 2: Empty Factor
    empty_factor = Factor("EmptyFactor", [])
    normalized_empty = normalize(empty_factor)
    assert normalized_empty is None, "Empty factor normalization should return None."
    print("Empty Factor normalization returned None as expected.")

    print("\nTest 3: Zero-Sum Factor")
    # Test Case 3: Zero-Sum Factor
    zero_factor = Factor("ZeroFactor", [var1, var2])
    zero_factor.add_values([
        [1, 'x', 0.0],
        [1, 'y', 0.0],
        [2, 'x', 0.0],
        [2, 'y', 0.0]
    ])
    normalized_zero = normalize(zero_factor)
    assert normalized_zero is None, "Zero-sum factor normalization should return None."
    print("Zero-Sum Factor normalization returned None as expected.")

    print("\nTest 4: Single Value Factor")
    # Test Case 4: Single Value Factor
    single_value_factor = Factor("SingleValueFactor", [var1])
    single_value_factor.add_values([
        [1, 4.0]
    ])
    normalized_single = normalize(single_value_factor)
    assert normalized_single is not None, "Single value factor normalization should not return None."
    assert normalized_single.get_value([1]) == 1.0, "Single value factor should normalize to 1.0."
    print("Single Value Factor normalization passed.")

    print("\nTest 5: All Values Equal")
    # Test Case 5: All Values Equal
    equal_factor = Factor("EqualFactor", [var1, var2])
    equal_factor.add_values([
        [1, 'x', 1.0],
        [1, 'y', 1.0],
        [2, 'x', 1.0],
        [2, 'y', 1.0]
    ])
    normalized_equal = normalize(equal_factor)
    assert normalized_equal is not None, "All values equal factor normalization should not return None."
    total_prob = sum([normalized_equal.get_value([1, 'x']), normalized_equal.get_value([1, 'y']),
                      normalized_equal.get_value([2, 'x']), normalized_equal.get_value([2, 'y'])])
    assert abs(total_prob - 1.0) < 1e-6, "Normalized probabilities should sum to 1.0."
    print("All Values Equal Factor normalization passed.")

    print("\nAll tests passed!")

if __name__ == "__main__":
    test_normalize()
