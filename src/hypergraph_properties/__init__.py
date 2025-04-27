import json

import click

from hypergraph_properties.hg_pipeline.pipeline import run_pipeline
from hypergraph_properties.hg_reader.readers import (
    EmpiricalHGReader,
    HGFReader,
    SyntheticHGReader,
    XGIReader,
)
from hypergraph_properties.hg_reader.template import HypergraphReader
from hypergraph_properties.utils.logger import get_logger

logger = get_logger()


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option(
    "--fmt",
    type=click.Choice(["empirical", "synthetic", "hgf", "xgi"], case_sensitive=False),
)
def main(filename: click.Path, fmt: str) -> None:
    logger.info(f"running `hypergraph-properties` pipeline on file {filename}")
    logger.info(f"expecting hypergraph to be in `{fmt}` format")

    reader: HypergraphReader = {  # type: ignore[abstract]
        "empirical": EmpiricalHGReader,
        "synthetic": SyntheticHGReader,
        "hgf": HGFReader,
        "xgi": XGIReader,
    }.get(fmt.lower(), HGFReader)()

    result = run_pipeline(reader, filename)

    logger.info(json.dumps(result.to_dict(), indent=4))
