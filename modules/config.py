import configparser
import csv
import os

import numpy as np

from modules.ai import load_model_vars
from modules.misc import fix_path

def get_form_format():
	file = form_format
	with open(file, newline='') as csvfile:
		row = list(csv.reader(csvfile, delimiter = ','))

		globals()['form_labels'] = row[0]
		globals()['form_shape'] = [int(i) for i in row[1]]
		globals()['field_join'] = row[2]
		globals()['number_offset'] = [int(i) for i in row[3]]

def get_form_keys():

	column_names = []
	headers = []
	
	file = form_keys
	
	with open(file, newline='') as csvfile:
		lst = list(csv.reader(csvfile, delimiter = ','))

		# transpose list
		lst = [list(i) for i in zip(*lst)]

		# map item numbers to column names
		for section in lst:

			# pop the section label
			section_label = section.pop(0)
			
			for i in range(len(section)):
				
				# filter out empty cells/fields
				if section[i] != '':

					# dct[section_label+str(i+1)] = section[i]
					# 'A1', Meaning of life
					column_names.append([section_label+str(i+1), section[i]])

		
		globals()['column_names'] = column_names

def load_config(file_ini='./settings.ini'):
	config = configparser.SafeConfigParser()

	if os.path.isfile(file_ini):
		config.read(file_ini)

		sect = 'MODEL'
		globals()['num_models'] = config.getint(sect, 'num_models')

		sect = 'FILE'

		form_format = fix_path(config.get(sect, 'form_format'))
		globals()['form_format'] = os.path.join('', *form_format)


		form_keys = fix_path(config.get(sect, 'form_keys'))
		globals()['form_keys'] = os.path.join('', *form_keys)

		sect = 'ORIENTATION'
		globals()['is_landscape'] = config.getboolean(sect, 'is_landscape')

		sect = 'REGION'
		globals()['min_ratio_region'] = config.getfloat(sect, 'min_ratio')
		globals()['max_ratio_region'] = config.getfloat(sect, 'max_ratio')
		globals()['padding_region'] = config.getint(sect, 'padding')
		globals()['repl_pad_region'] = config.getboolean(sect, 'replace_pad')

		sect = 'SECTION'
		globals()['min_ratio_section'] = config.getfloat(sect, 'min_ratio')
		globals()['max_ratio_section'] = config.getfloat(sect, 'max_ratio')
		globals()['padding_section'] = config.getint(sect, 'padding')
		globals()['repl_pad_section'] = config.getboolean(sect, 'replace_pad')
		globals()['tolerance_section'] = config.getint(sect, 'tolerance_factor')

		sect = 'FIELD'
		globals()['min_ratio_field'] = config.getfloat(sect, 'min_ratio')
		globals()['max_ratio_field'] = config.getfloat(sect, 'max_ratio')
		globals()['padding_field'] = config.getint(sect, 'padding')
		globals()['repl_pad_field'] = config.getboolean(sect, 'replace_pad')
		globals()['tolerance_field'] = config.getint(sect, 'tolerance_factor')

		sect = 'CHARACTER'
		globals()['min_ratio_character'] = config.getfloat(sect, 'min_ratio')
		globals()['max_ratio_character'] = config.getfloat(sect, 'max_ratio')
		globals()['padding_character'] = config.getint(sect, 'padding')
		globals()['repl_pad_character'] = config.getboolean(sect, 'replace_pad')
		globals()['tolerance_character'] = config.getint(sect, 'tolerance_factor')

		sect = 'DEBUG'
		globals()['show_contours'] = config.getboolean(sect, 'show_contours')
		globals()['show_preprocessing'] = config.getboolean(sect, 'show_preprocessing')
		globals()['show_region'] = config.getboolean(sect, 'show_region')
		globals()['show_section'] = config.getboolean(sect, 'show_section')
		globals()['show_field'] = config.getboolean(sect, 'show_field')
		globals()['show_character'] = config.getboolean(sect, 'show_character')

	else:
		load_defaults()

def load_defaults():
		globals()['is_landscape'] = True

		globals()['min_ratio_region'] = 0.5
		globals()['max_ratio_region'] = 0.99
		globals()['padding_region'] = -7
		globals()['repl_pad_region'] = False

		globals()['min_ratio_section'] = 0.1
		globals()['max_ratio_section'] = 0.9
		globals()['padding_section'] = -9
		globals()['repl_pad_section'] = False
		globals()['tolerance_section'] = 10

		globals()['min_ratio_field'] = 0.01
		globals()['max_ratio_field'] = 0.1
		globals()['padding_field'] = -9
		globals()['repl_pad_field'] = False
		globals()['tolerance_field'] = 10

		globals()['min_ratio_character'] = 0.0
		globals()['max_ratio_character'] = 0.9
		globals()['padding_character'] = 0
		globals()['repl_pad_character'] = False
		globals()['tolerance_character'] = 100

		globals()['show_contours'] = False
		globals()['show_preprocessing'] = False
		globals()['show_region'] = False
		globals()['show_section'] = False
		globals()['show_field'] = False
		globals()['show_character'] = False

def load_settings():
	load_config()
	get_form_format()
	get_form_keys()

load_settings()
mean_px, std_px = load_model_vars()