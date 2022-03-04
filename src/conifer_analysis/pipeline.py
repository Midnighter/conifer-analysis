# Copyright (c) 2022, Moritz E. Beber.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Provide complete dask ETL pipelines."""


import numpy as np
import pandas as pd

from .extract import extract_tsv
from .transform import bin_confidence, tidy_conifer


DEFAULT_BINS = np.linspace(0, 1, 51)


def confidence_hist(path: str, bins: np.ndarray = DEFAULT_BINS) -> pd.DataFrame:
    """Compute confidence value bins per path and taxa and return a data frame."""
    return (
        extract_tsv(path)
        .pipe(tidy_conifer)
        .pipe(bin_confidence, bins=bins)
        .compute()
        .droplevel(-1)
        .reset_index()
    )
