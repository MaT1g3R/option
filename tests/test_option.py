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

from option import NONE, Option, Some, maybe
from tests import parametrize


@parametrize('is_some', [True, False])
def test_no_init(is_some):
    with pytest.raises(TypeError):
        if is_some:
            Option(1, True)
        else:
            Option(None, False)


@parametrize('obj', [Option.Some(1), Some(1)])
def test_some(obj):
    assert obj.is_some is True
    assert obj.is_none is False
    assert bool(obj)
    assert obj._val == 1


@parametrize('obj', [Option.NONE(), NONE])
def test_none(obj):
    assert obj.is_some is False
    assert obj.is_none is True
    assert bool(obj) is False
    assert obj._val is None


@parametrize('obj,is_some', [
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


@parametrize('obj,truth', [
    (Some(1), True),
    (NONE, False)
])
def test_bool(obj, truth):
    assert bool(obj) is truth


@parametrize('obj,raise_', [
    (Some(1), False),
    (NONE, True)
])
def test_except(obj, raise_):
    if raise_:
        with pytest.raises(ValueError):
            obj.expect('asd')
    else:
        assert obj.expect('asd') == 1


@parametrize('obj,raise_', [
    (Some(1), False),
    (Some(None), False),
    (NONE, True)
])
def test_value(obj, raise_):
    if raise_:
        with pytest.raises(ValueError):
            obj.value
        with pytest.raises(ValueError):
            obj.unwrap()
    else:
        assert obj.value == obj.unwrap() == obj._val


@parametrize('obj,default,exp', [
    (Some(0), 1, 0),
    (Some(False), 1, False),
    (NONE, 0, 0)
])
def test_unwrap_or(obj, default, exp):
    assert obj.unwrap_or(default) == exp
    assert obj.unwrap_or_else(lambda: default) == exp


def _raise(*args):
    raise ValueError


@parametrize('obj,func,exp', [
    (Some(1), lambda x: x * 2, Some(2)),
    (NONE, _raise, NONE),
    (Some('asd'), len, Some(3))
])
def test_map(obj, func, exp):
    assert obj.map(func) == exp


@parametrize('obj,func,default,exp', [
    (Some(1), lambda x: x * 2, 100, 2),
    (NONE, _raise, 100, 100),
    (Some('asd'), len, 100, 3)
])
def test_map_or(obj, func, default, exp):
    assert obj.map_or(func, default) == exp
    assert obj.map_or_else(func, lambda: default) == exp


@parametrize('obj,filt,exp', [
    (Some(1), lambda x: x % 2 == 0, NONE),
    (Some('asd'), lambda s: len(s) < 10, Some('asd')),
    (NONE, lambda x: True, NONE),
    (NONE, _raise, NONE)
])
def test_filter(obj, filt, exp):
    assert obj.filter(filt) == exp


@parametrize('a,b,exp', [
    (Some(1), NONE, NONE),
    (NONE, Some(1), NONE),
    (Some(2), Some('asd'), Some('asd')),
    (NONE, NONE, NONE)
])
def test_and(a, b, exp):
    assert (a and b) == exp


@parametrize('a,b,exp', [
    (Some(1), Some(2), Some(1)),
    (Some(1), NONE, Some(1)),
    (NONE, Some(1), Some(1)),
    (NONE, NONE, NONE),
])
def test_or(a, b, exp):
    assert (a or b) == exp


@parametrize('self,other', [
    (Some(1), Some(1)),
    (Some([1, 2]), Some([1, 2])),
    (Some({'': 'asd'}), Some({'': 'asd'})),
    (NONE, NONE)
])
def test_eq(self, other):
    assert self == other


@parametrize('self,other', [
    (Some(1), Some(2)),
    (NONE, Some(1)),
    (Some(1), NONE),
])
def test_ne(self, other):
    assert self != other


@parametrize('self,other', [
    (Some(1), Some(2)),
    (NONE, Some(0)),
    (NONE, Some(False)),
])
def test_lt_gt(self, other):
    assert self < other
    assert self <= other
    assert other > self
    assert other >= self


def test_le_ge():
    assert NONE <= NONE
    assert NONE >= NONE


@parametrize('self,other', [
    (Some(None), Some(1)),
    (Some(1), Some(None)),
    (Some(1), Some('')),
    (Some(''), Some(None)),
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


@parametrize('obj,key,default,exp', [
    (NONE, 1, None, NONE),
    (NONE, 1, 1, Some(1)),
    (Some({}), '', None, NONE),
    (Some({'': ''}), '', None, Some('')),
    (Some({'': ''}), 'aaa', 11, Some(11)),
])
def test_get(obj, key, default, exp):
    assert obj.get(key, default) == exp
