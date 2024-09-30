# pyright: strict

#from __future__ import annotations
from typing import Any, List, cast

import pandas as pd
from shiny import reactive

df: pd.DataFrame = pd.DataFrame({
    'house': ['A', 'B', 'C', 'D'],
    'price': [250000, 400000, 320000, 550000],
    'sq_ft': [1800, 2200, 1500, 2800]
})

col: pd.Series[str] = df["house"]

idx_int: pd.Index[Any] = pd.Index([1, 2, 3])
idx_int: pd.Index[int] = pd.Index([1, 2, 3])
idx_str: pd.Index[str] = pd.Index(["hello", "world"])

print(idx_int)
print(idx_str)

def return_index(df: pd.DataFrame) -> "pd.Index[Any]":
    """This function exists to make pyright errors go away
    when trying to pull the .index of a dataframe
    """
    return cast("pd.Index[Any]", df.index)


idx: set[int] = set(cast("pd.Index[Any]", df.index)) # <<

var: "pd.Index[Any]"= df.index

@reactive.calc
def filter_idx() -> List[pd.Index[Any]]:
    idx: set[int] = set(cast(pd.Index[Any], df.index)) # <<


    current_idx: pd.Index[Any] = df.loc[df["day"].isin(input.filter_day())].index
    idx: Set[pd.Index] = idx.intersection(set(current_idx)) # <<


    current_idx: pd.Index[Any] = df.loc[df["time"].isin(input.filter_time())].index
    idx = idx.intersection(set(current_idx)) # <<

    return list(idx) # list because .loc[] would return TypeError# <<
