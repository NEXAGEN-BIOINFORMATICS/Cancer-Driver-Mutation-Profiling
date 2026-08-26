from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def load_mutation_data(input_file):
    """Load mutation data from a CSV file."""
    return pd.read_csv(input_file)


def get_gene_column(data):
    """Find the column containing gene names."""
    if "Hugo_Symbol" in data.columns:
        return "Hugo_Symbol"
    if "gene" in data.columns:
        return "gene"

    raise ValueError(
        "Gene column not found. Expected 'Hugo_Symbol' or 'gene'."
    )


def count_mutations_by_gene(data):
    """Count mutations for each gene."""
    gene_column = get_gene_column(data)
    return data[gene_column].value_counts()


def plot_mutations_by_gene(gene_counts, output_file):
    """Create a bar chart showing the most frequently mutated genes."""
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))
    gene_counts.head(10).plot(kind="bar")

    plt.title("Top 10 Mutated Genes")
    plt.xlabel("Gene")
    plt.ylabel("Number of Mutations")
    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def get_mutation_type_column(data):
    """Find the column containing mutation classifications."""
    possible_columns = [
        "Variant_Classification",
        "mutation_type",
        "Mutation_Type",
        "Consequence",
    ]

    for column in possible_columns:
        if column in data.columns:
            return column

    return None


def count_mutation_types(data):
    """Count mutations by mutation type."""
    mutation_column = get_mutation_type_column(data)

    if mutation_column is None:
        raise ValueError(
            "Mutation type column not found."
        )

    return data[mutation_column].value_counts()


def plot_mutation_distribution(mutation_counts, output_file):
    """Create a bar chart showing mutation type distribution."""
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))
    mutation_counts.plot(kind="bar")

    plt.title("Mutation Type Distribution")
    plt.xlabel("Mutation Type")
    plt.ylabel("Number of Mutations")
    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def create_mutation_summary(data, output_file):
    """Create and save a summary table of mutations by gene."""
    gene_column = get_gene_column(data)

    summary = (
        data[gene_column]
        .value_counts()
        .rename_axis("Gene")
        .reset_index(name="Mutation_Count")
    )

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(output_path, index=False)

    return summary
