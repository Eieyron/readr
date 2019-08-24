import cv2
import numpy as np


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


# params:
# src <- image to be cropped
# x, y <- origins
# w, h <- width, height
# padding <- padding, can be + or -
# replace_pad <- just repads the image; for replacing border artifacts; only for negative padding
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


# params:
# img <- img to be processed
# show <- if output of every process should be shown (default=False)
def preprocess_image(img, show=False):
    if show:
        cv2.imshow("original img", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    # clear spots that may be highlighted in adapted thresholding
    _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    if show:
        cv2.imshow("img after binary thresholding", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # remove possible shadows (?)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    if show:
        cv2.imshow("img after adaptive thresholding", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    img = cv2.bitwise_not(img)

    # too destructive    
    # # remove "holes"
    # img = cv2.morphologyEx(img, cv2.MORPH_OPEN, (5,5))
    # if (show == True):
    #     img = cv2.bitwise_not(img)
    #     cv2.imshow("img after opening", img)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()
    #     img = cv2.bitwise_not(img)

    # remove small black points
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, (5,5))
    if show:
        img = cv2.bitwise_not(img)
        cv2.imshow("img after closing", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        img = cv2.bitwise_not(img)

    img = cv2.bitwise_not(img)

    return img
# returns:
# img <- modified img
