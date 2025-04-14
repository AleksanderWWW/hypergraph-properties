import click

from hypergraph_properties.hg_properties.corr import node_corr
from hypergraph_properties.hg_reader.readers import EmpiricalHGReader, SyntheticHGReader, HGFReader
from hypergraph_properties.hg_reader.template import HypergraphReader
from hypergraph_properties.reporting.html import generate_html_report
from hypergraph_properties.reporting.result_set import PearsonNodeCor
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
        "hgf": HGFReader
    }.get(fmt.lower(), HGFReader)()

    hg = reader.read_graph(filename)

    cors = []

    for log_avg_he_sizes in [False, True]:
        for log_degrees in [False, True]:
            corr = node_corr(
                hg, log_degrees=log_degrees, log_avg_he_sizes=log_avg_he_sizes
            )
            expr = f"node_corr(hg, log_degrees={log_degrees}, log_avg_he_sizes={log_avg_he_sizes})"
            logger.info(f"{expr} = {corr.statistic} (p={corr.pvalue})")
            cors.append(corr)

    p_cor = PearsonNodeCor(*cors)

    if html_report:
        saved_to = generate_html_report(str(filename), hg, fmt, p_cor)
        logger.info(f"HTML report saved at {saved_to}")
