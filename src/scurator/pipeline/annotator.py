import argparse
import pandas as pd
from pathlib import Path

DRIVER_GENES = {
    "TP53",
    "KRAS",
    "EGFR",
    "BRCA1",
    "BRCA2",
}

def filter_driver_genes(data):
    if "Hugo_Symbol" in data.columns:
        gene_column = "Hugo_Symbol"
    elif "gene" in data.columns:
        gene_column = "gene"
    else:
        raise ValueError(
            "Gene column not found. Expected 'Hugo_Symbol' or 'gene'."
        )

    filtered_data = data[data[gene_column].isin(DRIVER_GENES)].copy()
    return filtered_data


def save_results(data, output_file):
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(output_path, index=False)

def main():
    parser = argparse.ArgumentParser(
        description="Filter mutation data for known cancer driver genes."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to the input mutation CSV file."
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Path to save the filtered CSV file."
    )

    args = parser.parse_args()

    print(f"Loading mutation data from: {args.input}")
    data = pd.read_csv(args.input)

    print(f"Loaded {len(data)} mutations.")

    filtered_data = filter_driver_genes(data)

    print(
        f"Found {len(filtered_data)} mutations "
        f"in known driver genes."
    )

    save_results(filtered_data, args.output)

    print(f"Results saved to: {args.output}")


if __name__ == "__main__":
    main()
