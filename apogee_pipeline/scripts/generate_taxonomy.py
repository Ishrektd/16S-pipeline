#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script creates the taxonomy table needed for loading the data into the 
phyloseq package.

The taxonomy table links every taxID to its taxonomy

@author: Adriel Latorre-Pï¿½rez
@company: Darwin Bioprospecting Excellence S.L.
@date: 19/10/2020
"""
import argparse
from pathlib import Path

def taxnomyDIC(taxonomy_file):
    taxDIC = {}
    with open(taxonomy_file) as file:
        for line in file:
            taxID, taxonomy = line.strip().split("\t")
            taxDIC[taxID] = taxonomy.replace(";", ",")
    return taxDIC

def taxID2taxonomy(otu_table, taxDIC, output):
    lines = ["#OTU ID,Domain,Phylum,Class,Order,Family,Genus,Species"]
    with open(otu_table) as file:
        for line in file:
            if line[0] == "#":
                continue
            taxID = line.strip().split("\t")[0]
            try:
                lines.append(taxID + "," + taxDIC[taxID])
            except KeyError:
                pass
    Path(output).write_text("\n".join(lines))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate taxonomy table")
    parser.add_argument("--taxonomy_file", required=True, help="Path to the taxonomy file")
    parser.add_argument("input", help="Path to the OTU table")
    parser.add_argument("output", help="Path to the output taxonomy table")
    args = parser.parse_args()

    taxDIC = taxnomyDIC(args.taxonomy_file)
    taxID2taxonomy(args.input, taxDIC, args.output)
