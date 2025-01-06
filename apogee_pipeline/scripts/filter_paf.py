#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

def filterPAF(fileRoute, output, blockLimit=350):
    """
    Takes an input PAF and prints to stdout a filtered PAF with unique hits. 
    Hits with the largest block length will be kept. Also, it will remove any
    hit with a block length < blockLimit.

    Parameters
    ----------
    fileRoute : str
        Path to input PAF file.
    output: str
        Output file
    blockLimit : int, optional
        Hits with a block length alignment lower than this parameter will be removed.
        The default is 350.

    Returns
    -------
    None

    """
    hits = {}  # to temporarily store the hits
    with open(fileRoute) as file:
        # Filter the PAF file and store the output in hits
        for line in file:
            line = line.strip()
            fields = line.split("\t")
            seq = fields[0]
            blockLength = int(fields[10])

            if blockLength >= blockLimit:
                if seq not in hits:
                    hits[seq] = (blockLength, line)
                elif hits[seq][0] < blockLength:
                    hits[seq] = (blockLength, line)
    hits_ = [hit[1] for hit in hits.values()]
    Path(output).write_text("\n".join(hits_))

if __name__ == "__main__":
    filterPAF(snakemake.input[0], snakemake.output[0], blockLimit=snakemake.config["filter_paf_block_limit"])
