#!/usr/bin/env python

## Creates a variant matrix.  Inputs to this program are a set of masterVarBeta
## files.

import argparse
from os.path import basename

import sys

# C1,C2,D1,D2,D3,D4,FM,c76140

delim = ","

def process_file(samples, var_file):
    sample_list = samples.split(',')
    header = []
    for s in sample_list:
           header = header + [ s + " allele1" , s + " allele2", s + " allele1XRef", s + " allele2XRef", s + " allele1Gene", s + " allele2Gene" ]
    print "start, end, chromo, variant type, " + ', '.join(header)
    with open(var_file) as var_file_handle:
        prev = ""
        row = {}
        for l in var_file_handle:
            (start, end, chromo, zygo, var_type, ref, allele1, allele2, allele1XRef, allele2XRef, allele1Gene, allele2Gene, sample) = l.strip().split(' ')
            row[sample] = '{}->{}{}{}->{}{}{}{}{}{}{}{}{}'.format(ref, allele1, delim, ref, allele2, delim, allele1XRef, delim, allele2XRef, delim, allele1Gene, delim, allele2Gene)
            if prev and start+end+chromo != prev:                
                if len(row):
                    r = ""
                    for s in sample_list:
                        if s in row:
                            if r:
                                r += delim + row[s]
                            else:
                                r = row[s]
                        else:
                            r += delim
                    print delim.join([ chromo, start, end, var_type, r ])
                else:
                    raise Exception("dict should contain at least one element")
                row.clear()
            prev = start+end+chromo
                


def main():
    # set the parser
    parser = argparse.ArgumentParser(description='Creates a variant matrix from a collection of variants.')
    parser.add_argument('samples', help='Comma delimited variant list')
    parser.add_argument('varfile', help='Variant File')
    args = parser.parse_args()
    process_file(args.samples, args.varfile)
    
if __name__ == "__main__":
    main()


