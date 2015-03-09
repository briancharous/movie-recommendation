import argparse
import csv

def matrix_from_filename(filename):
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            rows.append(row[:-1])
    return rows

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-tr', '--training', required=False, help='Filename for training set')
    args = parser.parse_args()

    print matrix_from_filename(args.training)

if __name__ == '__main__':
    main()