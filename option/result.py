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

"""This module contains the Result type."""
from typing import Any, Callable, Generic, Union

from .option_ import Option
from .types_ import E, F, T, U


class Result(Generic[T, E]):
    """
    :class:`Result` is a type that either success (:meth:`Result.Ok`)
    or failure (:meth:`Result.Err`).

    To create an Ok value, use :meth:`Result.Ok` or :func:`Ok`.

    To create a Err value, use :meth:`Result:Err` or :func:`Err`.

    Calling the :class:`Result` constructor directly will raise a ``TypeError``.

    Examples:
        >>> Result.Ok(1)
        Ok(1)
        >>> Result.Err('Fail!')
        Err('Fail!')
    """
    __slots__ = ('_val', '_is_ok')

    def __init__(self, val: Union[T, E], is_ok: bool, *, _force=False) -> None:
        if not _force:
            raise TypeError(
                'Cannot directly initialize, '
                'please use one of the factory functions instead.'
            )
        self._val = val
        self._is_ok = is_ok

    @classmethod
    def Ok(cls, val: T) -> 'Result[T, Any]':
        """
        Contains the success value.

        Args:
             val: The success value.

        Returns:
             The :class:`Result` containing the success value.

        Examples:
            >>> res = Result.Ok(1)
            >>> res
            Ok(1)
            >>> res.is_ok
            True
        """
        pass

    @classmethod
    def Err(cls, err: E) -> 'Result[Any, E]':
        """
        Contains the error value.

        Args:
            err: The error value.

        Returns:
            The :class:`Result` containing the error value.

        Examples:
            >>> res = Result.Err('Oh No')
            >>> res
            Err('Oh No')
            >>> res.is_err
            True
        """
        pass

    def __bool__(self):
        return self._is_ok

    @property
    def is_ok(self) -> bool:
        """
        Returns `True` if the result is :meth:`Result.Ok`.

        Examples:
            >>> Ok(1).is_ok
            True
            >>> Err(1).is_ok
            False
        """
        return self._is_ok

    @property
    def is_err(self) -> bool:
        """
        Returns `True` if the result is :meth:`Result.Err`.

        Examples:
            >>> Ok(1).is_err
            False
            >>> Err(1).is_err
            True
        """
        return not self._is_ok

    def ok(self) -> Option[T]:
        """
        Converts from :class`Result`[T, E] to :class:`Option`[T].

        Returns:
            :class:`Option` containing the success value if `self` is
            :meth:`Result.Ok`, otherwise :data:`NONE`.

        Examples:
            >>> Ok(1).ok()
            Option(1)
            >>> Err(1).ok()
            NONE
        """
        pass

    def err(self) -> Option[E]:
        """
        Converts from :class:`Result`[T, E] to :class:`Option`[E].

        Returns:
            :class:`Option` containing the error value if `self` is
            :meth:`Result.Err`, otherwise :data:`NONE`.

        Examples:
            >>> Ok(1).err()
            NONE
            >>> Err(1).err()
            Option(1)
        """
        pass

    def map(self, op: Callable[[T], U]) -> 'Result[U, E]':
        """
        Applies a function to the contained :meth:`Result.Ok` value.

        Args:
            op: The function to apply to the :meth:`Result.Ok` value.

        Returns:
            A :class:`Result` with its success value as the function result
            if `self` is an :meth:`Result.Ok` value, otherwise returns
            `self`.

        Examples:
            >>> Ok(1).map(lambda x: x * 2)
            Ok(2)
            >>> Err(1).map(lambda x: x * 2)
            Err(1)
        """
        pass

    def map_err(self, op: Callable[[E], F]) -> 'Result[T, F]':
        """
        Applies a function to the contained :meth:`Result.Err` value.

        Args:
            op: The function to apply to the :meth:`Result.Err` value.

        Returns:
            A :class:`Result` with its error value as the function result
            if `self` is a :meth:`Result.Err` value, otherwise returns
            `self`.

        Examples:
            >>> Ok(1).map(lambda x: x * 2)
            Ok(1)
            >>> Err(1).map(lambda x: x * 2)
            Err(2)
        """
        pass

    def unwrap(self) -> T:
        """
        Returns the success value in the :class:`Result`.

        Returns:
            The success value in the :class:`Result`.

        Raises:
            ``ValueError`` with the message provided by the error value
             if the :class:`Result` is a :meth:`Result.Err` value.

        Examples:
            >>> Ok(1).unwrap()
            1
            >>> try:
            ...     Err(1).unwrap()
            ... except ValueError as e:
            ...     print(e)
            1
        """
        pass

    def unwrap_or(self, optb: T) -> T:
        """
        Returns the success value in the :class:`Result` or ``optb``.

        Args:
            optb: The default return value.

        Returns:
            The success value in the :class:`Result` if it is a
            :meth:`Result.Ok` value, otherwise ``optb``.

        Notes:
            If you wish to use a result of a function call as the default,
            it is recommnded to use :meth:`unwrap_or_else` instead.

        Examples:
            >>> Ok(1).unwrap_or(2)
            1
            >>> Err(1).unwrap_or(2)
            2
        """
        pass

    def unwrap_or_else(self, op: Callable[[E], U]) -> Union[T, U]:
        """
        Returns the sucess value in the :class:`Result` or computes a default
        from the error value.

        Args:
            op: The function to computes default with.

        Returns:
            The success value in the :class:`Result` if it is
             a :meth:`Result.Ok` value, otherwise ``op(E)``.

        Examples:
            >>> Ok(1).unwrap_or_else(lambda e: e * 10)
            1
            >>> Err(1).unwrap_or_else(lambda e: e * 10)
            10
        """
        pass

    def expect(self, msg) -> T:
        """
        Returns the success value in the :class:`Result` or raises
        a ``ValueError`` with a provided message.

        Args:
            msg: The error message.

        Returns:
            The success value in the :class:`Result` if it is
            a :meth:`Result.Ok` value.

        Raises:
            ``ValueError`` with ``msg`` as the message if the
            :class:`Result` is a :meth:`Result.Err` value.

        Examples:
            >>> Ok(1).expect('no')
            1
            >>> try:
            ...     Err(1).expect('no')
            ... except ValueError as e:
            ...     print(e)
            no
        """
        pass

    def unwrap_err(self) -> E:
        """
        Returns the error value in a :class:`Result`.

        Returns:
            The error value in the :class:`Result` if it is a
            :meth:`Result.Err` value.

        Raises:
            ``ValueError`` with the message provided by the success value
             if the :class:`Result` is a :meth:`Result.Ok` value.

        Examples:
            >>> try:
            ...     Ok(1).unwrap_err()
            ... except ValueError as e:
            ...     print(e)
            1
            >>> Err('Oh No').unwrap_err()
            'Oh No'
        """
        pass

    def expect_err(self, msg) -> E:
        """
        Returns the error value in a :class:`Result`, or raises a
        ``ValueError`` with the provided message.

        Args:
            msg: The error message.

        Returns:
            The error value in the :class:`Result` if it is a
            :meth:`Result.Err` value.

        Raises:
            ``ValueError`` with the message provided by ``msg`` if
            the :class:`Result` is a :meth:`Result.Ok` value.

        Examples:
            >>> try:
            ...     Ok(1).expect_err('Oh No')
            ... except ValueError as e:
            ...     print(e)
            Oh No
            >>> Err(1).expect_err('Yes')
            1
        """
        pass

    def __repr__(self):
        return f'Ok({self._val!r})' if self._is_ok else f'Err({self._val!r})'

    def __hash__(self):
        pass

    def __eq__(self, other):
        pass

    def __ne__(self, other):
        pass

    def __lt__(self, other):
        pass

    def __le__(self, other):
        pass

    def __gt__(self, other):
        pass

    def __ge__(self, other):
        pass


def Ok(val: T) -> Result[T, Any]:
    """Shortcut function for :meth:`Result.Ok`."""
    return Result.Ok(val)


def Err(err: E) -> Result[Any, E]:
    """Shortcut function for :meth:`Result.Err`."""
    return Result.Err(err)
