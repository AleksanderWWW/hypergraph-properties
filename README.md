# hypergraph-properties

## Python API:

```python
from hypergraph_properties.hg_properties.corr import node_corr
from hypergraph_properties.hg_reader.readers import EmpiricalHGReader
from hypergraph_properties.utils.logger import get_logger

logger = get_logger()

r = EmpiricalHGReader()

hg = r.read_graph("./data/tags-ask-ubuntu.txt")

corr = node_corr(hg, log_degrees=True)

logger.info(f"node_corr(hg, log_degrees=True) = {corr.statistic} (p={corr.pvalue})")

```

Output:

```text
[hypergraph-properties] [info   ] reading file ./data/tags-ask-ubuntu.txt
[hypergraph-properties] [info   ] reading ./data/tags-ask-ubuntu.txt complete
[hypergraph-properties] [info   ] node_corr(hg, log_degrees=True) = 0.3954907961556929 (p=5.7688107146332454e-114)
```


## CLI

```commandline
$ hypergraph-properties ./data/tags-ask-ubuntu.txt --fmt empirical
```

Output:

```text
[hypergraph-properties] [info   ] running `hypergraph-properties` pipeline on file ./data/tags-ask-ubuntu.txt
[hypergraph-properties] [info   ] expecting hypergraph to be in `empirical` format
[hypergraph-properties] [warning] final report will not be saved - pass an out-file with --out <filename>
[hypergraph-properties] [info   ] reading file ./data/tags-ask-ubuntu.txt
[hypergraph-properties] [info   ] reading ./data/tags-ask-ubuntu.txt complete
[hypergraph-properties] [info   ] node_corr(hg, log_degrees=True, log_avg_he_sizes=True) = 0.40539589371227935 (p=3.467592536283849e-120)
[hypergraph-properties] [info   ] node_corr(hg, log_degrees=True, log_avg_he_sizes=False) = 0.39228486251988537 (p=5.364449174601271e-112)
[hypergraph-properties] [info   ] node_corr(hg, log_degrees=False, log_avg_he_sizes=True) = 0.1718754643044873 (p=1.6272589030331839e-21)
[hypergraph-properties] [info   ] node_corr(hg, log_degrees=False, log_avg_he_sizes=False) = 0.1811359746915786 (p=9.358505850238468e-24)
```

```commandline
$ hypergraph-properties ./data/ABCD-h_seed_1235.txt --fmt synthetic
```

Output:

```text
[hypergraph-properties] [info   ] running `hypergraph-properties` pipeline on file ./data/ABCD-h_seed_1235.txt
[hypergraph-properties] [info   ] expecting hypergraph to be in `synthetic` format
[hypergraph-properties] [warning] final report will not be saved - pass an out-file with --out <filename>
[hypergraph-properties] [info   ] reading file ./data/ABCD-h_seed_1235.txt
[hypergraph-properties] [info   ] reading ./data/ABCD-h_seed_1235.txt complete
[hypergraph-properties] [info   ] node_corr(hg, log_degrees=True, log_avg_he_sizes=True) = 0.042010524165326274 (p=2.6248171997912895e-40)
[hypergraph-properties] [info   ] node_corr(hg, log_degrees=True, log_avg_he_sizes=False) = -0.0030696244883005866 (p=0.3317023506645107)
[hypergraph-properties] [info   ] node_corr(hg, log_degrees=False, log_avg_he_sizes=True) = 0.03416366260811625 (p=3.2060974145117905e-27)
[hypergraph-properties] [info   ] node_corr(hg, log_degrees=False, log_avg_he_sizes=False) = -0.0012296204410713741 (p=0.6973979034901194)
```

```commandline
$ hypergraph-properties ./data/nba.hgf --fmt hgf
```

Output:

```text
[hypergraph-properties] [info   ] running `hypergraph-properties` pipeline on file ./data/nba.hgf
[hypergraph-properties] [info   ] expecting hypergraph to be in `hgf` format
[hypergraph-properties] [warning] final report will not be saved - pass an out-file with --out <filename>
[hypergraph-properties] [info   ] reading file ./data/nba.hgf
[hypergraph-properties] [info   ] reading ./data/nba.hgf complete
[hypergraph-properties] [info   ] node_corr(hg, log_degrees=True, log_avg_he_sizes=True) = -0.5583289591842195 (p=8.140371877425156e-180)
[hypergraph-properties] [info   ] node_corr(hg, log_degrees=True, log_avg_he_sizes=False) = -0.5636493927828619 (p=5.833554811536166e-184)
[hypergraph-properties] [info   ] node_corr(hg, log_degrees=False, log_avg_he_sizes=True) = -0.46808336480683643 (p=1.0120255480796103e-119)
[hypergraph-properties] [info   ] node_corr(hg, log_degrees=False, log_avg_he_sizes=False) = -0.4667273354406076 (p=5.990069791878768e-119)
```