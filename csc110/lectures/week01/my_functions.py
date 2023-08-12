"""CSC110 course notes section 2.2 example"""

def square(x: float) -> float:
    """return x squared
    >>> square(3.0)
    9.0
    >>> square(2.5)
    6.25
    """
    return x ** 2

def calculate_distance(p1: list, p2: list) -> float:
    """Return the distance between points p1 and p2.
    p1 and p2 are lists of the form [x, y], where the x- and y-coordinates are points.
    >>> calculate_distance([0, 0], [3.0, 4.0])
    5.0
    """
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def fahrenheit_to_celcius(deg_f: float) -> float:
    """Return the celcius temperature corresponding to fahrenheit mransure ded_f.

    >>> fahrenheit_to_celcius(80.0)
    26.6666666666668

    >>> fahrenheit_to_celcius(0.0)
    -17.777777777778
    """
    return (deg_f - 32) * 5 / 9


def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """Return the distance between (x1, y1) and (x2, y2).

    >>> distance(0.0, 0.0, 3.0, 4.0)
    5.0
    >>> distance(-5.0, 0.0, 0.0, -12.0)
    13.0
    """
    delta_x = x2 - x1
    delta_y = y2 - y1
    return (delta_x ** 2 + delta_y ** 2) ** 0.5


def is_same_length(list1: list, list2: list) -> bool:
	"""Returns if list1 and list2 have the same length
	>>> is_same_length([1, 2, 3], [4, 5, 6])
    True
    >>> is_same_length([1, 2, 3], [])
    False
    """
	length1 = len(list1)
	length2 = len(list2)
	return length1==length2


def after_tax_cost(price: float, tax_rate: float) -> float:
    """Returns the price after the tax_rate is added, rounded to two decimal places
    >>> after_tax_cost(5.0, 0.01)
    5.05
    """
    cost = price * (1 + tax_rate)
    return round(cost, 2)

def total_after_tax_cost(prices: list, tax_rate: float) -> float:
    """Returns the total cost of prices after tax has been added to each price
    >>> total_after_tax_cost([2.0, 3.0], 0.13)
    5.65
    """
    return round(after_tax_cost(sum(prices), tax_rate), 2)

def total_after_tax_cost2(prices: list, tax_rate: float) -> float:
    cost = [price * (1 + tax_rate) for price in prices]
    return round(sum(cost), 2)


def strings_upper(strings: list) -> list:
    """Returns the same list of strings in all uppercase
    >>> strings_upper(['Hello', 'hi', 'vrinda'])
    ['HELLO', 'HI', 'VRINDA']
    """
    return [str.upper(s) for s in strings]


if __name__ == '__main__':
    import doctest
    doctest.testmod()


