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

from typing import Callable, Generic, Union

from .types_ import A, NoneError, T, U, _NoneError


class Option(Generic[T]):
    __slots__ = ('_val', '_is_some')

    def __init__(self, value: T, is_some: bool, *, _force: bool = False):
        if not _force:
            raise TypeError(
                'Cannot directly initialize, '
                'please use one of the factory functions instead.'
            )
        self._val = value
        self._is_some = is_some

    @classmethod
    def some(cls, val: T) -> 'Option[T]':
        return cls(val, True, _force=True)

    @classmethod
    def none(cls) -> 'Option[None]':
        return NONE

    @classmethod
    def maybe(cls, val: T) -> 'Option[T]':
        return NONE if val is None else cls.some(val)

    def __bool__(self):
        return self._is_some

    @property
    def is_some(self) -> bool:
        return self.__bool__()

    @property
    def is_none(self) -> bool:
        return not self.__bool__()

    def except_(self, msg) -> T:
        if self._is_some:
            return self._val
        raise NoneError(msg)

    def unwrap(self) -> T:
        return self.value

    @property
    def value(self) -> T:
        if self._is_some:
            return self._val
        raise _NoneError

    def unwrap_or(self, default: U) -> Union[T, U]:
        return self.unwrap_or_else(lambda: default)

    def unwrap_or_else(self, callback: Callable[[], U]) -> Union[T, U]:
        return self._val if self._is_some else callback()

    def map(self, callback: Callable[[T], U]) -> 'Option[U]':
        return self.some(callback(self._val)) if self._is_some else NONE

    def map_or(self, callback: Callable[[T], U], default: A) -> Union[U, A]:
        return callback(self._val) if self._is_some else default

    def map_or_else(self, callback: Callable[[T], U], default: Callable[[], A]) -> Union[U, A]:
        return callback(self._val) if self._is_some else default()

    def filter(self, predicate: Callable[[T], bool]) -> 'Option[T]':
        return self if self._is_some and predicate(self._val) else NONE

    def __hash__(self):
        return hash((self.__class__, self._is_some, self._val))

    def __eq__(self, other: 'Option'):
        return (isinstance(other, type(self))
                and self._is_some == other._is_some
                and self._val == other._val)

    def __ne__(self, other):
        return (not isinstance(other, type(self))
                or self._is_some != other._is_some
                or self._val != other._val)

    def __lt__(self, other):
        if isinstance(other, type(self)):
            if self._is_some == other._is_some:
                return self._val < other._val if self._is_some else False
            else:
                return other._is_some
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, type(self)):
            if self._is_some == other._is_some:
                return self._val <= other._val if self._is_some else True
            return other._is_some
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, type(self)):
            if self._is_some == other._is_some:
                return self._val > other._val if self._is_some else False
            else:
                return self._is_some
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, type(self)):
            if self._is_some == other._is_some:
                return self._val >= other._val if self._is_some else True
            return self._is_some
        return NotImplemented

    def __repr__(self):
        return 'none' if self.is_none else f'some({self._val!r})'


def some(val: T) -> Option[T]:
    return Option.some(val)


def maybe(val: T) -> Option[T]:
    return Option.maybe(val)


NONE = Option(None, False, _force=True)
