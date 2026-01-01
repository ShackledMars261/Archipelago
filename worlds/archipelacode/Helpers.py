from .Types import LocData
from typing import List


def split_array(locations: List[LocData], array_count: int) -> List[List[LocData]]:
    t: float = float(len(locations))
    result_arrays = [[] for _ in range(array_count)]
    for index, location in enumerate(locations):
        temp_array = result_arrays[
            round(((float(index) * float(array_count)) / float(t)) - 0.5)
        ]
        temp_array.append(location)
        result_arrays[round(((float(index) * float(array_count)) / float(t)) - 0.5)] = (
            temp_array
        )
    return result_arrays
