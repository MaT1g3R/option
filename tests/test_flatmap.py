# MIT License

# Copyright (c) 2018-2021 Peijun Ma

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

from option import Err, NONE, Ok, Some
from tests.conftest import parametrize


@parametrize('option,maps,expected', [
    (Some(2), [lambda x: Some(x + 1)] * 2, Some(4)),
    (Some(2), [lambda x: Some(x + 1)] * 2 + [lambda x: NONE], NONE),
    (Some(2), [lambda x: NONE] + [lambda x: Some(x + 1)] * 2, NONE),
    (NONE, [lambda x: Some(x + 1)] * 2, NONE),
])
def test_option(option, maps, expected):
    for map_ in maps:
        option = option.flatmap(map_)
    assert option == expected


@parametrize('result,maps,expected', [
    (Ok(2), [lambda x: Ok(x + 1)] * 2, Ok(4)),
    (Ok(2), [lambda x: Ok(x + 1)] * 2 + [lambda x: Err(x + 1)], Err(5)),
    (Ok(2), [lambda x: Ok(x + 1)] * 2 + [lambda x: Err(x + 1)] + [lambda x: Ok(x + 1)], Err(5)),
    (Ok(2), [lambda x: Err(x + 1)] + [lambda x: Ok(x + 1)] * 2, Err(3)),
    (Err(2), [lambda x: Ok(x + 1)] * 2, Err(2)),
    (Err(2), [lambda x: Ok(x + 1)] * 2 + [lambda x: Err(x + 1)], Err(2)),
    (Err(2), [lambda x: Ok(x + 1)] * 2 + [lambda x: Err(x + 1)] + [lambda x: Ok(x + 1)], Err(2)),
    (Err(2), [lambda x: Err(x + 1)] + [lambda x: Ok(x + 1)] * 2, Err(2)),
])
def test_result(result, maps, expected):
    for map_ in maps:
        result = result.flatmap(map_)
    assert result == expected
