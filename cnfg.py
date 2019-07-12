import configparser
import csv
import os

def get_form_format(file='./format.csv'):
	with open('./format.csv', newline='') as csvfile:
		row = list(csv.reader(csvfile, delimiter = ','))

		globals()['form_labels'] = row[0]
		globals()['form_shape'] = [int(i) for i in row[1]]
		globals()['field_join'] = row[2]
		globals()['number_offset'] = [int(i) for i in row[3]]

def load_config(file_ini='./settings.ini'):
	config = configparser.SafeConfigParser()

	if os.path.isfile(file_ini):
		config.read(file_ini)
		
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
	get_form_format()
	load_config()

load_settings()

# MIN_RATIO_REGION = 0.5
# MAX_RATIO_REGION = 0.99
# PADDING_REGION = -7
# REPL_PAD_REGION = False

# MIN_RATIO_SECTION = 0.1
# MAX_RATIO_SECTION = 0.9
# PADDING_SECTION = -9
# REPL_PAD_SECTION = False
# TOLERANCE_SECTION = 10

# MIN_RATIO_FIELD = 0.01
# MAX_RATIO_FIELD = 0.1
# PADDING_FIELD = -9
# REPL_PAD_FIELD = False
# TOLERANCE_FIELD = 10

# MIN_RATIO_CHARACTER = 0.0
# MAX_RATIO_CHARACTER = 0.9
# PADDING_CHARACTER = 0
# REPL_PAD_CHARACTER = False
# TOLERANCE_CHARACTER = 100

# FORM_LABEL = ['S','S','S','F','D','N']
# FORM_SHAPE = [1,1,1,2,3,1]
# FIELD_JOIN = ['','','','.','-','']

# SHOW_DETECTED_CONTOURS = False
# SHOW_PREPROCESSING = False
# SHOW_REGION = True
# SHOW_SECTION = False
# SHOW_FIELD = False
# SHOW_CHARACTER = False