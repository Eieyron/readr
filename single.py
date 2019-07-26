import argparse
import sys

from modules.config import mean_px
from modules.config import std_px

from modules.extract import process_single

from modules.model import models

from modules.write import map_values
from modules.write import read_values
from modules.write import write_rows


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--csv_file',
                        type=str,
                        default='',
                        help='csv file to append read data; will be created if not found'
                        )

    parser.add_argument('--img_file',
                        type=str,
                        default='',
                        help='image file of document to be read; jpg or png formats only'
                        )

    args = parser.parse_args()
    process(args)


def process(args):
    # check if args are invalid
    if not args.csv_file.endswith('.csv'):
        sys.stdout.write('Invalid csv_file argument. Must be a .csv file.')

    elif not (args.img_file.endswith('.png') or args.img_file.endswith('.jpg')):
        sys.stdout.write('Invalid img_file argument. Must be a .png or .jpg file.')

    else:
        sys.stdout.write('1/5 Successfully loaded img_file: {} \n'.format(args.img_file))
        sys.stdout.write('2/5 Successfully loaded csv_file: {} \n'.format(args.csv_file))

        # process image
        paper = process_single(args.img_file)
        sys.stdout.write('3/5 Extracted fields\n')

        # read and map fields
        values = read_values(paper)
        row = map_values(paper)
        sys.stdout.write('4/5 Extracted values from fields\n')

        # print(config.column_names)
        # print(row)

        # write to file
        # place in a list since write_rows accepts 2d list
        data = [row]
        ret = write_rows(args.csv_file, data)
        sys.stdout.write('5/5 {}\n'.format(ret))


if __name__ == '__main__':
    main()
