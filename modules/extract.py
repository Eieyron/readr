import cv2
import os

import modules.config as config

from modules.filter import select_rectangular

from modules.misc import draw_detected_contours
from modules.misc import write_img

from modules.preprocess import apply_canny
from modules.preprocess import apply_threshold
from modules.preprocess import center_by_mass
from modules.preprocess import preprocess_image
from modules.preprocess import transform_perspective


# params:
# src <- image to be cropped
# x, y <- origins
# w, h <- width, height
# padding <- padding, can be + or -
# replace_pad <- just re-pads the image; for replacing border artifacts; only for negative padding
def crop_by_origin(src, x, y, w, h, padding=0, replace_pad=False):
    p = padding
    if replace_pad:
        b = abs(p)
        img = src[y-p:y+h+p, x-p:x+w+p].copy()
        padded = cv2.copyMakeBorder(img, b, b, b, b, cv2.BORDER_CONSTANT,value=[255,255,255])
        return padded
    else:
        return src[y-p:y+h+p, x-p:x+w+p].copy()
# returns:
# img


# https://stackoverflow.com/questions/39403183/python-opencv-sorting-contours
# usage: 
# 	contours.sort(key=lambda x:get_contour_precedence(x, img.shape[1]))
# determines the rank or order of a contour
# contour <- single contour to be ordered
# cols <- number of columns of contours
# tolerance_factor <- how vertically displaced a contour should be to be considered top or bottom of another contour?
def get_contour_precedence(contour, cols, tolerance_factor=10):
    origin = cv2.boundingRect(contour)
    return ((origin[1] // tolerance_factor) * tolerance_factor) * cols + origin[0]
# returns:
# order of the contour


# sorts contours from left to right, top to bottom
# cnts <- list of contours to be ordered
# cols <- number of columns of contours
# tol <- tolerance_factor, how vertically displaced a contour should be
#        to be considered top or bottom of another contour?
# heir <- hierarchy list that goes with cnts
def sort_contours(cnts, cols, tol, heir=None):
    if heir is None:
        cnts.sort(key=lambda x: get_contour_precedence(x, cols, tol))
        return cnts
    else:
        cnts, heir = zip(*sorted(zip(cnts, heir), key=lambda x: get_contour_precedence(x[0], cols, tol)))
        return cnts, heir
# returns:
# cnts <- ordered list of contours


# src <- image to get contours from
# min_ratio, max_ratio <- min and max ratio of the stat of the contour to the stat of the src to be considered
# show <- show processes
def get_contours(src, min_ratio=0, max_ratio=1, retr_mode=cv2.RETR_EXTERNAL):

    # get contours and hierarchy
    contours, hierarchy = cv2.findContours(src, retr_mode, cv2.CHAIN_APPROX_SIMPLE)
    if hierarchy is not None: hierarchy = hierarchy[0]

    # lists to return
    cnts = []
    rank = []

    # compute src_area ratio
    src_area = src.shape[0] * src.shape[1]
    min_area = src_area * min_ratio
    max_area = src_area * max_ratio

    # initial filtering of contours by size
    for i in range(len(contours)):
        c = contours[i]
        h = hierarchy[i]

        a = cv2.contourArea(c)

        m = cv2.moments(c)

        if m["m00"] <= 0: continue
        elif a <= 0: continue
        elif a <= min_area: continue
        elif a >= max_area: continue

        cnts.append(c)
        rank.append(h)

    write_img(src, "acimg_{}_{}_{}".format(len(cnts), src.shape[0], src.shape[1]))

    return cnts, rank
# returns:
# cnts <- list of cnts that satisfy the conditions
# rank <- hierarchy of filtered contours


# fn to process a whole dir of doc
# unused by actual app
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
        # read as b&w
        # img = cv2.imread(filename, 0)
        # read as colored; changed for preprocess_image
        img = cv2.imread(filename, 1)

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
    # preprocessing
    # put image processing operations exclusive to this phase here
    # copy the original image, use it to do the operations,
    # and carry over the results on the original

    paper = preprocess_image(img_paper, show=config.show_preprocessing)
    # preprocessing ends here

    # apply canny
    edge = apply_canny(paper)

    # get external contours
    stats = get_contours(edge, min_ratio=config.min_ratio_region, max_ratio=config.max_ratio_region)[0]

    # filter out non-rectangular contours
    stats = select_rectangular(stats)[0]

    # get the largest single contour
    stat = max(stats, key=cv2.contourArea)

    # use perspective transform
    p = cv2.arcLength(stat, True)
    warped = transform_perspective(paper, cv2.approxPolyDP(stat, 0.05*p, True))

    # cv2.imshow("warped", warped)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    region = crop_by_origin(warped, 0, 0, warped.shape[1], warped.shape[0],
                            padding=config.padding_region, replace_pad=config.repl_pad_region)

    # extract sections from region
    region_list = process_region(region)

    # show results
    mod = draw_detected_contours(paper, [stat])
    write_img(mod, "dcimg_{}_{}_{}_{}".format(1, len(stats), paper.shape[0], paper.shape[1]))
    write_img(region, "rgimg_{}_{}_{}_{}_{}_{}_{}_{}".format(2, 1, paper.shape[0], paper.shape[1], 0, 0,
                                                             warped.shape[1], warped.shape[0]))

    if config.show_contours:
        cv2.imshow("detected contours", mod)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if config.show_region:
        cv2.imshow("region", region)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return region_list


# extract sections from region
def process_region(region):
    # preprocessing
    # put image processing operations exclusive to this phase here
    # copy the original image, use it to do the operations,
    # and carry over the results on the original

    # preprocessing ends here

    # apply canny
    edge = apply_canny(region)

    # get external contours
    stats = get_contours(edge, min_ratio=config.min_ratio_section, max_ratio=config.max_ratio_section)[0]

    # sort contours
    stats = sort_contours(stats, region.shape[1], config.tolerance_section)

    # show detected contours
    mod = draw_detected_contours(region, stats)
    write_img(mod, "dcimg_{}_{}_{}_{}".format(2, len(stats), region.shape[0], region.shape[1]))
    if config.show_contours:
        cv2.imshow("detected contours", mod)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # loop through each section and extract their fields
    region_list = []
    for i in range(len(stats)):
        # get the bounding box of the contour
        x, y, w, h = cv2.boundingRect(stats[i])

        # crop into new image
        section = crop_by_origin(region, x, y, w, h, padding=config.padding_section,
                                 replace_pad=config.repl_pad_section)

        if i < len(config.form_shape):
            # extract fields from section
            section_list = process_section(section, config.form_shape[i])
            region_list.append(section_list)

            # show extracted sections
            if config.show_section:
                cv2.imshow("section", section)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            write_img(section, "scimg{}_{}_{}_{}_{}_{}_{}_{}".format(3, i, region.shape[0], region.shape[1], x, y, w, h))

    return region_list


# extract fields from sections
def process_section(section, row_length):
    # preprocessing
    # put image processing operations exclusive to this phase here
    # copy the original image, use it to do the operations,
    # and carry over the results on the original

    # first flood fill
    floodfilled = apply_threshold(section)
    cv2.floodFill(floodfilled, None, (10, 10), 255)

    # apply canny for finding contours
    to_detect = apply_canny(floodfilled)
    if config.show_preprocessing:
        cv2.imshow("to_detect", to_detect)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # second flood fill
    to_crop = cv2.bitwise_not(floodfilled)
    cv2.floodFill(to_crop, None, (10, 10), 255)
    if config.show_preprocessing:
        cv2.imshow("to_crop", to_crop)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # preprocessing ends here

    # get all contours
    stats = get_contours(to_detect, min_ratio=config.min_ratio_field, max_ratio=config.max_ratio_field)[0]

    # filter rectangular
    stats = select_rectangular(stats)[0]

    # sort contours
    # sort from top to bottom
    stats = sort_contours(stats, section.shape[1], config.tolerance_field)
    # sort from left to right
    temp = []
    for i in range(0, len(stats), row_length):
        temp.extend(sort_contours(stats[i:i+row_length], section.shape[1], 100))
    # print("Stats: {}, Temp: {}".format(len(stats), len(temp)))
    stats = temp

    # show detected contours
    mod = draw_detected_contours(section, stats)
    write_img(mod, "dcimg_{}_{}_{}_{}".format(3, len(stats), section.shape[0], section.shape[1]))
    if config.show_contours:
        cv2.imshow("detected contours", mod)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # loop through each field and extract their characters
    section_list = []
    for i in range(len(stats)):
        x, y, w, h = cv2.boundingRect(stats[i])

        field = crop_by_origin(to_crop, x, y, w, h, padding=config.padding_field, replace_pad=config.repl_pad_field)
        field_list = process_field(field)
        section_list.append(field_list)

        if config.show_field:
            cv2.imshow("field", field)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        write_img(field, "flimg{}_{}_{}_{}_{}_{}_{}_{}".format(4, i, section.shape[0], section.shape[1], x, y, w, h))

    write_img(section, "msimg{}_{}_{}_{}".format(4, len(stats), section.shape[0], section.shape[1]))

    return section_list


# extract characters from fields
def process_field(field):
    # preprocessing
    # put image processing operations exclusive to this phase here
    # copy the original image, use it to do the operations,
    # and carry over the results on the original

    # # clear noise
    # field = cv2.bitwise_not(field)
    # field = cv2.morphologyEx(field, cv2.MORPH_CLOSE, (5, 5))
    # field = cv2.bitwise_not(field)

    # preprocessing ends here

    # apply canny
    edge = apply_canny(field)

    # extract external contours
    stats = get_contours(edge, min_ratio=config.min_ratio_character, max_ratio=config.max_ratio_character)[0]

    # sort contours
    stats = sort_contours(stats, field.shape[1], config.tolerance_character)

    # show detected contours
    mod = draw_detected_contours(field, stats)
    write_img(mod, "dcimg_{}_{}_{}_{}".format(4, len(stats), field.shape[0], field.shape[1]))
    if config.show_contours:
        cv2.imshow("detected contours", mod)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # loop through each character
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

            write_img(character, "chimg_{}_{}_{}_{}_{}_{}_{}_{}".format(5, i, field.shape[0], field.shape[1], x, y, w, h))

        except ValueError as err:
            if config.show_error:
                cv2.imshow(str(err), character)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

    return field_list
