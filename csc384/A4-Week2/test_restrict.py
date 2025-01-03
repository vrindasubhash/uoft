from bnetbase import Factor, Variable
from naive_bayes import restrict

def test_restrict():
    print("Test 1: Restrict Normal Factor")
    # Test Case 1: Normal Restriction
    var1 = Variable("A", [1, 2])
    var2 = Variable("B", ['x', 'y'])
    factor = Factor("ExampleFactor", [var1, var2])

    # Add values to the factor manually
    factor.add_values([
        [1, 'x', 0.2],
        [1, 'y', 0.8],
        [2, 'x', 0.5],
        [2, 'y', 0.5]
    ])

    print("Original Factor Values:")
    factor.print_table()

    # Restrict variable A to 1
    restricted_factor = restrict(factor, var1, 1)

    if restricted_factor is not None:
        print("\nRestricted Factor (A=1):")
        restricted_factor.print_table()
        # Expected output:
        # [B = x,] = 0.2
        # [B = y,] = 0.8
    else:
        print("\nRestriction failed (check variable or value).")

    print("\nTest 2: Restrict with Variable Not in Scope")
    # Test Case 2: Restrict with variable not in scope
    var3 = Variable("C", [3, 4])
    restricted_not_in_scope = restrict(factor, var3, 3)
    assert restricted_not_in_scope is None, "Restriction should return None for variable not in scope."
    print("Restriction correctly returned None for variable not in scope.")

    print("\nTest 3: Restrict with Value Not in Domain")
    # Test Case 3: Restrict with value not in variable's domain
    restricted_invalid_value = restrict(factor, var1, 3)
    assert restricted_invalid_value is None, "Restriction should return None for value not in domain."
    print("Restriction correctly returned None for value not in domain.")

    print("\nTest 4: Restrict Factor to Single Value")
    # Test Case 4: Restrict Factor to Single Value
    restricted_single_value = restrict(factor, var2, 'x')
    if restricted_single_value is not None:
        print("\nRestricted Factor (B=x):")
        restricted_single_value.print_table()
        # Expected output:
        # [A = 1,] = 0.2
        # [A = 2,] = 0.5
    else:
        print("\nRestriction failed (check variable or value).")

    print("\nTest 5: Restrict Factor to Eliminate All")
    # Test Case 5: Restrict Factor to Eliminate All
    restricted_eliminate_all = restrict(factor, var2, 'z')  # Value 'z' does not exist
    assert restricted_eliminate_all is None, "Restriction should return None if value is invalid."
    print("Restriction correctly returned None for invalid value.")

    print("\nAll tests passed!")

if __name__ == "__main__":
    test_restrict()
