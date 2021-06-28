from ex4 import obfuscate

def test_obfuscate_step1():
    input_text = 'and'
    assert obfuscate(input_text).lower() == 'the'

def test_obfuscate_step2():
    input_text = 'one'
    assert obfuscate(input_text) == 'onE'

def test_obfuscate_step3():
    input_text = 'one two three four five'
    assert obfuscate(input_text).split(' ')[4].lower() == 'evif'

def test_obfuscate_step4():
    input_text = 'one two three four five'
    assert obfuscate(input_text).split(' ')[1].lower() == 'uxp'

def test_obfuscate_all_steps():
    input_text = 'one two three four five six seven eight nine ten'
    expected = 'onE uXp ThrEe GpvS evIf tjY sEveN fJhiU nIne Ofu'
    assert obfuscate(input_text) == expected

def test_obfuscate_keyword_arg():
    assert obfuscate(text='a') == 'a'
