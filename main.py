import datetime
import os
from pathlib import Path

import pandas as pd

from hypergraph_properties import EmpiricalHGReader, SyntheticHGReader, HGFReader
from hypergraph_properties.pipeline import run_pipeline


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


    pd.DataFrame(data).to_csv(f"pipeline_result_{datetime.datetime.now()}.csv")


if __name__ == "__main__":
    main()
