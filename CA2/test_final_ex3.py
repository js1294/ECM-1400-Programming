from ex3 import five_a_side_selector
from functools import reduce

def test_five_a_side_selector_adjacent():
    names = ["David", "Ronaldo", "Matthew", "Jacq", "Johan", "Achim"]
    teams = five_a_side_selector(names.copy())
    assert not (( names[0] in teams[0] ) and( names[1] in teams[0] ))

def test_teams_less_than_20():
    names = ['David', 'Ronaldo', 'Matt', 'Jacq', 'Johan', 'Achim',
        'Ed', 'Diego', 'Sareh', 'Khulood']
    assert len(five_a_side_selector(names)) == 2

def test_teams_more_than_20():
    names = [str(i) for i in range(29)]
    teams = five_a_side_selector(names)
    assert len(teams) == 5
    assert len(teams[0]) in [5 , 6]

def test_all_names_in_teams():
    names = [str(i) for i in range(29)]
    teams = five_a_side_selector(names)
    assert reduce(lambda a,b: a+b, map(len,teams)) == 29

