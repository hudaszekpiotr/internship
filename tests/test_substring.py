from substring import length_of_longest_substring
import pytest


def test_empty():
    assert length_of_longest_substring("") == 0


def test_raising_error():
    with pytest.raises(ValueError):
        length_of_longest_substring(5)


def test_same_letter():
    assert length_of_longest_substring("GGGGG") == 1


def test_basic():
    assert length_of_longest_substring("ABCABCBB") == 3


def test_ASCI():
    s = r" !#$%&'\"()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{|}~"
    assert length_of_longest_substring(s) == len(s)

def test_long_string():
    s = r" !#$%&'\"()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{|}~"
    s_long = s*10000
    assert length_of_longest_substring(s_long) == len(s)