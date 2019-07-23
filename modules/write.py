import csv

import modules.config as config

from modules.ai import read_character

from modules.config import mean_px
from modules.config import std_px

from modules.model import models

def read_values(paper):
	for i in range(len(paper)):
		section = paper[i]
		
		for j in range(len(section)):
			field = section[j]
			
			for k in range(len(field)):
				character = field[k]

				# read characters
				field[k] = str(read_character(models, character)[2])
			
			# merge into a single string
			section[j] = ''.join(field)
		
		# merge multiple non-empty fields
		paper[i] = [config.field_join[i].join(filter(None, section[x:x+config.form_shape[i]])) for x in range(0, len(section), config.form_shape[i])]

	return paper

def map_values(paper, show=False):
	# map fields to number, store in num_field
	num_field = {}
	for i in range(len(paper)):
		section = paper[i]

		k = config.number_offset[i]
		for j in range(len(section)):
			field = section[j]

			item_number = config.form_labels[i] + str(k)
			num_field[item_number] = field

			k = k + 1

	# map numbered fields to column names
	row = {}
	for key in config.column_names:
		row[config.column_names[key]]=num_field[key]

	if (show == True):
		for key, val in row.items():
			print(key+": "+val)

	return row

def write_rows(file_csv, data):
	with open(file_csv, 'a') as csvfile:
		fields = config.column_names.values()
		writer = csv.DictWriter(csvfile, fieldnames=fields)
		writer.writeheader()
		writer.writerows(data)
