import configparser
import json
import os

from modules.ai import load_model_vars
from modules.misc import fix_path


# load form attributes
def load_form_attr():
    # file_form is defined in load_config
    json_form = file_form

    try:
        with open(json_form) as form:
            form = json.load(form)

            # get number of entries per paper
            globals()['entries'] = int(form['format']['entries'])

            # get form format, section stats
            section = form['format']['section']['list']

            form_labels = [section[i]['label'] for i in range(len(section))]
            globals()['form_labels'] = form_labels

            globals()['form_shape'] = list([int(section[i]['fields_per_row']) for i in range(len(section))])
            globals()['field_join'] = list([section[i]['separator'] for i in range(len(section))])
            globals()['number_offset'] = [section[i]['first_number_offset'] for i in range(len(section))]

            globals()['length'] = [section[i]['length'] for i in range(len(section))]
            globals()['total_length'] = sum(length)

            # form_labels defined earlier
            unique_labels = list(dict.fromkeys(form_labels))
            keys = form['keys']
            column_names = []
            item_numbers = []
            for i in unique_labels:
                column_names.extend(keys[i])

            # title/attribute asked/column name
            globals()['column_names'] = column_names

            # A1, A2, A3..
            item_numbers = []
            for s in section:
                start = s['first_number_offset']
                stop = start + s['length']
                item_numbers.extend([s['label'] + str(i) for i in range(start, stop)])

            globals()['item_numbers'] = item_numbers

            # settings
            settings = form['settings']
            # orientation
            orientation = settings['orientation']
            globals()['is_landscape'] = orientation['is_landscape'] == "True"

            # region
            region = settings['region']
            globals()['min_ratio_region'] = float(region['min_ratio'])
            globals()['max_ratio_region'] = float(region['max_ratio'])
            globals()['padding_region'] = int(region['padding'])
            globals()['repl_pad_region'] = region['replace_pad'] == "True"

            # section
            section = settings['section']
            globals()['min_ratio_section'] = float(section['min_ratio'])
            globals()['max_ratio_section'] = float(section['max_ratio'])
            globals()['padding_section'] = int(section['padding'])
            globals()['repl_pad_section'] = section['replace_pad'] == "True"
            globals()['tolerance_section'] = float(section['tolerance_factor'])

            # field
            field = settings['field']
            globals()['min_ratio_field'] = float(field['min_ratio'])
            globals()['max_ratio_field'] = float(field['max_ratio'])
            globals()['padding_field'] = int(field['padding'])
            globals()['repl_pad_field'] = field['replace_pad'] == "True"
            globals()['tolerance_field'] = float(field['tolerance_factor'])

            # character
            character = settings['character']
            globals()['min_ratio_character'] = float(character['min_ratio'])
            globals()['max_ratio_character'] = float(character['max_ratio'])
            globals()['padding_character'] = int(character['padding'])
            globals()['repl_pad_character'] = character['replace_pad'] == "True"
            globals()['tolerance_character'] = float(character['tolerance_factor'])

    except:
        globals()['file_error'] = file_form, 'not found or incorrect'


# load config file
def load_config(file_ini='settings.ini'):
    config = configparser.ConfigParser()

    if os.path.isfile(file_ini):
        try:
            globals()['file_error'] = None

            config.read(file_ini)

            sect = 'MODEL'
            globals()['num_models'] = config.getint(sect, 'num_models')

            sect = 'FILE'
            file_form = fix_path(config.get(sect, 'form'))
            globals()['file_form'] = os.path.join('', *file_form)

            sect = 'DEBUG'
            globals()['show_contours'] = config.getboolean(sect, 'show_contours')
            globals()['show_preprocessing'] = config.getboolean(sect, 'show_preprocessing')
            globals()['show_region'] = config.getboolean(sect, 'show_region')
            globals()['show_section'] = config.getboolean(sect, 'show_section')
            globals()['show_field'] = config.getboolean(sect, 'show_field')
            globals()['show_character'] = config.getboolean(sect, 'show_character')
            globals()['show_error'] = config.getboolean(sect, 'show_error')

        except:
            globals()['file_error'] = file_ini, 'has missing or incorrect values'

    else:
        globals()['file_error'] = file_ini, 'not found'


# load all files
# num_models, file_error defined in load_config
def load_settings():
    load_config()

    dir_models = './models/'
    # if models/ folder does not exist:
    if not os.path.isdir(dir_models):
        globals()['file_error'] = dir_models, 'not found'
    # if models/ is empty
    elif os.listdir(dir_models)[0:num_models] == []:
        globals()['file_error'] = dir_models, 'is empty'
    # if models/ has no valid .h5 py
    elif [file for file in os.listdir('./models') if file.endswith('.h5')][0:num_models] == []:
        globals()['file_error'] = dir_models, 'has no valid .h5 file'

    # if there's no error in loading config files
    if file_error == None:
        load_form_attr()


load_settings()
mean_px, std_px = load_model_vars()

# some deprecated globals
globals()['translate_data'] = False
