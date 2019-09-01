import configparser
import csv
import os

from modules.ai import load_model_vars
from modules.misc import fix_path


def get_form_dict():
    file = form_dict

    with open(file, newline='') as csvfile:
        row = list(csv.reader(csvfile, delimiter=','))

        # pop column names row
        col_names = row.pop(0)
        # remove index cell
        col_names.pop(0)

        # transpose remaining cells
        lst = [list(i) for i in zip(*row)]
        # pop idx column
        idx = lst.pop(0)

        # create a dict
        dct = {}
        for i in range(len(col_names)):
            dct[str(col_names[i])] = {}
            for j in range(len(idx)):
                if lst[i][j] == '':
                    dct[str(col_names[i])][str(idx[j])] = None
                else:
                    dct[str(col_names[i])][str(idx[j])] = lst[i][j]

        globals()['form_dict'] = dct


def get_form_format():
    file = form_format

    try:
        with open(file, newline='') as csvfile:
            row = list(csv.reader(csvfile, delimiter=','))

            globals()['form_labels'] = row[0]
            globals()['form_shape'] = [int(i) for i in row[1]]
            globals()['field_join'] = row[2]
            globals()['number_offset'] = [int(i) for i in row[3]]

            if len(set(map(len, row))) != 1:
                globals()['file_error'] = file, 'has missing or incorrect values'

    except:
        globals()['file_error'] = file, 'not found'


def get_form_keys():
    file = form_keys

    column_names = []
    item_numbers = []

    try:
        with open(file, newline='') as csvfile:
            lst = list(csv.reader(csvfile, delimiter=','))

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
                        # column_names.append([section_label + str(i + 1), section[i]])
                        column_names.append(section[i])
                        item_numbers.append(section_label+str(i+1))

            globals()['column_names'] = column_names
            globals()['item_numbers'] = item_numbers

    except:
        globals()['file_error'] = file, 'not found'


def load_config(file_ini='settings.ini'):
    config = configparser.ConfigParser()

    if os.path.isfile(file_ini):
        try:
            globals()['file_error'] = None

            config.read(file_ini)

            sect = 'MODEL'
            globals()['num_models'] = config.getint(sect, 'num_models')

            sect = 'FILE'
            form_dict = fix_path(config.get(sect, 'form_dict'))
            globals()['form_dict'] = os.path.join('', *form_dict)

            form_format = fix_path(config.get(sect, 'form_format'))
            globals()['form_format'] = os.path.join('', *form_format)

            form_keys = fix_path(config.get(sect, 'form_keys'))
            globals()['form_keys'] = os.path.join('', *form_keys)

            sect = 'OUTPUT'
            globals()['translate_data'] = config.getboolean(sect, 'translate_data')

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
            globals()['show_error'] = config.getboolean(sect, 'show_error')
        except:
            globals()['file_error'] = file_ini, 'has missing or incorrect values'

    else:
        globals()['file_error'] = file_ini, 'not found'


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

    if file_error == None:
        get_form_dict()
        get_form_format()
        get_form_keys()


load_settings()
mean_px, std_px = load_model_vars()
