import pandas as pd

from src.scurator.visualization.plots import (
    count_mutations_by_gene,
    count_mutation_types,
    create_mutation_summary,
    get_gene_column,
    get_mutation_type_column,
)


EXPECTED_TP53_COUNT = 2
EXPECTED_KRAS_COUNT = 1
EXPECTED_MISSENSE_COUNT = 2


def test_get_gene_column_with_gene():
    data = pd.DataFrame(
        {
            "gene": ["TP53", "KRAS"],
        }
    )

    assert get_gene_column(data) == "gene"


def test_get_gene_column_with_hugo_symbol():
    data = pd.DataFrame(
        {
            "Hugo_Symbol": ["TP53", "BRCA1"],
        }
    )

    assert get_gene_column(data) == "Hugo_Symbol"


def test_count_mutations_by_gene():
    data = pd.DataFrame(
        {
            "gene": ["TP53", "TP53", "KRAS"],
        }
    )

    result = count_mutations_by_gene(data)

    assert result["TP53"] == EXPECTED_TP53_COUNT
    assert result["KRAS"] == EXPECTED_KRAS_COUNT


def test_get_mutation_type_column():
    data = pd.DataFrame(
        {
            "Variant_Classification": [
                "Missense_Mutation",
                "Frame_Shift_Del",
            ]
        }
    )

    assert get_mutation_type_column(data) == "Variant_Classification"


def test_count_mutation_types():
    data = pd.DataFrame(
        {
            "Variant_Classification": [
                "Missense_Mutation",
                "Missense_Mutation",
                "Frame_Shift_Del",
            ]
        }
    )

    result = count_mutation_types(data)

    assert result["Missense_Mutation"] == EXPECTED_MISSENSE_COUNT
    assert result["Frame_Shift_Del"] == 1


def test_create_mutation_summary(tmp_path):
    data = pd.DataFrame(
        {
            "gene": ["TP53", "TP53", "KRAS"],
        }
    )

    output_file = tmp_path / "mutation_summary.csv"

    summary = create_mutation_summary(data, output_file)

    assert output_file.exists()
    assert list(summary.columns) == ["Gene", "Mutation_Count"]
    assert summary.iloc[0]["Gene"] == "TP53"
    assert summary.iloc[0]["Mutation_Count"] == EXPECTED_TP53_COUNT
