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
[hypergraph-properties] [warning] final report will not be saved
[hypergraph-properties] [info   ] reading file ./data/tags-ask-ubuntu.txt
[hypergraph-properties] [info   ] reading ./data/tags-ask-ubuntu.txt complete
[hypergraph-properties] [info   ] node_corr(hg, log_degrees=True, log_avg_he_sizes=True) = 0.41230378723158423 (p=1.187410149783796e-124)
[hypergraph-properties] [info   ] node_corr(hg, log_degrees=True, log_avg_he_sizes=False) = 0.3954907961556929 (p=5.7688107146332454e-114)
[hypergraph-properties] [info   ] node_corr(hg, log_degrees=False, log_avg_he_sizes=True) = 0.1662450181861485 (p=3.264299752282773e-20)
[hypergraph-properties] [info   ] node_corr(hg, log_degrees=False, log_avg_he_sizes=False) = 0.1811359746915786 (p=9.358505850238468e-24)
```

```commandline
$ hypergraph-properties ./data/ABCD-h_seed_1235.txt --fmt synthetic
```

Output:

```text
[hypergraph-properties] [info   ] running `hypergraph-properties` pipeline on file ./data/ABCD-h_seed_1235.txt
[hypergraph-properties] [info   ] expecting hypergraph to be in `synthetic` format
[hypergraph-properties] [warning] final report will not be saved
[hypergraph-properties] [info   ] reading file ./data/ABCD-h_seed_1235.txt
[hypergraph-properties] [info   ] reading ./data/ABCD-h_seed_1235.txt complete
[hypergraph-properties] [info   ] node_corr(hg, log_degrees=True, log_avg_he_sizes=True) = 0.04912133992232744 (p=1.7825487853823948e-54)
[hypergraph-properties] [info   ] node_corr(hg, log_degrees=True, log_avg_he_sizes=False) = -0.0031835560335866037 (p=0.31406993512870207)
[hypergraph-properties] [info   ] node_corr(hg, log_degrees=False, log_avg_he_sizes=True) = 0.039342929809835725 (p=1.4705032026097002e-35)
[hypergraph-properties] [info   ] node_corr(hg, log_degrees=False, log_avg_he_sizes=False) = -0.0012296204410713741 (p=0.6973979034901194)
```
