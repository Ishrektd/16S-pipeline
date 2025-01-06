import polars as pl

def check_config():
    for key in ["sample_sheet", "output_folder", "mmi", "tsv"]:
        config[key] = Path(config[key]).expanduser()
    df = pl.read_csv(config["sample_sheet"])
    if df.is_empty():
        exit("Sample sheet is empty")
    Nsamples = len(df)
    for col in ["sample_id", "sample_path"]:
        if len(df.select(col).unique()) < Nsamples:
            exit(f"Column {col} must contain unique values!")
    config["samples"] = { row["sample_id"]: Path(row["sample_path"]).expanduser() for row in df.iter_rows(named=True) }

def get_pafs(wildcards):
    return { sid: f"filteredPAFs/{sid}-porechop-nanofilt.scrubb.refilt-f.paf" for sid in config["samples"].keys() }

def get_fastq(wildcards):
    return config["samples"][wildcards.sample]