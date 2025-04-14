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
$ hypergraph-properties ./data/threads-ask-ubuntu.hgf --fmt hgf --html-report
```

Output:

```text
[hypergraph-properties] [info   ] running `hypergraph-properties` pipeline on file ./data/threads-ask-ubuntu.hgf
[hypergraph-properties] [info   ] expecting hypergraph to be in `hgf` format
[hypergraph-properties] [info   ] reading file ./data/threads-ask-ubuntu.hgf
[hypergraph-properties] [info   ] reading ./data/threads-ask-ubuntu.hgf complete
[hypergraph-properties] [info   ] node_corr(hg, log_degrees=False, log_avg_he_sizes=False) = 0.04039681603957261 (p=1.5835648248929718e-46)
[hypergraph-properties] [info   ] node_corr(hg, log_degrees=True, log_avg_he_sizes=False) = 0.12526492858056895 (p=0.0)
[hypergraph-properties] [info   ] node_corr(hg, log_degrees=False, log_avg_he_sizes=True) = 0.048067464711542135 (p=3.809320136716598e-65)
[hypergraph-properties] [info   ] node_corr(hg, log_degrees=True, log_avg_he_sizes=True) = 0.1580846868633572 (p=0.0)
[hypergraph-properties] [info   ] HTML report saved at threads-ask-ubuntu.html
```

### Interface spec

```text
Usage: hypergraph-properties [OPTIONS] FILENAME

Options:
  --fmt [empirical|synthetic|hgf]
  --html-report
```