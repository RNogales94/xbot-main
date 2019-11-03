import utils.register_utils as reg


def test_is_register_message():
    assert reg.is_register_message('/register mitag')
    assert reg.is_register_message('/register')
    assert reg.is_register_message('/register unatag-21 mas cosas')
    assert not reg.is_register_message('register unatag-21')
    assert not reg.is_register_message('/reg mitag-21')


