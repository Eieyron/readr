import cv2
import os

import numpy as np

import modules.config as config

from modules.preprocess import center_by_mass
from modules.preprocess import crop_by_origin
from modules.preprocess import preprocess_image


# lazy canny
# https://www.pyimagesearch.com/2015/04/06/zero-parameter-automatic-canny-edge-detection-with-python-and-opencv/
def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged


# https://stackoverflow.com/questions/39403183/python-opencv-sorting-contours
# usage: 
# 	contours.sort(key=lambda x:get_contour_precedence(x, img.shape[1]))
# sorts contours from left to right, top to bottom
# contour <- single contour to be ordered
# cols <- number of columns of contours
# tolerance factor <- how vertically different a contour should be to be considered top or bottom of another contour?
def get_contour_precedence(contour, cols, tolerance_factor=10):
    origin = cv2.boundingRect(contour)
    return ((origin[1] // tolerance_factor) * tolerance_factor) * cols + origin[0]


# src <- image to get contours from
# rectangular_filter <- if False, checks if extracted contours are rectangular
# min_ratio, max_ratio <- min and max ratio of the stat of the contour to the stat of the src to be considered
# tolerance_factor <- for ordering contours using get_contour_precedence
# show <- show processes
def get_contours(src, rectangular_filter=True, min_ratio=0, max_ratio=1, tolerance_factor=10, show=False):
    # font for printing text
    font = cv2.FONT_HERSHEY_SIMPLEX

    # preprocessing
    mod = src.copy()
    edge = auto_canny(mod)
    edge = cv2.GaussianBlur(edge, (3, 3), 0)

    contours, _ = cv2.findContours(edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # list to return
    cnts = []

    # compute src_area ratio
    src_area = src.shape[0] * src.shape[1]
    min_area = src_area * min_ratio
    max_area = src_area * max_ratio

    for i in range(len(contours)):
        contour = contours[i]
        # x, y, w, h = cv2.boundingRect(contour)
        # a = w * h
        a = cv2.contourArea(contour)

        if a <= 0: continue
        elif a <= min_area: continue
        elif a >= max_area: continue
        elif rectangular_filter:
            # check if rectangular
            p = cv2.arcLength(contour, cv2.isContourConvex(contour))
            approx = cv2.approxPolyDP(contour, 0.04*p, True)
            if not len(approx) == 4: continue

        cnts.append(contour)

    # sorts contours from left to right, top to bottom
    cnts.sort(key=lambda x: get_contour_precedence(x, mod.shape[1], tolerance_factor))

    # for displaying detected contours and order
    if show:
        for i in range(len(cnts)):
            contour = cnts[i]
            m = cv2.moments(contour)
            c_x = int(m["m10"] / m["m00"])
            c_y = int(m["m01"] / m["m00"])
            midpoint = c_x, c_y

            cv2.putText(mod, str(i), midpoint, font, 1, 125, 2)
            cv2.drawContours(mod, [contour], 0, 125, 3)

        cv2.imshow("detected contours", mod)
        cv2.waitKey(0)

    return cnts


# fn to process a whole dir of doc
# params:
# dir_batch <- folder where the batch of img are stored
def process_batch(dir_batch):
    batch = os.listdir(dir_batch)

    batch_list = []
    for filename in batch:
        img_filename = os.path.join(dir_batch, filename)
        form_list = process_single(img_filename)

        if form_list is not None:
            batch_list.append(form_list)

    return batch_list
# returns:
# batch_list


# fn to process a single img
def process_single(filename):
    filename = os.fsdecode(filename)

    # default files not fitting the criteria to None
    form_list = None
    if filename.endswith(".png") or filename.endswith(".jpg"):
        img = cv2.imread(filename, 0)

        # rotate clockwise once if landscape and length is greater than height
        # so that the fields to be extracted and read are right side up
        if (img.shape[0] > img.shape[1]) and config.is_landscape:
            img = cv2.transpose(img)
            img = cv2.flip(img, 1)

        form_list = process_paper(img)

    return form_list
# returns:
# form_list


# extract region from paper
def process_paper(img_paper):
    paper = preprocess_image(img_paper, show=config.show_preprocessing)

    # get the largest contour
    stats = get_contours(paper, min_ratio=config.min_ratio_region, max_ratio=config.max_ratio_region,
                         show=config.show_contours)
    stat = max(stats, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(stat)

    # crop
    region = crop_by_origin(paper, x, y, w, h, padding=config.padding_region, replace_pad=config.repl_pad_region)

    region_list = process_region(region)

    if config.show_region:
        cv2.imshow("region", region)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return region_list


# extract sections from region
def process_region(region):
    stats = get_contours(region, rectangular_filter=False, min_ratio=config.min_ratio_section, max_ratio=config.max_ratio_section,
                         tolerance_factor=config.tolerance_section, show=config.show_contours)

    region_list = []

    for i in range(len(stats)):
        x, y, w, h = cv2.boundingRect(stats[i])

        section = crop_by_origin(region, x, y, w, h, padding=config.padding_section,
                                 replace_pad=config.repl_pad_section)
        section_list = process_section(section)
        region_list.append(section_list)

        if config.show_section:
            cv2.imshow("section", section)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    return region_list


# extract fields from sections
def process_section(section):
    stats = get_contours(section, min_ratio=config.min_ratio_field, max_ratio=config.max_ratio_field,
                         tolerance_factor=config.tolerance_field, show=config.show_contours)

    section_list = []

    for i in range(len(stats)):
        x, y, w, h = cv2.boundingRect(stats[i])

        field = crop_by_origin(section, x, y, w, h, padding=config.padding_field, replace_pad=config.repl_pad_field)
        field_list = process_field(field)
        section_list.append(field_list)

        if config.show_field:
            cv2.imshow("field", field)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    return section_list


# extract characters from fields
def process_field(field):
    stats = get_contours(field, rectangular_filter=False, min_ratio=config.min_ratio_character, max_ratio=config.max_ratio_character,
                         tolerance_factor=config.tolerance_character, show=config.show_contours)

    field_list = []

    for i in range(len(stats)):
        x, y, w, h = cv2.boundingRect(stats[i])

        character = crop_by_origin(field, x, y, w, h, padding=config.padding_character,
                                   replace_pad=config.repl_pad_character)
        try:
            character = center_by_mass(character, nsize=20, lsize=28)
            field_list.append(character)

            if config.show_character:
                cv2.imshow("character", character)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

        except ValueError as err:
            if config.show_error:
                cv2.imshow(str(err), character)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

    return field_list

# # unit test
# # use with debug section in settings.ini
# # which is loaded here by config.py
# if __name__ == '__main__':
# 	paper = process_single("./../images/v2.png")
