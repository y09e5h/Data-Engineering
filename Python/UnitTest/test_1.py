import pytest


def add(a,b):
    return a*b
def sub(a,b):
    return a-b
def div(a,b):
    return a/b

def testingadd():
    assert add(1,2) == 3

def testingsub():
    assert sub(-3,6) == -9

def testingZero():
    with pytest.raises(ZeroDivisionError):
        div(0,0)