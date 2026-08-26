import pandas as pd

from src.scurator.pipeline.annotator import filter_driver_genes

EXPECTED_GENE_COUNT = 3
EXPECTED_HUGO_SYMBOL_COUNT = 2


def test_filter_driver_genes_with_gene_column():
    data = pd.DataFrame(
        {
            "gene": ["TP53", "KRAS", "NOT_A_DRIVER", "BRCA1"],
            "mutation": ["m1", "m2", "m3", "m4"],
        }
    )

    result = filter_driver_genes(data)

    assert len(result) == EXPECTED_GENE_COUNT
    assert set(result["gene"]) == {"TP53", "KRAS", "BRCA1"}


def test_filter_driver_genes_with_hugo_symbol_column():
    data = pd.DataFrame(
        {
            "Hugo_Symbol": ["EGFR", "BRCA2", "OTHER"],
            "mutation": ["m1", "m2", "m3"],
        }
    )

    result = filter_driver_genes(data)

    assert len(result) == EXPECTED_HUGO_SYMBOL_COUNT
    assert set(result["Hugo_Symbol"]) == {"EGFR", "BRCA2"}
