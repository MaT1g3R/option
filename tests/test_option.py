# MIT License
#
# Copyright (c) 2018 Peijun Ma
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pytest

from option import NONE, NoneError, Option, maybe, some


@pytest.mark.parametrize('is_some', [True, False])
def test_no_init(is_some):
    with pytest.raises(TypeError):
        if is_some:
            Option(1, True)
        else:
            Option(None, False)


@pytest.mark.parametrize('obj', [Option.some(1), some(1)])
def test_some(obj):
    assert obj.is_some is True
    assert obj.is_none is False
    assert bool(obj)
    assert obj._val == 1


@pytest.mark.parametrize('obj', [Option.none(), NONE])
def test_none(obj):
    assert obj.is_some is False
    assert obj.is_none is True
    assert bool(obj) is False
    assert obj._val is None


@pytest.mark.parametrize('obj,is_some', [
    (maybe(0), True),
    (maybe(0.0), True),
    (maybe(''), True),
    (maybe([]), True),
    (maybe({}), True),
    (maybe(()), True),
    (maybe(set()), True),
    (maybe(None), False),
    (maybe(1), True),
    (maybe(True), True),
    (maybe(False), True)
])
def test_maybe(obj, is_some):
    if is_some:
        assert obj.is_some
    else:
        assert obj.is_none


@pytest.mark.parametrize('obj,truth', [
    (some(1), True),
    (NONE, False)
])
def test_bool(obj, truth):
    assert bool(obj) is truth


@pytest.mark.parametrize('obj,raise_', [
    (some(1), False),
    (NONE, True)
])
def test_except(obj, raise_):
    if raise_:
        with pytest.raises(ValueError):
            obj.except_('asd')
    else:
        assert obj.except_('asd') == 1


@pytest.mark.parametrize('obj,raise_', [
    (some(1), False),
    (some(None), False),
    (NONE, True)
])
def test_value(obj, raise_):
    if raise_:
        with pytest.raises(NoneError):
            obj.value
        with pytest.raises(NoneError):
            obj.unwrap()
    else:
        assert obj.value == obj.unwrap() == obj._val


@pytest.mark.parametrize('obj,default,exp', [
    (some(0), 1, 0),
    (some(False), 1, False),
    (NONE, 0, 0)
])
def test_unwrap_or(obj, default, exp):
    assert obj.unwrap_or(default) == exp
    assert obj.unwrap_or_else(lambda: default) == exp


def _raise(*args):
    raise ValueError


@pytest.mark.parametrize('obj,func,exp', [
    (some(1), lambda x: x * 2, some(2)),
    (NONE, _raise, NONE),
    (some('asd'), len, some(3))
])
def test_map(obj, func, exp):
    assert obj.map(func) == exp


@pytest.mark.parametrize('obj,func,default,exp', [
    (some(1), lambda x: x * 2, 100, 2),
    (NONE, _raise, 100, 100),
    (some('asd'), len, 100, 3)
])
def test_map_or(obj, func, default, exp):
    assert obj.map_or(func, default) == exp
    assert obj.map_or_else(func, lambda: default) == exp


@pytest.mark.parametrize('obj,filt,exp', [
    (some(1), lambda x: x % 2 == 0, NONE),
    (some('asd'), lambda s: len(s) < 10, some('asd')),
    (NONE, lambda x: True, NONE),
    (NONE, _raise, NONE)
])
def test_filter(obj, filt, exp):
    assert obj.filter(filt) == exp


@pytest.mark.parametrize('a,b,exp', [
    (some(1), NONE, NONE),
    (NONE, some(1), NONE),
    (some(2), some('asd'), some('asd')),
    (NONE, NONE, NONE)
])
def test_and(a, b, exp):
    assert (a and b) == exp


@pytest.mark.parametrize('a,b,exp', [
    (some(1), some(2), some(1)),
    (some(1), NONE, some(1)),
    (NONE, some(1), some(1)),
    (NONE, NONE, NONE),
])
def test_or(a, b, exp):
    assert (a or b) == exp


@pytest.mark.parametrize('self,other', [
    (some(1), some(1)),
    (some([1, 2]), some([1, 2])),
    (some({'': 'asd'}), some({'': 'asd'})),
    (NONE, NONE)
])
def test_eq(self, other):
    assert self == other


@pytest.mark.parametrize('self,other', [
    (some(1), some(2)),
    (NONE, some(1)),
    (some(1), NONE),
])
def test_ne(self, other):
    assert self != other


@pytest.mark.parametrize('self,other', [
    (some(1), some(2)),
    (NONE, some(0)),
    (NONE, some(False)),
])
def test_lt_gt(self, other):
    assert self < other
    assert self <= other
    assert other > self
    assert other >= self


def test_le_ge():
    assert NONE <= NONE
    assert NONE >= NONE


@pytest.mark.parametrize('self,other', [
    (some(None), some(1)),
    (some(1), some(None)),
    (some(1), some('')),
    (some(''), some(None)),
])
def test_lt_gt_type_error(self, other):
    with pytest.raises(TypeError):
        self < other
    with pytest.raises(TypeError):
        self <= other
    with pytest.raises(TypeError):
        self > other
    with pytest.raises(TypeError):
        self >= other


@pytest.mark.parametrize('obj,key,default,exp', [
    (NONE, 1, None, NONE),
    (NONE, 1, 1, some(1)),
    (some({}), '', None, NONE),
    (some({'': ''}), '', None, some('')),
    (some({'': ''}), 'aaa', 11, some(11)),
])
def test_get(obj, key, default, exp):
    assert obj.get(key, default) == exp
