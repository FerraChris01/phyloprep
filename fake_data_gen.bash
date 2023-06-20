#!/bin/bash

fasta_name="ref"
fasta_seq_length=100
reads_length=95
sam_name="alignments"

while getopts ":fn:fl:rl:sn:" opt; do
  case $opt in
    fn)
      fasta_name=$OPTARG
      ;;
    fl)
      fasta_seq_length=$OPTARG
      ;;
    rl)
      reads_length=$OPTARG
      ;;
    sn)
      sam_name=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      ;;
  esac
done

python3 ~/fastq_generator/fastq_generator.py generate_fasta "$fasta_name" "$fasta_seq_length" > "$fasta_name.fa"

art_illumina -ss MSv3 -i "$fasta_name.fa" -p -l "$reads_length" -f 10 -m 200 -s 10 -o output

bwa index "$fasta_name.fa"

bwa mem "$fasta_name.fa" output1.fq output2.fq > "$sam_name.sam"

umask 0000

rm *.amb *.ann *.bwt *.pac *.sa *.aln *.fq
