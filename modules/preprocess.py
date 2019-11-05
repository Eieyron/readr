import cv2
import numpy as np

from modules.misc import write_img


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
# returns:
# edged <- for extracting contours


# does nothing and only returns the input img if there are no contours found
# gets the largest contour, its center of mass, and returns it
# src <- to get center of mass from
# nsize <- size of input image after size normalization
# lsize <- size of the larger image input image will be centered
def center_by_mass(src, nsize=20, lsize=28):
    # do this only if lsize is larger than nsize, duh
    if lsize > nsize:
        # normalize input img
        img = reshape_to_square(src, nsize)

        # invert color, then get contour
        img = cv2.bitwise_not(img)
        contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if len(contours) != 0:
            # get the largest contour, the digit itself
            c = max(contours, key=cv2.contourArea)

            # make a mask and draw the contour on it
            mask = np.zeros(img.shape, np.uint8)
            cv2.drawContours(mask, [c], -1, 255, -1)

            # write it on a new img
            mod = cv2.bitwise_and(img, mask)
            mod = cv2.bitwise_not(mod)

            # get the center of mass of size normalized image
            # ZeroDivisionError
            n = cv2.moments(c)
            if n["m00"] != 0:
                n_x = int(n["m10"]/n["m00"])
                n_y = int(n["m01"]/n["m00"])
            else:
                n_x, n_y = 0, 0

            # # draw com of digit
            # cv2.circle(mod, (nX, n_y), 1, (125), 1)
            # print("nX: "+str(nX)+" n_y: "+str(n_y))

            # cv2.imshow("mod", mod)
            # cv2.waitKey(0)

            # create white blank image 
            blank = np.zeros((lsize, lsize), np.uint8)
            blank[:] = 255

            # get its center
            lX = lY = int(sum(np.arange(lsize))//lsize)

            # get the difference of two images as offset
            dX = abs(lX - n_x)
            dY = abs(lY - n_y)

            # edge case when input and recipient shape are for some reason not the same
            # get their shape difference, and crop the input shape starting from the origin
            h1, w1 = blank[dY:dY+nsize, dX:dX+nsize].shape[:2] 
            h2, w2 = mod.shape[:2]
            h3 = abs(h1-h2)
            w3 = abs(w1-w1)

            blank[dY:dY+nsize, dX:dX+nsize] = mod[0:h2-h3, 0:w2-w3]

            # # see if it works
            # cv2.circle(blank, (lX, lY), 1, (125), 1)
            # print("dX: "+str(dX)+" dY: "+str(dY))
            # cv2.imshow("result", blank)
            # cv2.waitKey(0)

            return blank

    return src
# returns:
# blank <- the centered image
# src <- source image


# reshape to square with sides s. 
# utilizes padding if src is not square to avoid distortion
# params:
# src <- img to be resized
# s <- w, h of returned square
def reshape_to_square(src, s):
    h, w = src.shape[:2]

    if w > h:
        p = int((w - h)/2)
        src = cv2.copyMakeBorder(src, p, p, 0, 0, cv2.BORDER_CONSTANT,value=[255,255,255])
    elif w < h:
        p = int((h - w)/2)
        src = cv2.copyMakeBorder(src, 0, 0, p, p, cv2.BORDER_CONSTANT,value=[255,255,255])

    src = cv2.resize(src, (s, s))
    return src
# returns:
# img


# ref
# https://stackoverflow.com/questions/42065405/remove-noise-from-threshold-image-opencv-python
# params:
# img <- img to be processed
# show <- if output of every process should be shown (default=False)
def preprocess_image(img, show=False):
    if show:
        cv2.imshow("original img", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    write_img(img, "orimg")

    # denoisify image
    img = denoisify_image(img, show)

    # use edge coherence enhancing diffusion filter
    # img = coherence_filter(img, show)

    # convert image to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img = cv2.bitwise_not(img)
    # remove small black points
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, (5, 5))
    img = cv2.bitwise_not(img)

    if show:
        cv2.imshow("img after closing", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return img
# returns:
# img <- modified img


# params
# img <- unprocessed image
def denoisify_image(img, show=False):
    morph = img.copy()

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel)
    morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)

    # take morphological gradient
    # unnecessary for text on white background
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    # gradient_image = cv2.morphologyEx(morph, cv2.MORPH_GRADIENT, kernel)

    # split the gradient image into channels
    image_channels = np.split(np.asarray(morph), 3, axis=2)

    channel_height, channel_width, _ = image_channels[0].shape

    # apply Otsu threshold to each channel
    for i in range(0, 3):
        _, image_channels[i] = cv2.threshold(image_channels[i], 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)
        image_channels[i] = np.reshape(image_channels[i], newshape=(channel_height, channel_width, 1))

    # merge the channels
    img = np.concatenate((image_channels[0], image_channels[1], image_channels[2]), axis=2)

    if show:
        cv2.imshow("denoised img", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    write_img(img, "dnimg")

    return img
# returns
# img <- binarized image


# ref
# http://www.mia.uni-saarland.de/Publications/weickert-dagm03.pdf
# keyword:
# edge coherence enhancing diffusion filter
# params:
# img <- binarized image
# sigma <-
# str_sigma <-
# blend <-
# iter_n <- diffusion time; how many times the operation is executed
def coherence_filter(img, sigma=31, str_sigma=1, blend=0.3, iter_n=4, show=False):
    h, w = img.shape[:2]

    for i in range(iter_n):
        # print(i)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        eigen = cv2.cornerEigenValsAndVecs(gray, str_sigma, 3)
        eigen = eigen.reshape(h, w, 3, 2)  # [[e1, e2], v1, v2]
        x, y = eigen[:, :, 1, 0], eigen[:, :, 1, 1]

        gxx = cv2.Sobel(gray, cv2.CV_32F, 2, 0, ksize=sigma)
        gxy = cv2.Sobel(gray, cv2.CV_32F, 1, 1, ksize=sigma)
        gyy = cv2.Sobel(gray, cv2.CV_32F, 0, 2, ksize=sigma)
        gvv = x*x*gxx + 2*x*y*gxy + y*y*gyy
        m = gvv < 0

        ero = cv2.erode(img, None)
        dil = cv2.dilate(img, None)
        img1 = ero
        img1[m] = dil[m]
        img = np.uint8(img*(1.0 - blend) + img1*blend)

    if show:
        cv2.imshow("after filter", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return img
# returns:
# img <- cleaned image


# ref:
# https://stackoverflow.com/questions/4993082/how-to-sharpen-an-image-in-opencv
# fn to sharpen image using unsharp mask
# img <- img to sharpen
# kernel_size <- tuple containing dim of kernel
# sigma <- for GaussianBlur
# amount <- higher value, sharper
# threshold <- for low contrast cases
def sharpen(image, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
    blurred = cv2.GaussianBlur(image, kernel_size, sigma)

    sharpened = float(amount+1)*image-float(amount)*blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)

    if threshold > 0:
        low_contrast_mask = np.absolute(image-blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)

    return sharpened
# returns:
# sharpened <- sharpened image


# ref:
# http://opencvpython.blogspot.com/2012/05/skeletonization-using-opencv-python.html
# img <- cleaned and binarized img
def get_morphological_skeleton(img, show=False):
    img = cv2.bitwise_not(img)

    size = np.size(img)
    skel = np.zeros(img.shape, np.uint8)

    ret, img = cv2.threshold(img, 127, 255, 0)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    done = False

    iter = 0
    while not done:
        eroded = cv2.erode(img, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(img, temp)
        skel = cv2.bitwise_or(skel, temp)
        img = eroded.copy()

        zeros = size - cv2.countNonZero(img)
        if zeros == size:
            done = True

        iter = iter + 1

    img = cv2.bitwise_not(skel)

    if show:
        cv2.imshow("skel", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return img, iter
# returns:
# img <- morphological skeleton of the image


# https://www.pyimagesearch.com/2014/05/05/building-pokedex-python-opencv-perspective-warping-step-5-6/
def transform_perspective(img, corners):
    def reorder_corner_points(corners):
        tr, tl, bl, br = [(corner[0][0], corner[0][1]) for corner in corners][0:4]
        return tl, tr, br, bl

    # order the points in clockwise order
    ordered_corners = reorder_corner_points(corners)
    tl, tr, br, bl = ordered_corners

    # determine width of new image which is the max distance between
    # (bottom right and bottom left) or (top right and top left) x-coordinates
    width_A = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    width_B = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    width = max(int(width_A), int(width_B))

    # determine height of new image which is the max distance between
    # (top right and bottom right) or (top left and bottom left) y-coordinates
    height_A = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    height_B = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    height = max(int(height_A), int(height_B))

    # construct new points to obtain top-down view of image in
    # tr, tl, bl, br order
    dimensions = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1],
                           [0, height - 1]], dtype="float32")

    # convert to Numpy format
    ordered_corners = np.array(ordered_corners, dtype="float32")

    # find perspective transform matrix
    matrix = cv2.getPerspectiveTransform(ordered_corners, dimensions)

    # get the transformed image
    warped = cv2.warpPerspective(img, matrix, (width, height))

    # rotate the transformed image
    warped = cv2.transpose(warped)
    warped = cv2.flip(warped, 0)

    return warped


# for get_contours
# src <- image apply canny to
def apply_canny(src, sigma=0.33):
    # preprocessing
    edge = auto_canny(src, sigma)
    edge = cv2.GaussianBlur(edge, (3, 3), 0)

    return edge
# returns
# edge <- the canny image


# for get_contours in section
def apply_threshold(src):
    prep = src.copy()

    # prep = cv2.GaussianBlur(prep, (3, 3), 0)
    # prep = cv2.bitwise_not(prep)
    prep = cv2.threshold(prep, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]

    return prep
# returns
# prep <- thresholded image