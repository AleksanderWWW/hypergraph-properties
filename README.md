# hypergraph-properties

Example flow:

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
