import pysam
import numpy as np
from pysam import AlignmentFile
from Bio import SeqIO
import positions_generator
import argparse
import file_handler
import sys

d_output_filename = "output_phylo_M.txt"
d_r_positions = 10

def fetch_alignments(sam_file, ref_id):
    sam_file_reader = AlignmentFile(sam_file, "r")
    alignments = [al for al in sam_file_reader.fetch() 
                  if sam_file_reader.get_reference_name(al.reference_id) == ref_id]

    sam_file_reader.close()
    return alignments

def get_mutation_value(alignment, position, ref_seq_at_pos):
    reference_positions = alignment.get_reference_positions()
   
    if position not in reference_positions:
        val = 2
    else:
        read_value_at_pos = alignment.query_alignment_sequence[reference_positions.index(position)]
        if read_value_at_pos == ref_seq_at_pos:
            val = 0
        else:
            val = 1
    return val

def build_phylogenetic_matrix(fasta_sequence, alignments, positions): 
    if len(fasta_sequence) == 0:
        raise Exception("No reference genome sequence provided.")   
    if len(alignments) == 0:
        raise Exception("No alignments provided.")
    if len(positions) == 0:
        raise Exception("No positions on the genome provided.")
    
    try:
        M = [[get_mutation_value(alignment, position, fasta_sequence[position]) for position in positions]
                for alignment in alignments]
    except IndexError:
        raise Exception("The positions provided must be within the range of the reference genome.")

    return M

def main():
    parser = argparse.ArgumentParser(description='Build an input matrix M for pyhlogenesis.')
    parser.add_argument('-s', type=str, required=True, help='Name of the SAM file.')
    parser.add_argument('-f', type=str, required=True, help='Name of the FASTA file.')
    parser.add_argument('--p', type=str, help='Name of the CSV or JSON file containing the positions on the genome (optional, the default option is to generate randomly).')
    parser.add_argument('--n', type=int, default=d_r_positions, help='Number of positions to generate when not specifying any positions file (default is 10).')
    parser.add_argument('--o', type=str, default=d_output_filename, help='Name of the output file containing the input matrix for pyhlogenesis.')

    args = parser.parse_args()

    try:
        fasta_genome = SeqIO.read(args.f, 'fasta')
        alignments = fetch_alignments(args.s, fasta_genome.name)

        fasta_sequence = fasta_genome.seq

        if args.p is not None:
            if args.p.endswith('.csv'):
                positions = file_handler.read_from_csv(args.p)
            elif args.p.endswith('.json'):
                positions = file_handler.read_from_json(args.p)
            else:
                raise Exception("Invalid file format. The integers file must be either CSV or JSON.")
        else:
            positions = positions_generator.generate_integers(0, len(fasta_sequence), args.n)

        M = build_phylogenetic_matrix(fasta_sequence, alignments, positions)
        file_handler.write_on_file(d_output_filename, M)

    except Exception as e:
        print("Error: ", str(e), file=sys.stderr) 

if __name__ == '__main__':
    main()