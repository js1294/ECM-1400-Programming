from ex2 import email_addresses

def test_email_addresses():
    first = ['David', 'Ronaldo', 'Matthew', 'Jacq', 'Johan', 'Achim']
    last = ['Wakeling', 'Menezes', 'Collison', 'Christmas', 'Whalstrōm', 'Bruker']
    emails = ['d.wakeling@exeter.ac.uk', 'r.menezes@exeter.ac.uk',
        'm.collison@exeter.ac.uk', 'j.christmas@exeter.ac.uk',
        'j.whalstrōm@exeter.ac.uk', 'a.bruker@exeter.ac.uk']
    assert email_addresses(first, last) == emails

#def test_email_inlcuding_at():
#    first = ['m@tthew', 'd@vid']
#    last = ['collison', 'w@keling']
#    assert email_addresses(first, last) == ['m.collison@exeter.ac.uk', 'd.wkeling@exeter.ac.uk']

def test_keyword_args():
    assert email_addresses(last=['relaxing'],first=['matt'],domain='@home') == ['m.relaxing@home']

def test_lower_only():
    assert email_addresses(['m'],['collison']) == ['m.collison@exeter.ac.uk']

