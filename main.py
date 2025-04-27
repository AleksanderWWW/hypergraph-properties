import time
import os
from pathlib import Path

import pandas as pd

from hypergraph_properties import EmpiricalHGReader, SyntheticHGReader, HGFReader, XGIReader
from hypergraph_properties.hg_pipeline.pipeline import run_pipeline
from hypergraph_properties.utils.git_info import get_current_commit_sha


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


    filename = f"pipeline_result_{int(time.time())}_{get_current_commit_sha()}.csv"
    pd.DataFrame(data).set_index("name").to_csv(filename)


if __name__ == "__main__":
    main()
