import os

from modules.config import mean_px
from modules.config import std_px

from modules.config import translate_data

from modules.extract import process_single

from modules.model import models

from modules.translate import translate_values

from modules.write import read_values
from modules.write import map_values
from modules.write import write_rows


def check_batch(app_tracker, img_dir):
    if img_dir == '':
        app_tracker.update_status_label("Aborted: no directory path selected")
        return None
    elif not os.path.isdir(str(img_dir)):
        app_tracker.update_status_label("Aborted: invalid directory path")
        return None
    elif not [file for file in os.listdir(img_dir) if file.endswith(".png") or file.endswith(".jpg")]:
        app_tracker.update_status_label("Aborted: no valid files found")
        return None
    else:
        app_tracker.update_status_label("Successfully loaded directory")
        app_tracker.update_progress_bar(10)
        return img_dir


def extract_batch(app_tracker, img_dir):
    app_tracker.update_status_label("Extracting")

    batch_list = os.listdir(img_dir)
    data = []
    i = 1
    for filename in batch_list:
        # extract fields from paper
        img_filename = os.path.join(img_dir, filename)
        paper = process_single(img_filename)

        if paper is not None:
            # read fields
            values = read_values(paper)
            # map their values
            row = map_values(values)

            # translate row if indicated
            if translate_data:
                row = translate_values(row)

            # add to list
            data.append(row)

            app_tracker.update_status_label("Extracted data from {}".format(filename))

        app_tracker.update_progress_bar(10+((i/len(batch_list))*10))
        i = i + 1

    if len(data) == 1:
        app_tracker.update_status_label("Extracted data from image file")
        app_tracker.update_progress_bar(20)
        return data
    else:
        app_tracker.update_status_label("Extracted data from {} image files".format(len(data)))
        app_tracker.update_progress_bar(20)
        return data


def check_multiple(app_tracker, img_files):
    if len(img_files) == 0:
        app_tracker.update_status_label("Aborted: no image files selected")
        return None
    else:
        for file in img_files:
            if not (file.endswith('.png') or file.endswith('.jpg')):
                img_files.remove(file)

        if len(img_files) == 0:
            app_tracker.update_status_label("Aborted: no valid image files to read")
            return None
        elif len(img_files) == 1:
            app_tracker.update_status_label("Successfully loaded image file")
            app_tracker.update_progress_bar(10)
            return img_files
        elif len(img_files) > 1:
            app_tracker.update_status_label("Successfully loaded {} image files".format(len(img_files)))
            app_tracker.update_progress_bar(10)
            return img_files


def extract_multiple(app_tracker, img_files):
    app_tracker.update_status_label("Extracting")

    data = []
    i = 1
    for file in img_files:
        # read fields
        paper = process_single(file)
        # map their values
        values = read_values(paper)
        row = map_values(values)

        # translate row if indicated
        if translate_data:
            row = translate_values(row)

        # add to list
        data.append(row)

        app_tracker.update_status_label("Extracted data from {}".format(file))
        app_tracker.update_progress_bar(10+((i/len(img_files))*10))
        i = i + 1

    if len(data) == 1:
        app_tracker.update_status_label("Extracted data from image file")
        app_tracker.update_progress_bar(20)
        return data
    else:
        app_tracker.update_status_label("Extracted data from {} image files".format(len(data)))
        app_tracker.update_progress_bar(20)
        return data


def check_single(app_tracker, img_file):
    if img_file == "":
        app_tracker.update_status_label("Aborted: no image file selected")
        return None
    elif not (img_file.endswith(".png") or img_file.endswith(".jpg")):
        app_tracker.update_status_label("Aborted: invalid image file")
        return None
    else:
        app_tracker.update_status_label("Successfully loaded image file")
        app_tracker.update_progress_bar(10)
        return img_file


def extract_single(app_tracker, img_file):
    app_tracker.update_status_label("Extracting")

    paper = process_single(img_file)
    values = read_values(paper)
    row = map_values(values)

    # translate row if indicated
    if translate_data:
        row = translate_values(row)

    # add to list
    data = [row]

    app_tracker.update_status_label("Extracted data from {}".format(img_file))
    app_tracker.update_progress_bar(20)

    return data


def check_file(app_tracker, csv_file):
    if csv_file == "":
        app_tracker.update_status_label("Aborted: no csv file selected")
        return None
    elif not csv_file.endswith('.csv'):
        # app_tracker.update_status_label("Aborted: invalid csv file")
        app_tracker.update_status_label("Successfully loaded csv file")
        app_tracker.update_progress_bar(30)
        return csv_file + ".csv"
    else:
        app_tracker.update_status_label("Successfully loaded csv file")
        app_tracker.update_progress_bar(30)
        return csv_file


def write_data(app_tracker, csv_file, data):
    try:
        ret = write_rows(csv_file, data)
    except PermissionError:
        ret = "Aborted: permission denied"

    app_tracker.update_status_label(ret)
    app_tracker.update_progress_bar(40)

