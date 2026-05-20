import numpy as np
from typing import TypeVar, Generic

T = TypeVar('T')

class NumpyArray(Generic[T]):
    def __init__(self, array: np.ndarray):
        self.array = array

    def get_array(self) -> np.ndarray:
        return self.array

    def set_array(self, array: np.ndarray) -> None:
        self.array = array

def create_numpy_array(array: np.ndarray) -> NumpyArray[np.float64]:
    return NumpyArray(array)

def test_numpy_integration() -> None:
    array = np.array([1.0, 2.0, 3.0])
    numpy_array = create_numpy_array(array)
    assert numpy_array.get_array().dtype == np.float64

if __name__ == "__main__":
    test_numpy_integration()