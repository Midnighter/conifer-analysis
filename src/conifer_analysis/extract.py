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


"""Provide data extraction functions."""


from dask.dataframe import DataFrame, read_csv


def extract_tsv(path: str) -> DataFrame:
    """Extract conifer tables in a lazy fashion."""
    return read_csv(
        path,
        blocksize=None,
        include_path_column=True,
        sep="\t",
        header=None,
        names=[
            "marker",
            "identifier",
            "taxa",
            "read_lengths",
            "kraken",
            "read1_confidence",
            "read2_confidence",
            "avg_confidence",
        ],
    )
