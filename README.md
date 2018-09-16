# Option
[![Build Status](https://travis-ci.org/MaT1g3R/option.svg?branch=master)](https://travis-ci.org/MaT1g3R/option)
[![codecov](https://codecov.io/gh/MaT1g3R/option/branch/master/graph/badge.svg)](https://codecov.io/gh/MaT1g3R/option)

A [rust-like](https://doc.rust-lang.org/std/option/enum.Option.html) `Option` type in Python, slotted and fully typed.

An `Option` type represents an optional value, every `Option` is either `Some` and contains Some value, or `NONE`

Using an `Option` type forces you to deal with `None` values in your code and increase type safety.

## Quick Start
```Python
from option import Some, NONE, Option
from requests import get

def call_api(url, params) -> Option[dict]:
    result = get(url, params)
    if result.status_code == 200:
        return Some(result.json())
    return NONE

# Instead of checking for None, the NONE case is always dealt with.
dict_len = call_api(url, params).map(len)
```

## Install
Option can be installed from PyPi:
```bash
pip install option
```

## Documentation
The documentation lives at https://mat1g3r.github.io/option/

## License
MIT
