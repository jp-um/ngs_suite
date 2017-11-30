#!/usr/bin/python3
"""
This is a python program which imports VCF data
in a PostgreSQL database.
"""
import argparse
import configparser
import psycopg2
import psycopg2.extras
import sys
import vcf


def setup_args():
    parser = argparse.ArgumentParser(description='Import a VCF file to a PostgreSQL database.')
    parser.add_argument("-i", "--input", help="Input VCF file", required=True)
    return parser.parse_args()


def get_db_conn(conf_file="db.conf"):
    config = configparser.ConfigParser()
    config.read(conf_file)
    return psycopg2.connect(dbname=config['db']['database'], user=config['db']['username'])


def convert_to_list(single_vcf_record):
    alt = single_vcf_record.ALT
    if len(alt) == 1:
        alt = [alt[0].sequence, None]
    elif len(alt) == 2:
        alt = sorted([a.sequence for a in alt])
    else:
        assert False, "How much stuff does ALT have? A. %s" % alt
    assert len(single_vcf_record.samples) == 1, "Should only have one sample!"
    sample = single_vcf_record.samples[0]
    return single_vcf_record.CHROM, single_vcf_record.POS, single_vcf_record.REF, alt[0], alt[1], sample.gt_nums, sample.sample


def save_to_db(vcf_records, conn, n=200):
    sql = """
      INSERT INTO snp (chrom, pos, ref, alt1, alt2, genotype, sample)
      VALUES %s
    """
    cursor = conn.cursor()
    r = [convert_to_list(x) for x in vcf_records]
    psycopg2.extras.execute_values(cursor, sql, r, page_size=1000)
    cursor.close()


def parse_vcf(vcf_file, chunk_size=50000):
    f = open(vcf_file, 'r')
    vcf_reader = vcf.Reader(f)
    vcf_records = []
    conn = get_db_conn()
    for i, vcf_rec in enumerate(vcf_reader):
        if i % chunk_size == 0 and vcf_records:
            vcf_records.append(vcf_rec)
            save_to_db(vcf_records, conn)
            vcf_records = []
            sys.stdout.write('*')
            sys.stdout.flush()
        else:
            vcf_records.append(vcf_rec)

    save_to_db(vcf_records, conn)
    conn.commit()
    conn.close()
    f.close()


# Gather our code in a main() function
def main():
    args = setup_args()
    parse_vcf(args.input)


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()
