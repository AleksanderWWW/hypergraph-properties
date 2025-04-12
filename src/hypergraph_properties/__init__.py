import click

from hypergraph_properties.hg_properties.corr import node_corr
from hypergraph_properties.hg_reader.readers import EmpiricalHGReader, SyntheticHGReader
from hypergraph_properties.hg_reader.template import HypergraphReader
from hypergraph_properties.utils.logger import get_logger

logger = get_logger()


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option(
    "--fmt", type=click.Choice(["empirical", "synthetic", "hgf"], case_sensitive=False)
)
@click.option(
    "--out", type=click.Path(writable=True), default=None, help="Output file path."
)
def main(filename: click.Path, fmt: str, out: click.Path | None) -> None:
    logger.info(f"running `hypergraph-properties` pipeline on file {filename}")
    logger.info(f"expecting hypergraph to be in `{fmt}` format")

    if out is not None:
        logger.info(f"final report will be saved to {out}")
    else:
        logger.warning("final report will not be saved")

    reader: HypergraphReader = {
        "empirical": EmpiricalHGReader,
        "synthetic": SyntheticHGReader,
    }.get(fmt, EmpiricalHGReader)()

    hg = reader.read_graph(filename)

    _ = out  # TODO: save to file

    for log_degrees in [True, False]:
        for log_avg_he_sizes in [True, False]:
            corr = node_corr(
                hg, log_degrees=log_degrees, log_avg_he_sizes=log_avg_he_sizes
            )
            expr = f"corr = node_corr(hg, log_degrees={log_degrees}, log_avg_he_sizes={log_avg_he_sizes})"
            logger.info(f"{expr} = {corr.statistic} (p={corr.pvalue})")
