#!/usr/bin/env python

## Creates a variant matrix.  Inputs to this program are a set of masterVarBeta
## files.

import argparse
from os.path import basename

class VariantFile:
    
    def __init__(self, fname, varType='snp'):
        self.fname_handle = open(fname)
        self.varType = varType.lower()

        
    def get_next(self):
        for l in self.fname_handle:
            l = l.strip().lower()
            if l and not l.startswith("#") and not l.startswith(">"):
                entries = l.split('\t')
                if entries[6] == self.varType:
                    # start, end, chromo, zygosity, varType, ref, allele1, allele2, allele1XRef, allele2XRef, allele1Gene, allele2Gene
                    yield (int(entries[3]), int(entries[4]), entries[2], entries[5], entries[6], entries[7], entries[8], entries[9], entries[18], entries[19], entries[29], entries[30])
                    
    
    def __del__(self):
        if not self.fname_handle.closed:
            self.fname_handle.close()
                
def process_var_files(master_var_files):
    var_files = []
    for master_var_file in master_var_files:
        var_file = VariantFile(master_var_file)
        for (start, end, chromo, zygosity, varType, ref, allele1, allele2, allele1XRef, allele2XRef, allele1Gene, allele2Gene) in var_file.get_next():
            print start, end, chromo, zygosity, varType, ref, allele1, allele2, allele1XRef, allele2XRef, allele1Gene, allele2Gene, basename(master_var_file)
                   
def main():
    # set the parser
    parser = argparse.ArgumentParser(description='Creates a variant matrix from a number of samples files.')
    parser.add_argument('master_var_files', metavar='master_var_files', nargs='+', help='list of master variant files')
    args = parser.parse_args()
    process_var_files(args.master_var_files)
    
if __name__ == "__main__":
    main()


