"""This is exercise 2."""
__author__ = "Jack Shaw"


def email_addresses(first: list, last: list, domain="@exeter.ac.uk") -> list:
    """This will take names and a domain and return a list of emails based off this."""
    length_first = len(first)
    length_last = len(last)
    email_list = []

    if length_first != length_last:
        print("Error - first and last are not the same size")
        return []
    for index in range(length_first):
        email = first[index][0] + "." + last[index] + domain
        email = str.lower(email)
        email_list.append(email)
    return email_list
