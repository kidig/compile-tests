
# START HIDDEN BLOCK
def test_valid(value):
    assert value is True, 'value is not true'


def test_invalid(value):
    assert value is False, 'value is not false'

# END HIDDEN BLOCK


def foo(bar):
    # HIDDEN TESTS
    test_valid(bar)
    test_invalid(bar)
    # HIDDEN TESTS

    test_valid(bar)
    test_invalid(bar)


foo(True)
