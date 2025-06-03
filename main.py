import os
import time
from multiprocessing.util import get_logger
from pathlib import Path

import pandas as pd

from hypergraph_properties import (
    EmpiricalHGReader,
    HGFReader,
    SyntheticHGReader,
    XGIReader,
)
from hypergraph_properties.hg_pipeline.pipeline import run_pipeline
from hypergraph_properties.utils.git_info import get_current_commit_sha

logger = get_logger()

DESC_STATS_COLUMNS = [
    "avg_degree",
    "avg_he_size",
    "degree_sd",
    "he_size_sd",
    "min_degree",
    "max_degree",
    "min_he_size",
    "max_he_size",
    "n_incidence_edges",
    "n_vertices",
    "n_edges",
    "degree_skew",
    "he_size_skew",
]


def main() -> None:
    data = []

    for file in os.listdir(r"./data"):
        if file.startswith("coauth"):
            continue
        if "unique" in file:
            continue

        if file.endswith("hgf"):
            fmt = "hgf"
        elif file.startswith("ABCD"):
            fmt = "synthetic"
        elif file.endswith("txt"):
            fmt = "empirical"
        else:
            continue

        reader = {  # type: ignore[abstract]
            "empirical": EmpiricalHGReader,
            "synthetic": SyntheticHGReader,
            "hgf": HGFReader,
        }.get(fmt.lower(), HGFReader)()

        result = run_pipeline(reader, Path("data") / file)

        data.append(result.to_dict())

    for file in os.listdir(Path("data/xgi")):
        path = Path("data/xgi") / file
        if not path.is_file():
            continue
        result = run_pipeline(XGIReader(), path)

        data.append(result.to_dict())

    now = int(time.time())

    corr_result_filename = (
        f"corr_result_{now}_{get_current_commit_sha()}.csv"
    )
    desc_stats_filename = (
        f"descriptive_stats_{now}_{get_current_commit_sha()}.csv"
    )

    df = pd.DataFrame(data).set_index("name")

    df.drop(columns=DESC_STATS_COLUMNS).to_csv(str(Path("output") / corr_result_filename))
    df[DESC_STATS_COLUMNS].to_csv(str(Path("output") / desc_stats_filename))


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    logger.info(f"Finished in {time.perf_counter() - start} seconds")
