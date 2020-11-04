#!/usr/bin/python3
"""
This is a python program which, given a csv file - builds a sample matrix
"""
import argparse
import pandas as pd
import numpy as np

def setup_args():
    parser = argparse.ArgumentParser(description='Create a sample/snp matrix from a CSV file')
    parser.add_argument("-i", "--input", help="Input CSV file", required=True)
    parser.add_argument("-o", "--output", help="Output Matrix (CSV) file", required=True)
    return parser.parse_args()


def build_matrix(csv_file):

    df = pd.read_csv(csv_file)
    samples = df['ASM_ID'].drop_duplicates()
    key_cols = ['begin', 'end', 'varType', 'chromosome', 'symbol', 'impact', 'proteinAcc']
    cols = np.append(key_cols, samples)
    matrix = pd.DataFrame(columns=cols)
    no_refs = df.loc[df["varType"] != "ref", key_cols]
    row_keys = no_refs.drop_duplicates()
    for index, row in row_keys.iterrows():
        b = row["begin"]
        e = row["end"]
        t = row["varType"]
        c = row["chromosome"]
        g = row["symbol"]
        i = row["impact"]
        p = row["proteinAcc"]
        data = [ b, e, t, c, g, i, p ]
        for s in samples:
            at_position = df[(df["begin"] == b) & (df["end"] == e) & (df["varType"] == t) & (df["ASM_ID"] == s)
                             & (df["chromosome"] == c) & (df["symbol"] == g) & (df["impact"] == i) & (df["proteinAcc"] == p)]
            if len(at_position) == 2:
                data.append("11")
            elif len(at_position) == 1:
                data.append("01")
            elif len(at_position) == 0:
                data.append("00")
            else:
                assert False, "Unhandled number of mutations (%d)" % len(at_position)

        matrix.loc[index] = data

    return(matrix)


# Gather our code in a main() function
def main():
    args = setup_args()
    m = build_matrix(args.input)
    m.sort_values(['chromosome', 'begin']).to_csv(args.output, index=False)


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()
