import cv2


# for use with os.path.join
# fixes hardcoded path strings with /
# by splitting the string by these chars
# and letting os.path.join do the job
# str_path <- path string to be processed
def fix_path(str_path):
    # split by '/'
    res = str_path.split('/')

    return res
# res <- list to be used with os.path.join
# os.path.join('',*fix_path(str_path))


# for debugging and documentation purposes
# saves to a folder named debug in root dir if it exists
def write_img(img, name, loc="./debug/"):
    cv2.imwrite("{}{}.png".format(loc, name), img)


# img <- img where the detected contours will be drawn on
# cnts <- list of detected contours
def draw_detected_contours(img, cnts):
    # font for printing text
    font = cv2.FONT_HERSHEY_SIMPLEX

    # create a copy of the original image
    mod = img.copy()

    # index and draw a bounding box around each contour
    for i in range(len(cnts)):
        contour = cnts[i]
        m = cv2.moments(contour)
        c_x = int(m["m10"] / m["m00"])
        c_y = int(m["m01"] / m["m00"])
        midpoint = c_x, c_y

        # x, y, w, h = cv2.boundingRect(contour)
        # midpoint = int(w//2), int(h//2)

        cv2.putText(mod, str(i), midpoint, font, 1, (125, 0, 0), 2)
        cv2.drawContours(mod, [contour], 0, (125, 0, 0), 3)

    return mod
# returns:
# mod <- modified image

