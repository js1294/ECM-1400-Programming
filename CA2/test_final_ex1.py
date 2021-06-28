from ex1 import vat

def test_vat_1():
    assert vat(pretax_price=1.0) == 1.2

def test_vat_str():
    assert vat(pretax_price='100') == 120

def test_vat_large():
    large=8e100
    assert vat(pretax_price=large) == large*1.2

def test_vat_kids():
    assert vat(pretax_price=1.0, kids=True) == 1.2

def test_vat_kids_clothing():
    assert vat(pretax_price=1.0, kids=True, category='clothing') == 1.0

def test_vat_keyword():
    assert vat(kids=False,pretax_price=2.0) == 2.4

def test_vat_keyword_category():
    assert vat(category='food',pretax_price=1.0) == 1.0
