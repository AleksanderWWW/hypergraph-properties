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

    reader: HypergraphReader = {
        "empirical": EmpiricalHGReader,
        "synthetic": SyntheticHGReader,
        "hgf": HGFReader,
    }.get(fmt.lower(), HGFReader)()

    hg = reader.read_graph(filename)

    cors_p = []
    cors_s = []

    for log_avg_he_sizes in [False, True]:
        for log_degrees in [False, True]:
            corr_p = node_corr(
                hg, log_degrees=log_degrees, log_avg_he_sizes=log_avg_he_sizes
            )
            corr_s = node_corr(
                hg,
                log_degrees=log_degrees,
                log_avg_he_sizes=log_avg_he_sizes,
                algorithm=CorAlgorithm.SPEARMAN,
            )

            cors_p.append(corr_p)
            cors_s.append(corr_s)

    p_cor = PearsonNodeCor(*cors_p)
    s_cor = SpearmanNodeCor(*cors_s)

    if html_report:
        saved_to = generate_html_report(str(filename), hg, fmt, p_cor, s_cor)
        logger.info(f"HTML report saved at {saved_to}")
