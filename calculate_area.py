import math

def calculate_area(radius: float) -> float:
    """
    Calculate the area of a circle given its radius.

    Args:
        radius (float): The radius of the circle. Must be non-negative.

    Returns:
        float: The area of the circle.

    Raises:
        ValueError: If the radius is negative.
    """
    if radius < 0:
        raise ValueError("Radius cannot be negative.")
    return math.pi * radius ** 2
