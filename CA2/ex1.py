"""This is exercise 1."""
__author__ = "Jack Shaw"


def vat(pretax_price: float, kids=False, category="miscellaneous") -> float:
    """This will calculate the total price of a purchase including tax."""
    tax = 0.2
    if (kids is True and category == "clothing") or category == "food":
        tax = 0
    price = pretax_price + pretax_price * tax
    return price
