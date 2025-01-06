#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from glob import glob

def parse_args():
    parser = argparse.ArgumentParser(description="Summarize PAF files")
    parser.add_argument("input", help="Input samplesheet file")
    parser.add_argument("output", help="Output OTU table file")
    parser.add_argument("--min_confidence", type=int, help="Minimum confidence level")
    return parser.parse_args()

args = parse_args()

out_file = args.output
min_conf = args.min_confidence

# Use dictionary to store data
# Key: target (identification)
# Value: list of mapping quality scores from reads matching that target
db_dict = dict()
sample_list = list()

with open(args.input, 'r') as f:
    for line in f:
        sample_name, paf = line.strip().split('\t')
        sample_list.append(sample_name)
        print(f"Processing sample: {sample_name}")

        with open(paf, 'r') as paf_file:
            for line in paf_file:
                line = line.rstrip()
                if not line:
                    continue
                info_list = line.split('\t')

                # Extract columns of interest from paf file
                target_name = info_list[5]
                map_qual = info_list[11]

                # Create dictionary entry if target seen for first time
                if target_name not in db_dict:
                    db_dict[target_name] = dict()
                    db_dict[target_name]['quals'] = [map_qual]  # Add Q-score to list
                    db_dict[target_name]['n'] = 1  # Add to total mapping count
                else:
                    db_dict[target_name]['quals'].append(map_qual)  # Add Q-score to list
                    db_dict[target_name]['n'] += 1

                if sample_name not in db_dict[target_name]:
                    db_dict[target_name][sample_name] = 1  # Add to sample count
                else:
                    db_dict[target_name][sample_name] += 1

def ave_prob(map_qual_list):
    # https://www.biostars.org/p/295932/
    if map_qual_list:
        return sum([10**(int(q) / -10) for q in map_qual_list]) / len(map_qual_list)
    else:
        return None

def prob_2_conf(prob):
    return round(100.0 - (prob * 100), 2)

# Create output file with confidence level
with open(out_file, 'w') as f:
    f.write('OTU\t{}\tTotalCount\tMappingConfidence\n'.format('\t'.join(sample_list)))  # File header
    for target_name, my_dict in db_dict.items():
        map_qual_list = my_dict['quals']
        n_reads = my_dict['n']

        # Compute confidence
        prob = ave_prob(map_qual_list)
        conf = prob_2_conf(prob)

        # Get sample values for that specific target
        count_list = list()
        for sample_name in sample_list:
            if sample_name in my_dict:
                count_list.append(my_dict[sample_name])
            else:
                count_list.append(0)

        # Write ID and conf value to file
        if int(conf) >= min_conf:
            f.write('{}\t{}\t{}\t{}%\n'.format(target_name, '\t'.join([str(x) for x in count_list]), n_reads, conf))
            print(f"Written target: {target_name}, Confidence: {conf}")

print(f"Output written to {out_file}")