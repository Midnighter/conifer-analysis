=============================
Conifer Analysis
=============================

.. image:: https://img.shields.io/pypi/v/conifer-analysis.svg
   :target: https://pypi.org/project/conifer-analysis/
   :alt: Current PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/conifer-analysis.svg
   :target: https://pypi.org/project/conifer-analysis/
   :alt: Supported Python Versions

.. image:: https://img.shields.io/pypi/l/conifer-analysis.svg
   :target: https://www.apache.org/licenses/LICENSE-2.0
   :alt: Apache Software License Version 2.0

.. image:: https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg
   :target: .github/CODE_OF_CONDUCT.md
   :alt: Code of Conduct

.. image:: https://github.com/Midnighter/conifer-analysis/workflows/CI-CD/badge.svg
   :target: https://github.com/Midnighter/conifer-analysis/workflows/CI-CD
   :alt: GitHub Actions

.. image:: https://codecov.io/gh/Midnighter/conifer-analysis/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/Midnighter/conifer-analysis
   :alt: Codecov

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black
   :alt: Code Style Black

.. image:: https://readthedocs.org/projects/conifer-analysis/badge/?version=latest
   :target: https://conifer-analysis.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. summary-start

Post-process conifer output for downstream statistical analysis.

``conifer-analysis`` uses `dask <https://dask.org/>`_ in order to analyze
`conifer <https://github.com/Ivarz/Conifer>`_ results in a distributed and
out-of-memory fashion. This can be helpful when processing many such results.

Example
=======

Say that you have a bunch of ``conifer`` results in a directory. You can
generate a histogram of the confidence values per file (sample) and per taxa
using the provided pipeline ``confidence_hist``. Even when you work locally, it
can be helpful to explicitly create a distributed client controlling the number
of workers.

.. code-block:: python

    from dask.distributed import Client
    from conifer_analysis import confidence_hist

    client = Client(n_workers=8)

You can then visit the `default dashboard <http://127.0.0.1:8787/status>`_ in
your browser to observe tasks live.  Next, we run the pipeline which returns a
``pandas.DataFrame``.

.. code-block:: python

    hist = confidence_hist("data/*.tsv")
    hist.info()

As an example of the returned shape:

.. code-block:: console

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 7700 entries, 0 to 7699
    Data columns (total 8 columns):
     #   Column       Non-Null Count  Dtype
    ---  ------       --------------  -----
     0   path         7700 non-null   category
     1   name         7700 non-null   category
     2   taxonomy_id  7700 non-null   category
     3   bin          7700 non-null   interval[float64, right]
     4   midpoints    7700 non-null   float64
     5   read1_hist   7700 non-null   int64
     6   read2_hist   7700 non-null   int64
     7   avg_hist     7700 non-null   int64
    dtypes: category(3), float64(1), int64(3), interval(1)
    memory usage: 385.3 KB


Install
=======

It's as simple as:

.. code-block:: console

    pip install conifer-analysis

If you want to observe tasks in the dask dashboard, you will need additional
dependencies.

.. code-block:: console

    pip install conifer-analysis[dashboard]

Copyright
=========

* Copyright © 2022, Moritz E. Beber.
* Free software distributed under the `Apache Software License 2.0
  <https://www.apache.org/licenses/LICENSE-2.0>`_.

.. summary-end
