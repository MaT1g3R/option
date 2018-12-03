# MIT License

# Copyright (c) 2018 Peijun Ma

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pytest

from option import Err, NONE, Ok, Result, Some
from tests.conftest import parametrize


@parametrize('args', [
    (1, True),
    (0, False)
])
def test_no_init(args):
    with pytest.raises(TypeError):
        Result(*args)


@parametrize('val', [0, None, {}, [], False])
def test_factory_ok(val):
    res = Result.Ok(val)
    assert res._is_ok
    assert res._val == val


@parametrize('err', [0, None, '', [], False])
def test_factory_err(err):
    res = Result.Err(err)
    assert not res._is_ok
    assert res._val == err


@parametrize('ok', [True, False])
def test_bool(ok):
    res = Result.Ok(1) if ok else Result.Err(1)
    assert bool(res) == ok
    assert res.is_ok == ok
    assert res.is_err != ok


@parametrize('ok', [True, False])
def test_ok_err(ok):
    res = Result.Ok(1) if ok else Result.Err(1)
    if ok:
        assert res.ok() == Some(1)
        assert res.err() == NONE
    else:
        assert res.ok() == NONE
        assert res.err() == Some(1)


@parametrize('obj,call,exp', [
    (Ok(1), str, Ok('1')),
    (Err(1), str, Err(1))
])
def test_map(obj, call, exp):
    assert obj.map(call) == exp


@parametrize('obj,call,exp', [
    (Ok(1), str, Ok(1)),
    (Err(1), str, Err('1'))
])
def test_map_err(obj, call, exp):
    assert obj.map_err(call) == exp


@parametrize('obj,exp,ok', [
    (Ok(1), 1, True),
    (Ok(None), None, True),
    (Err(1), 1, False),
])
def test_unwrap(obj, exp, ok):
    if ok:
        assert obj.unwrap() == exp
    else:
        with pytest.raises(ValueError):
            obj.unwrap()


@parametrize('obj,optb,exp', [
    (Ok(0), 11, 0),
    (Err(11), 0, 0)
])
def test_unwrap_or(obj, optb, exp):
    assert obj.unwrap_or(optb) == exp


@parametrize('obj,op,exp', [
    (Ok('asd'), len, 'asd'),
    (Err('asd'), len, 3),
])
def test_unwrap_or_else(obj, op, exp):
    assert obj.unwrap_or_else(op) == exp


@parametrize('obj,ok,exp', [
    (Ok(1), True, 1),
    (Err(1), False, ''),
    (Ok(None), True, None)
])
def test_except(obj, ok, exp):
    if ok:
        assert obj.expect('') == exp
    else:
        with pytest.raises(ValueError):
            obj.expect('')


@parametrize('obj,err,exp', [
    (Ok(1), False, ''),
    (Err(None), True, None),
])
def test_unwrap_expect_err(obj, err, exp):
    if err:
        assert obj.unwrap_err() == exp
        assert obj.expect_err('') == exp
    else:
        with pytest.raises(ValueError):
            obj.unwrap_err()
        with pytest.raises(ValueError):
            obj.expect_err('')


@parametrize('obj1,obj2,eq', [
    (Ok(1), Ok(1), True),
    (Err(1), Err(1), True),
    (Ok(1), Err(1), False)
])
def test_hash(obj1, obj2, eq):
    if eq:
        assert hash(obj1) == hash(obj2)
    else:
        assert hash(obj1) != hash(obj2)


@parametrize('o1,o2', [
    (Ok(''), Ok('')),
    (Ok([]), Ok([])),
    (Err('aa'), Err('aa')),
    (Err({}), Err({}))
])
def test_eq(o1, o2):
    assert o1 == o2
    assert not o1 == o1._val
    assert not o1._val == o1


@parametrize('o1,o2', [
    (Ok(''), Err('')),
    (Err([]), Ok([])),
    (Ok({}), Err({})),
    (Ok(1), Ok(2)),
    (Err(2), Err(3))
])
def test_neq(o1, o2):
    assert o1 != o2
    assert o1 != o1._val
    assert o1._val != o1


@parametrize('o1,o2', [
    (Ok(2), Err(1)),
    (Ok(1), Ok(2)),
    (Err(1), Err(2))
])
def test_lt_gt(o1, o2):
    assert o1 < o2
    assert o1 <= o2
    assert o2 > o1
    assert o2 >= o1


@parametrize('o1,o2', [
    (Ok(1), Ok(1)),
    (Err(1), Err(1))
])
def test_le_ge(o1, o2):
    assert o1 <= o2
    assert o1 >= o2


@parametrize('self,other', [
    (Err(None), Err(1)),
    (Ok(1), Ok(None)),
    (Ok(1), Ok('')),
    (Ok(''), Ok(None)),
    (Ok(1), 1),
    (1, Err(1))
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
