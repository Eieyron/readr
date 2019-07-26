import argparse
import os
import sys

from modules.config import mean_px
from modules.config import std_px

from modules.extract import process_batch

from modules.model import models

from modules.write import read_values 
from modules.write import map_values 
from modules.write import write_rows


def main():
	parser = argparse.ArgumentParser()

	parser.add_argument('--csv_file',
						type=str,
						default='',
						help='csv file to append read data; will be created if not found'
						)

	parser.add_argument('--img_dir', 
						type=str, 
						default='', 
						help='directory of document image files to be read; must contain only document images of jpg or png formats only'
						)
	
	args = parser.parse_args()
	process(args)


def process(args):
	# check if args are invalid
	if not args.csv_file.endswith('.csv'):
		sys.stdout.write('Invalid csv_file argument. Must be a .csv file.')

	elif not os.path.isdir(args.img_dir):
		sys.stdout.write('Invalid img_dir argument. Must be an existing directory')
	
	else:	
		sys.stdout.write('1/5 Successfully loaded img_dir: {} \n'.format(args.img_dir))
		sys.stdout.write('2/5 Successfully loaded csv_file: {} \n'.format(args.csv_file))

		# process image
		batch = process_batch(args.img_dir)
		sys.stdout.write('3/5 Extracted fields from {} image files\n'.format(len(batch)))

		data = []
		for paper in batch:
			# read and map fields
			values = read_values(paper)
			row = map_values(paper)
			data.append(row)

		sys.stdout.write('4/5 Extracted values from fields\n')

		# write to file
		# place in a list since write_rows accepts list
		ret = write_rows(args.csv_file, data)
		sys.stdout.write('5/5 {}\n'.format(ret))


if __name__ == '__main__':
	main()


