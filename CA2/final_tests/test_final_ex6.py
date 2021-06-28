from ex6 import arrival
from ex6 import next_patient
import ex6

def test_next_patient():
    ex6.queue = ["David", "Matt"]
    next_patient(1)
    assert ex6.queue == ["Matt"]

def test_next_patient_keyword_arg():
    ex6.queue = ["David", "Matt"]
    next_patient(position=1)
    assert ex6.queue == ["Matt"]

def test_arrival():
    ex6.queue = ["David", "Matt"]
    arrival("Ronaldo")
    assert ex6.queue == ["David", "Matt","Ronaldo"]

test_next_patient_keyword_arg()
test_next_patient()
test_arrival()
