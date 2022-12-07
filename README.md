# DNAmetabarcoding
data processing for DNA metabarcoding

This repo currently consists of a single data processing script:
`contingency.py`

General instructions that guided the development of the script are found in:
`contingency.table.flow.txt`

The script currently takes ~8 minutes to run, and could be significantly optimized if needed.
The script depends on an `input` directory existing at the same level, that includes:
- `listofclusters_AMD18S_swarm_fastidious_shortnames.txt`
- `test_shortnames.tab`
- `statistics_swarm_fastidious_shortnames.txt`

The `output` directory will be created if it does not exist. Final output will be written to:
`output/final_contingency.txt` (tab-delimited text file)

The `output` and `input` directories are included in `.gitignore`, therefore they will not be pushed to this repo.

The packages needed to run the code are listed in `requirements.txt`. Note that these packages include `numba` and dependencies, which can be used to speed up the processing time for this code (future task). To get started all you really should need is `pandas`, which can be installed with `pip install pandas` (`numpy` will also be installed as a dependency of `pandas`). If you are running conda or miniconda, you should be good to just run the code.


