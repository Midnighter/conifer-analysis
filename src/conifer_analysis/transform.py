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


"""Provide data transformation functions."""


import numpy as np
import pandas as pd
from dask.dataframe import DataFrame


def tidy_conifer(ddf: DataFrame) -> DataFrame:
    """Tidy up the raw conifer output."""
    result = ddf.drop(columns=["marker", "identifier", "read_lengths", "kraken"])
    result[["name", "taxonomy_id"]] = result["taxa"].str.extract(
        r"^(?P<name>[\w ]+) \(taxid (?P<taxonomy_id>\d+)\)$", expand=True
    )
    return result.drop(columns=["taxa"]).categorize(
        columns=["name", "taxonomy_id"], index=False
    )


def _bin_group(df: pd.DataFrame, *, bins: np.ndarray) -> pd.DataFrame:
    """Perform actual binning of confidence values per group."""
    return (
        pd.DataFrame(
            {
                "midpoints": bins[1:] - (np.diff(bins) / 2),
                "read1_hist": df["read1_confidence"].value_counts(
                    bins=bins, sort=False
                ),
                "read2_hist": df["read2_confidence"].value_counts(
                    bins=bins, sort=False
                ),
                "avg_hist": df["avg_confidence"].value_counts(bins=bins, sort=False),
            }
        )
        .reset_index()
        .rename(columns={"index": "bin"})
    )


def bin_confidence(ddf: DataFrame, bins: np.ndarray) -> DataFrame:
    """Bin confidence values per path and taxa."""
    meta_df = (
        pd.DataFrame(
            columns=[
                "path",
                "taxonomy_id",
                "name",
                "bin",
                "midpoints",
                "read1_hist",
                "read2_hist",
                "avg_hist",
            ]
        )
        .astype(
            {
                "path": "category",
                "taxonomy_id": "category",
                "name": "category",
                "bin": "interval[float64, right]",
                "midpoints": np.float64,
                "read1_hist": np.float64,
                "read2_hist": np.float64,
                "avg_hist": np.float64,
            }
        )
        .set_index(["path", "name", "taxonomy_id"])
    )
    return ddf.groupby(
        ["path", "name", "taxonomy_id"], sort=False, group_keys=True, observed=True
    ).apply(_bin_group, bins=bins, meta=meta_df)
