import cnfg

import cv2
import os

from fn import *

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
# contours.sort(key=lambda x:get_contour_precedence(x, img.shape[1]))
def get_contour_precedence(contour, cols, tolerance_factor=10):
    origin = cv2.boundingRect(contour)
    return ((origin[1] // tolerance_factor) * tolerance_factor) * cols + origin[0]

# stat <- 2 for height, 3 for width, 4 for area 
def get_contours(src, min_ratio=0, max_ratio=1, stat=4, tolerance_factor=10, show=False):
	# font for printing text
	font = cv2.FONT_HERSHEY_SIMPLEX

	# preprocessing
	mod = src.copy()
	edge = auto_canny(mod)
	# cv2.imshow("edge after autocanny", edge)
	# cv2.waitKey(0)
	edge = cv2.GaussianBlur(edge,(3,3),0)
	# cv2.imshow("edge after blur", edge)
	# cv2.waitKey(0)
	(contours, _) = cv2.findContours(edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	# list to return
	cnts = []

	# per-stat processes
	if (stat == 2) or (stat == "height"):
		src_width = src.shape[0]
		min_width = src_width * min_ratio
		max_width = src_width * max_ratio

		for i in range(len(contours)):
			contour = contours[i]
			x, y, w, h = cv2.boundingRect(contour)

			if (w <= min_width): continue
			if (w >= max_width): continue

			cnts.append(contour)

	elif (stat == 3) or (stat == "width"):
		src_height = src.shape[1]
		min_height = src_height * min_ratio
		max_height = src_height * max_ratio

		for i in range(len(contours)):
			contour = contours[i]
			x, y, w, h = cv2.boundingRect(contour)

			if (h <= min_height): continue
			if (h >= max_height): continue

			cnts.append(contour)

	elif (stat == 4) or (stat == "area"):
		src_area = src.shape[0] * src.shape[1]
		min_area = src_area * min_ratio
		max_area = src_area * max_ratio

		for i in range(len(contours)):
			contour = contours[i]
			x, y, w, h = cv2.boundingRect(contour)
			a = w * h

			if (a <= min_area): continue
			if (a >= max_area): continue

			cnts.append(contour)

	# sorts contours from left to right, top to bottom
	cnts.sort(key = lambda x:get_contour_precedence(x, mod.shape[1], tolerance_factor))

	# for displaying detected contours and order
	if (show == True):
		for i in range(len(cnts)):
			contour = cnts[i]
			x, y ,w, h = cv2.boundingRect(contour)
			M = cv2.moments(contour)
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])
			midpoint = cX, cY

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
    for file in batch:
        img_filename = os.path.join(dir_batch, filename)
        form_list = process_single(img_filename)

        batch_list.append(form_list)

    return batch_list
# returns:
# batch_list

# fn to process a single img
def process_single(filename):
    filename = os.fsdecode(filename)

    if (filename.endswith(".png") or filename.endswith(".jpg")):
        img = cv2.imread(filename, 0)

        if (img.shape[0] > img.shape[1]) and (cnfg.is_landscape == True):
        	img = cv2.transpose(img)
        	img = cv2.flip(img, 1)

        form_list = process_paper(img)

    return form_list
# returns:
# form_list

def process_paper(img_paper):
	paper = preprocess_image(img_paper, show=cnfg.show_preprocessing)

	# get the largest contour
	stats = get_contours(paper, min_ratio=cnfg.min_ratio_region, max_ratio=cnfg.max_ratio_region, show=cnfg.show_contours)
	stat = max(stats, key = cv2.contourArea)
	x, y, w, h = cv2.boundingRect(stat)

	# crop
	region = crop_by_origin(paper, x, y, w, h, padding=cnfg.padding_region, replace_pad=cnfg.repl_pad_region)

	region_list = process_region(region)

	if (cnfg.show_region == True):
		cv2.imshow("region", region)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	return region_list


def process_region(region):
	stats = get_contours(region, min_ratio=cnfg.min_ratio_section, max_ratio=cnfg.max_ratio_section, tolerance_factor=cnfg.tolerance_section, show=cnfg.show_contours)
	
	region_list = []

	for i in range(len(stats)):
		x, y, w, h = cv2.boundingRect(stats[i])

		section = crop_by_origin(region, x, y, w, h, padding=cnfg.padding_section, replace_pad=cnfg.repl_pad_section)
		section_list = process_section(section)
		region_list.append(section_list)

		if (cnfg.show_section == True):
			cv2.imshow("section", section)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

	return region_list


def process_section(section):
	stats = get_contours(section, min_ratio=cnfg.min_ratio_field, max_ratio=cnfg.max_ratio_field, tolerance_factor=cnfg.tolerance_field, show=cnfg.show_contours)

	section_list = []

	for i in range(len(stats)):
		x, y, w, h = cv2.boundingRect(stats[i])

		field = crop_by_origin(section, x, y, w, h, padding=cnfg.padding_field, replace_pad=cnfg.repl_pad_field)
		field_list = process_field(field)
		section_list.append(field_list)

		if (cnfg.show_field == True):
			cv2.imshow("field", field)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

	return section_list

def process_field(field):
	stats = get_contours(field, min_ratio=cnfg.min_ratio_character, max_ratio=cnfg.max_ratio_character, tolerance_factor=cnfg.tolerance_character, show=cnfg.show_contours)

	field_list = []

	for i in range(len(stats)):
		x, y, w, h = cv2.boundingRect(stats[i])

		character = crop_by_origin(field, x, y, w, h, padding=cnfg.padding_character, replace_pad=cnfg.repl_pad_character)
		character = center_by_mass(character, 20)
		field_list.append(character)

		if (cnfg.show_character == True):
			cv2.imshow("character", character)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

	return field_list

if __name__ == '__main__':
	paper = process_single("./../images/v2.png")