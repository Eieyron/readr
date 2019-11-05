import cv2


def select_interior(cnts, rank):
    inner = [c[0] for c in zip(cnts, rank) if c[1][3] > 0]
    return inner


def select_rectangular(cnts, e=0.05):
    rect_cnts = []
    appx_cnts = []

    for i in range(len(cnts)):
        contour = cnts[i]

        p = cv2.arcLength(contour, cv2.isContourConvex(contour))
        approx = cv2.approxPolyDP(contour, e * p, True)
        if not len(approx) == 4: continue

        rect_cnts.append(contour)
        appx_cnts.append(approx)

    return rect_cnts, appx_cnts


def select_nonlinear(cnts, e=0.03):
    nonl_cnts = []

    for i in range(len(cnts)):
        contour = cnts[i]

        p = cv2.arcLength(contour, cv2.isContourConvex(contour))
        approx = cv2.approxPolyDP(contour, e * p, True)
        if not len(approx) > 2: continue

        nonl_cnts.append(contour)

    return nonl_cnts


def select_aspectratio(cnts, e=0.035, armin=0.1, armax=0.8):
    ar_cnts = []

    for i in range(len(cnts)):
        contour = cnts[i]

        p = cv2.arcLength(contour, cv2.isContourConvex(contour))
        approx = cv2.approxPolyDP(contour, e * p, True)
        (x, y, w, h) = cv2.boundingRect(approx)
        aspect_ratio = w / float(h)
        if not aspect_ratio >= armin and aspect_ratio <= armax: continue

        ar_cnts.append(contour)

    return ar_cnts