import click

from hypergraph_properties.hg_properties.corr import CorAlgorithm, node_corr
from hypergraph_properties.hg_reader.readers import (
    EmpiricalHGReader,
    HGFReader,
    SyntheticHGReader,
)
from hypergraph_properties.hg_reader.template import HypergraphReader
from hypergraph_properties.reporting.html import generate_html_report
from hypergraph_properties.reporting.result_set import PearsonNodeCor, SpearmanNodeCor
from hypergraph_properties.utils.logger import get_logger
from hypergraph_properties.pipeline import run_pipeline

logger = get_logger()


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option(
    "--fmt", type=click.Choice(["empirical", "synthetic", "hgf"], case_sensitive=False)
)
@click.option("--html-report", is_flag=True)
def main(filename: click.Path, fmt: str, html_report: bool) -> None:
    logger.info(f"running `hypergraph-properties` pipeline on file {filename}")
    logger.info(f"expecting hypergraph to be in `{fmt}` format")

    if not any((html_report,)):  # TODO: other saving options e.g. json, csv
        logger.warning("no saving option passed - results will not be persisted")

    reader: HypergraphReader = {  # type: ignore[abstract]
        "empirical": EmpiricalHGReader,
        "synthetic": SyntheticHGReader,
        "hgf": HGFReader,
    }.get(fmt.lower(), HGFReader)()

    result = run_pipeline(reader, filename)

    if html_report:
        saved_to = generate_html_report(
            str(filename),
            result.hg,
            fmt,
            result.p_cor,
            result.s_cor,
        )
        logger.info(f"HTML report saved at {saved_to}")
