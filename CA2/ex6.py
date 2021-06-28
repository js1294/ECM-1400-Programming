"""This is exercise 6."""
__author__ = "Jack Shaw"


def arrival(name: str) -> list:
    """This will add a name to the end of the queue."""
    queue.append(name)
    return queue


def next_patient(position=1) -> list:
    """This will remove the patient from the position entered in the queue."""
    queue.remove(queue[position - 1])
    return queue


queue = []
