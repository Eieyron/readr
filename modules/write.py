import os

import pandas as pd

from pandas import DataFrame

import modules.config as config

from modules.ai import read_character

# model needs these to run
from modules.config import mean_px
from modules.config import std_px

from modules.model import models


# params:
# paper <- structured nested list of character images from paper
def read_values(paper):
    for i in range(len(paper)):
        section = paper[i]

        for j in range(len(section)):
            field = section[j]

            for k in range(len(field)):
                character = field[k]                                    # image of the character

                # read characters
                field[k] = str(read_character(models, character)[2])    # interpreted character

            # merge into a single string, the field
            section[j] = ''.join(field)                                 # ex. "123", ""

        # merge with separators as rows
        rows = [''.join(list(sum(zip(section[x:x+config.form_shape[i]], config.field_join[i]+[0]), ())[:-1]))
                for x in range(0, len(section), config.form_shape[i])]

        # separate rows by comma
        columns = [row.split(',') for row in rows]
        paper[i] = [entry for row in columns for entry in row]

    return paper
# returns:
# paper <- same structured nested list but contains actual characters instead


# params:
# paper <- returned value of read_values
# show <- prints the mapping if True
def map_values(paper, show=True):
    # 1 entry per paper means multiple sections
    # assigns every field to corresponding items as much as possible
    # spatial and logical constraint
    if config.entries == 1:
        # map fields to number, store in num_field
        # 'A1': 42
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
        row = []
        for item_number in config.item_numbers:
            row.append(num_field.get(item_number, ""))

        if show:
            for item_number in config.item_numbers:
                print("{}: {}".format(item_number, num_field.get(item_number, "")))

        # add one dimension to fit
        rows = [row]

    # multiple entries assume only one section is used.
    # a row is an entry.
    # n number of fields will be assigned to n items m times, where n is config.length, m is config.entries.
    else:
        section = paper[0]

        # fold section list by row, as the entries
        entries = [section[i:i+config.length[0]] for i in range(0, len(section), config.length[0])]

        # loop through the entries
        rows = []
        for entry in entries:
            num_field = {}
            k = config.number_offset[0]
            for i in range(len(entry)):
                field = entry[i]

                item_number = config.form_labels[0] + str(k)
                num_field[item_number] = field

                k = k + 1

            row = []
            for item_number in config.item_numbers:
                row.append(num_field.get(item_number, ""))

            if show:
                for item_number in config.item_numbers:
                    print("{}: {}".format(item_number, num_field.get(item_number, "")))

            rows.append(row)

    return rows
# returns:
# rows <- for write_rows


# https://stackoverflow.com/a/30292938/7657721
def write_rows(file_csv, data, sep=',', show=False):
    data = DataFrame.from_records(data, columns=config.column_names)
    rows = len(data.index)
    # check if file exists
    if not os.path.isfile(file_csv):
        data.to_csv(file_csv, mode='a', index=False, sep=sep, header=True)
        if rows == 1:
            ret = "Successfully wrote {} row to new file".format(rows)
        else:
            ret = "Successfully wrote {} rows to new file".format(rows)

    # check if file is empty
    elif os.path.getsize(file_csv) == 0:
        data.to_csv(file_csv, mode='a', index=False, sep=sep, header=True)
        if rows == 1:
            ret = "Successfully wrote {} row to empty file".format(rows)
        else:
            ret = "Successfully wrote {} rows to empty file".format(rows)

    # check if file has mismatched column length
    elif len(data.columns) != len(pd.read_csv(file_csv, nrows=1, sep=sep).columns):
        ret = "Mismatched column length; no changes are made to csv file".format(
                str(len(data.columns)),
                str(len(pd.read_csv(file_csv, nrows=1, sep=sep).columns)))

    # check if file has mismatched column order
    elif not (data.columns == pd.read_csv(file_csv, nrows=1, sep=sep).columns).all():
        ret = "Mismatched column order; no changes are made to csv file"

    else:
        data.to_csv(file_csv, mode='a', index=False, sep=sep, header=False)
        if rows == 1:
            ret = "Successfully appended {} row to existing file".format(rows)
        else:
            ret = "Successfully appended {} rows to existing file".format(rows)

    return ret