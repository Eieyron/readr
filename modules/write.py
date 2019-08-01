import os

import pandas as pd

from pandas import DataFrame

import modules.config as config

from modules.ai import read_character

# model needs these to run
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
        paper[i] = [config.field_join[i].join(filter(None, section[x:x+config.form_shape[i]]))
                    for x in range(0, len(section), config.form_shape[i])]

    return paper


def map_values(paper, show=False):
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
        for i in row:
            print(i)

    return row


# https://stackoverflow.com/a/30292938/7657721
def write_rows(file_csv, data, sep=',', show=False):
    data = DataFrame.from_records(data, columns=config.column_names)
    rows = len(data.index)
    # check if file exists
    if not os.path.isfile(file_csv):
        data.to_csv(file_csv, mode='a', index=False, sep=sep)
        ret = "Successfully wrote {} row/s to new file".format(rows)

    # check if file is empty
    elif os.path.getsize(file_csv) == 0:
        data.to_csv(file_csv, mode='a', index=False, sep=sep, header=True)
        ret = "Successfully wrote {} row/s to empty file".format(rows)

    # check if file has mismatched column length
    elif len(data.columns) != len(pd.read_csv(file_csv, nrows=1, sep=sep).columns):
        ret = "Mismatched column length (data:{}, file:{}); no changes are made to csv file".format(
                str(len(data.columns)),
                str(len(pd.read_csv(file_csv, nrows=1, sep=sep).columns)))

    # check if file has mismatched column order
    elif not (data.columns == pd.read_csv(file_csv, nrows=1, sep=sep).columns).all():
        ret = "Mismatched column order; no changes are made to csv file"

    else:
        data.to_csv(file_csv, mode='a', index=False, sep=sep, header=False)
        ret = "Successfully appended {} row/s to existing file".format(rows)

    return ret

