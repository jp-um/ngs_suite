-- terminate all user activity
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'dna'
  AND pid <> pg_backend_pid();

DROP DATABASE IF EXISTS dna;
CREATE DATABASE dna;

-- connect to the (newly created) db
\c dna;

CREATE TABLE snp (
    chrom       char(5) NOT NULL,
    pos         integer NOT NULL,
    ref         varchar(10) NOT NULL,
    alt1        varchar(10) NOT NULL,
    alt2        varchar(10),
    genotype    varchar(5),
    sample      varchar(5) NOT NULL
);

