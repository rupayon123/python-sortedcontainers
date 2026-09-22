import pytest

from sortedcontainers import SortedSet


@pytest.mark.parametrize('key', [None, int])
def test_failed_add_preserves_membership_and_sorted_index(key):
    values = SortedSet([1, 2, 3], key=key)
    with pytest.raises((TypeError, ValueError)):
        values.add('invalid')
    assert 'invalid' not in values
    assert len(values) == 3
    assert list(values) == [1, 2, 3]
    values._check()
    values.add(4)
    assert values.pop() == 4
    values._check()


def test_failed_add_key_can_be_retried():
    def key(value):
        if fail[0]:
            raise ValueError('cannot calculate key')
        return value

    fail = [False]
    values = SortedSet([1], key=key)
    fail[0] = True
    with pytest.raises(ValueError, match='cannot calculate key'):
        values.add(2)
    fail[0] = False
    values.add(2)
    assert list(values) == [1, 2]
    values._check()
