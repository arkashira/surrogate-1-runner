
from typing import TypeVar, Generic, List
import pandas as pd
import numpy as np

T = TypeVar('T')

class HKTList(Generic[T]):
    def __init__(self, data: List[T]):
        self.data = data

    def to_pandas(self) -> pd.DataFrame:
        return pd.DataFrame(self.data)

# Example usage:
hkt_list = HKTList([1, 2, 3, 4, 5])
df = hkt_list.to_pandas()
print(df)

# /opt/axentx/surrogate-1/python_hkt/tests/test_pandas_integration.py

import pandas as pd
import numpy as np
from python_hkt.pandas_integration import HKTList

def test_hkt_list_to_pandas():
    hkt_list = HKTList([1, 2, 3, 4, 5])
    df = hkt_list.to_pandas()
    pd.testing.assert_frame_equal(df, pd.DataFrame([1, 2, 3, 4, 5]))

## Summary
- Implemented `HKTList` class with higher-kinded type variable `T`.
- Added `to_pandas` method to convert `HKTList` to a pandas DataFrame.
- Created a test case to validate the `to_pandas` method.