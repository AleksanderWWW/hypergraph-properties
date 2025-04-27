from pathlib import Path

import dominate  # type: ignore[import-untyped]
import dominate.tags as tags  # type: ignore[import-untyped]
import pandas as pd
from dominate.util import raw  # type: ignore[import-untyped]
from pandas.io.formats.style import Styler

from hypergraph_properties.hg_model import Hypergraph
from hypergraph_properties.reporting.result_set import PearsonNodeCorrResultSet
from scipy.stats._stats_py import SignificanceResult as SpearmanRResult


def generate_html_report(
    filepath: str,
    hg: Hypergraph,
    fmt: str,
    p_cor: PearsonNodeCorrResultSet,
    s_cor: SpearmanRResult,
) -> Path:
    title = f"Report for {hg.name}"

    save_path = f"{hg.name}.html"

    hg_meta_table = _create_metadata_table(hg, filepath, fmt)

    p_cor_table = _create_cor_table(p_cor)

    # s_cor_table = _create_cor_table(s_cor)

    with dominate.document(title=title) as doc:
        tags.h1(title)

        tags.h2("Basic info")
        tags.p("The following table provides metadata for the hypergraph")
        raw(add_styles(hg_meta_table).to_html())

        tags.h2("Pearson corelation coefficients")
        tags.p("The following table provides results for Pearson NodeCor")
        raw(add_styles(p_cor_table).to_html())

        # tags.h2("Spearman corelation coefficients")
        # tags.p("The following table provides results for Spearman NodeCor")
        # raw(add_styles(s_cor_table).to_html())

    with open(save_path, "w") as fp:
        fp.write(doc.render())

    return Path(save_path)


def _create_metadata_table(hg: Hypergraph, filepath: str, fmt: str) -> pd.DataFrame:
    return pd.DataFrame(
        data={"info": [hg.name, filepath, fmt, *hg.matrix.shape]},
        index=["name", "source", "format", "# vertices", "# hyperedges"],
    )


def _create_cor_table(cor: PearsonNodeCorrResultSet) -> pd.DataFrame:
    return pd.DataFrame(
        data={
            "avg_he_size": [
                f"{cor.no_log.statistic:.4f} (p_value={cor.no_log.pvalue:.4f}",
                f"{cor.log_degree.statistic:.4f} (p_value={cor.log_degree.pvalue:.4f}",
            ],
            "log(avg_he_size + 1)": [
                f"{cor.log_he_size.statistic:.4f} (p_value={cor.log_he_size.pvalue:.4f}",
                f"{cor.both_log.statistic:.4f} (p_value={cor.both_log.pvalue:.4f}",
            ],
        },
        index=["degree", "log(degree + 1)"],
    )


def add_styles(table: pd.DataFrame) -> Styler:
    return table.style.set_table_styles(
        [
            # Set table-wide styles
            {
                "selector": "table",
                "props": [
                    ("border-collapse", "collapse"),
                    ("margin", "20px auto"),
                    ("font-family", "'Segoe UI', Roboto, sans-serif"),
                    ("font-size", "14px"),
                    ("width", "80%"),
                    ("box-shadow", "0 2px 10px rgba(0,0,0,0.05)"),
                    ("border", "1px solid #ddd"),
                ],
            },
            # Header styles
            {
                "selector": "th",
                "props": [
                    ("background-color", "#f7f9fc"),
                    ("color", "#333"),
                    ("text-align", "center"),
                    ("padding", "10px"),
                    ("border-bottom", "2px solid #ccc"),
                ],
            },
            # Cell styles
            {
                "selector": "td",
                "props": [
                    ("text-align", "center"),
                    ("padding", "10px"),
                    ("border-bottom", "1px solid #eee"),
                ],
            },
            # Caption styling
            {
                "selector": "caption",
                "props": [
                    ("caption-side", "top"),
                    ("font-size", "16px"),
                    ("font-weight", "bold"),
                    ("margin-bottom", "10px"),
                ],
            },
        ]
    )
