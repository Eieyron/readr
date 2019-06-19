import cv2
import os
import numpy as np

# IMAGE PROCESSING FUNCTIONS

# params:
# imgScan <- scanned image
# imgReference <- image template to be used as reference for alignment
# max_features <- max num of features to be compared and matched
# good_match_percent <- how many good matches in % before terminating iteration
# show <- if output of every process should be shown (default=False)
def alignImages(imgScan, imgReference, max_features = 500, good_match_percent = 0.15, show=False):
  
    # convert to uint8
    # imgScan = imgScan.astype('uint8')
    # imgReference = imgReference.astype('uint8')

    # resize (experimental)
    # h, w = imgReference.shape[:2]
    # imgScan = cv2.resize(imgScan, (w, h))

    # no need for converting to grayscale as images have already been loaded as grayscale
    # to grayscale
    # imgScanGray = cv2.cvtColor(imgScan, cv2.COLOR_BGR2GRAY)
    # imgReferenceGray = cv2.cvtColor(imgReference, cv2.COLOR_BGR2GRAY)

    # detect ORB features and compute descriptors.
    orb = cv2.ORB_create(max_features)
    keypoints1, descriptors1 = orb.detectAndCompute(imgScanGray, None)
    keypoints2, descriptors2 = orb.detectAndCompute(imgReferenceGray, None)
       
    # match features.
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(descriptors1, descriptors2, None)
       
    # sort matches by score
    matches.sort(key=lambda x: x.distance, reverse=False)
     
    # remove not so good matches
    numGoodMatches = int(len(matches) * good_match_percent)
    matches = matches[:numGoodMatches]
     
    # draw top matches
    imMatches = cv2.drawMatches(imgScan, keypoints1, imgReference, keypoints2, matches, None)
    # cv2.imwrite("matches.jpg", imMatches)
    if (show==True): 
        cv2.imshow("img feature matches", imMatches)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
       
    # extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)
     
    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt
       
    # find homography
    h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)
     
    # use homography
    height, width, channels = imgReference.shape
    imgResult = cv2.warpPerspective(imgScan, h, (width, height))
       
    return imgResult, h
# returns:
# [0] imgResult <- aligned image
# [1] h <- homography

# params:
# src <- image to be cropped
# x, y <- origins
# w, h <- width, height
# padding <- padding, can be + or -
# replace_pad <- just repads the image; for replacing border artifacts; only for negative padding
def cropImageByOrigin(src, x, y, w, h, padding=0, replace_pad=False):
    p = padding
    if (replace_pad == True):
        b = abs(p)
        img = src[y-p:y+h+p, x-p:x+w+p].copy()
        padded = cv2.copyMakeBorder(img, b, b, b, b, cv2.BORDER_CONSTANT,value=[255,255,255])
        return padded
    else:
        return src[y-p:y+h+p, x-p:x+w+p].copy()
# returns:
# img

# params:
# src <- image to get connected components from
# min_ratio <- components such that component_area:src_area < min_ratio are not considered
# max_ratio <- components such that component_area:src_area > max_ratio are not considered
# get_labels <- if True, list of destination labeled images will also be returned
# sort_by <- list of int ranged 0 to 4 or:
#             cv2.CC_STAT_LEFT, cv2.CC_STAT_TOP, cv2.CC_STAT_WIDTH, cv2.CC_STAT_HEIGHT, cv2.CC_STAT_AREA;
#            sorts by these stats in ascending order. usually only works with 0 (sort by x)
# show <- if output of every process should be shown (default=False)
def getConnectedComponents(src, min_ratio, max_ratio, get_labels=False, sort_by=[], show=False):
    font = cv2.FONT_HERSHEY_SIMPLEX
      
    # gry = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    # thresh = cv2.adaptiveThreshold(gry,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
              # cv2.THRESH_BINARY,11,2)

    # invert image
    inv = cv2.bitwise_not(src)

    # copy src for output    
    mod = src.copy()

    # compute for min_area and max_area
    src_area = src.shape[0] * src.shape[1]
    min_area = src_area * min_ratio
    max_area = src_area * max_ratio

    # get 8-neighbor components with stats
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(inv, 8)

    # loop through each component and
    # weed out components not filling the criteria
    res = []
    lab = []
    for i in range(ret):
    # basic
        min_x = stats[i][0]
        min_y = stats[i][1]
        width = stats[i][2]
        height = stats[i][3]
        area = stats[i][4]

        # skip other unwanted components
        if (area <= min_area): continue
        if (area >= max_area): continue

        # derived
        max_x = min_x + width - 1
        max_y = min_y + height - 1

        mid_x = int(min_x + (width/2))
        mid_y = int(min_y + (height/2))

        # bounding boxes to components
        mod[min_y:max_y, min_x] = 125
        mod[min_y, min_x:max_x] = 125
        mod[min_y:max_y, max_x] = 125
        mod[min_y, min_x:max_x] = 125

        # append to res & lab
        res.append(stats[i])
        lab.append(labels[i])

        # for writing on mod
        n = len(res) - 1
        cv2.putText(mod, str(n), (mid_x,mid_y), font, 1, 125, 2)
        # print(i, n, stats[i])
    
    # assuming res and lab len are equal:
    # print("Labels length: {} Stats length: {}".format(len(lab), len(res)))
    zipped = list(zip(lab, res))

    # sort by the i-th element of the res list
    if (len(sort_by) > 0):
        for i in range(len(sort_by)):
            zipped.sort(key=lambda x:x[1][i]) 

    # unzip it back
    if (len(zipped) > 0):
        lab, res = zip(*zipped)

    # convert back to list
    lab = list(lab)
    res = list(res)

    # # sort res list
    # if (len(sort_by) > 0):
    #     for i in range(len(sort_by)):
    #         res.sort(key = lambda x:x[i])

    # write the new order from sorting to mod
    for i in range(len(res)):
        min_x = res[i][0]
        min_y = res[i][1]
        width = res[i][2]
        height = res[i][3]
        mid_x = int(min_x + (width/2))
        mid_y = int(min_y + (height/2))
        cv2.putText(mod, str(i), (mid_x,mid_y), font, 1, 125, 2)

    if (show == True):
        cv2.imshow("detected components", mod)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if (get_labels == True):
        return mod, res, lab
    else:
        return mod, res
# returns:
# [0] mod <- modified src where detected components are outlined
# [1] res <- list of components fulfilling the criteria

# reshape to square with sides s. 
# utilizes padding if src is not square to avoid distortion
# params:
# src <- img to be resized
# s <- w, h of returned square
def padResizeToSquare(src, s):
    h, w= src.shape[:2]

    if (w > h):
        p = int((w - h)/2)
        src = cv2.copyMakeBorder(src, p, p, 0, 0, cv2.BORDER_CONSTANT,value=[255,255,255])
    elif (w < h):
        p = int((h - w)/2)
        src = cv2.copyMakeBorder(src, 0, 0, p, p, cv2.BORDER_CONSTANT,value=[255,255,255])

    src = cv2.resize(src, (s, s))
    return src
# returns:
# img

# params:
# img <- img to be processed
# show <- if output of every process should be shown (default=False)
def preprocessImage(img, show=False):
    if (show == True):
        cv2.imshow("original img", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # clear spots that may be highlighted in adapted thresholding
        _, img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
        
        cv2.imshow("img after binary thresholding", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # remove possible shadows (?)
        img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        cv2.imshow("img after adaptive thresholding", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # remove small black points
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, (3,3))

        cv2.imshow("img after closing", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        # remove "holes"
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, (3,3))

        cv2.imshow("img after opening", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif (show == False):
        # clear spots that may be highlighted in adapted thresholding
        _, img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
        # remove possible shadows (?)
        img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        # remove small black points
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, (3,3))
        # remove "holes"
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, (3,3))

    return img
# returns:
# img <- modified img

# fn to process a single img
def processSingle(filename):
    filename = os.fsdecode(file)

    if (filename.endswith(".png") or filename.endswith(".jpg")):
        img = cv2.imread(img_filename, 0)

        paper_list = processPaper(img)

    return paper_list

# fn to process a whole dir of doc
# params:
# dir_batch <- folder where the batch of img are stored
def processBatch(dir_batch):
    batch = os.listdir(dir_batch)

    batch_list = []
    for file in batch:
        filename = os.fsdecode(file)
        
        if (filename.endswith(".png") or filename.endswith(".jpg")):
            img_filename = os.path.join(dir_batch, filename)
            img = cv2.imread(img_filename, 0)
            
            paper_list = processPaper(img)
            batch_list.append(paper_list)

    return batch_list
# returns:
# batch_list

# fn to process a single field extracted from paper img thru processSingle
# field <- img of field extracted
# min_ratio <- components such that component_area:src_area < min_ratio are not considered
# max_ratio <- components such that component_area:src_area > max_ratio are not considered
# show <- if output of every process should be shown (default=False)
def processField(field, min_ratio=0.0002, max_ratio=0.9, show=False):
    mod, stats = getConnectedComponents(field, min_ratio, max_ratio, sort_by=[0])

    field_list = []

    for i in range(len(stats)):
        x = stats[i][0]
        y = stats[i][1]
        w = stats[i][2]
        h = stats[i][3]

        character = cropImageByOrigin(field, x, y, w, h, padding=0)

        # character = cv2.medianBlur(character, 3)
        # _, character = cv2.threshold(character,127,255,cv2.THRESH_BINARY)

        # # # character = cv2.medianBlur(character, 3)
        # character = cv2.morphologyEx(character, cv2.MORPH_CLOSE, (3,3))
        # character = cv2.morphologyEx(character, cv2.MORPH_OPEN, (3,3))
        
        # character = sharpen(character)
        # should get the largest component and return it
        # should remove the noise 
        # _, character = getConnectedComponents(character, 0.5, 0.99)

        character = centerByMass(character, 20)

        # character = padResizeToSquare(character, 28)
        # character = cv2.cvtColor(character, cv2.COLOR_BGR2GRAY)

        if (show == True):
            cv2.imshow("character", character)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        field_list.append(character)

    return field_list
# returns:
# field_list <- list of components in field that satisfies the criteria

# fn to process a single paper
# paper <- img of paper, or path to img of paper
# min_ratio <- min ratio of component:paper area to consider, for getConnectedComponents
# max_ratio <- max ratio of component:paper area to consider, for getConnectedComponents
def processPaper(paper, min_ratio=0.0002, max_ratio=0.0060, show=False):
    paper = preprocessImage(paper)
    mod, stats = getConnectedComponents(paper, min_ratio, max_ratio)

    paper_list = []
    for i in range(len(stats)):
        x = stats[i][0]
        y = stats[i][1]
        w = stats[i][2]
        h = stats[i][3]

        field = cropImageByOrigin(paper, x, y, w, h, padding=-7, replace_pad=True)
        
        if (show == True):
            cv2.imshow("field", field)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        field_list = processField(field, show=show)
        paper_list.append(field_list)

    return paper_list
# returns:
# paper_list <- list of components in paper that satisfies the criteria

# ref:
# https://stackoverflow.com/questions/4993082/how-to-sharpen-an-image-in-opencv
# fn to sharpen image using unsharp mask
# img <- img to sharpen
# kernel_size <- tuple containing dim of kernel
# sigma <- for GaussianBlur
# amount <- higher value, sharper
# threshold <- for low contrast cases
def sharpen(image, kernel_size=(5,5), sigma=1.0, amount=1.0, threshold=0):
    blurred = cv2.GaussianBlur(image, kernel_size, sigma)

    sharpened = float(amount+1)*image-float(amount)*blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)

    if threshold > 0:
        low_contrast_mask = np.absolute(image-blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)

    return sharpened

# does nothing and only returns the input img if there are no contours found
# gets the largest contour, its center of mass, and 
# src <- to get center of mass from
# nsize <- size of input image after size normalization
# lsize <- size of the larger image input image will be centered
def centerByMass(src, nsize=20, lsize=28):
    # do this only if lsize is larger than nsize, duh
    if (lsize > nsize):
        # normalize input img
        img = padResizeToSquare(src, nsize)

        # invert color, then get contour
        img = cv2.bitwise_not(img)
        contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if (len(contours) != 0):
            # get the largest contour, the digit itself
            c = max(contours, key = cv2.contourArea)

            # make a mask and draw the contour on it
            mask = np.zeros(img.shape, np.uint8)
            cv2.drawContours(mask, [c], -1, (255), -1)

            # write it on a new img
            mod = cv2.bitwise_and(img, mask)
            mod = cv2.bitwise_not(mod)

            # get the center of mass of size normalized image
            n = cv2.moments(c)
            nX = int(n["m10"]/n["m00"])
            nY = int(n["m01"]/n["m00"])

            # # draw com of digit
            # cv2.circle(mod, (nX, nY), 1, (125), 1)
            # print("nX: "+str(nX)+" nY: "+str(nY))

            # cv2.imshow("mod", mod)
            # cv2.waitKey(0)

            # create white blank image 
            blank = np.zeros((lsize, lsize), np.uint8)
            blank[:] = 255

            # get its center
            lX = lY = int(sum(np.arange(lsize))//lsize)

            # get the difference of two images as offset
            dX = abs(lX - nX)
            dY = abs(lY - nY)

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
# sharpened <- sharpened img

# # use specific function instead
# # input model and character
# # model <- the model to read the character with
# # character <- img to be recognized
# def readCharacter(model, character):
#   character = character/255
#   character = np.expand_dims(character, axis=0)
#   character = np.expand_dims(character, axis=3)
#   character.reshape((1, 28, 28, 1))
#   predictions = model.predict(character)
#   predicted_value = str(np.argmax(predictions))

#   return predictions, predicted_value
# # returns:
# # predicted_value <- the most probable classification of the character

# if __name__ == "__main__":

#     # # NN
#     # import tensorflow as tf
#     # from model import formatDataset
#     # from tensorflow import keras   
#     # mean_px, std_px = formatDataset()
#     # models = [keras.models.load_model('./models/w_m'+str(i)+'_eF.h5') for i in range(10)]

#     # # kNN
#     # from lbpknn import createClassifier
#     # from lbpknn import getLocalBinaryPattern
#     # k5 = createClassifier("./knn_5.pkl")
#     # k10 = createClassifier("./knn_10.pkl")

#     scanned = "./in/v6/v6.png"  

#     scanned = cv2.imread(scanned, 0)

#     # clean character images
#     paper = processPaper(scanned, show=False)

#     for field in paper:
#         txt = ""
#         for character in field:
#             print("")

#             # for i in range(len(models)):
#             #     p, c = readCharacter(models[i], character)
#             #     print("Model #"+str(i)+" prediction: "+str(c))

#             p = k5.predict(getLocalBinaryPattern(character)[1].reshape(1, -1))[0] 
#             print("k=5 prediction: "+str(p))

#             p = k10.predict(getLocalBinaryPattern(character)[1].reshape(1, -1))[0] 
#             print("k=10 prediction: "+str(p))

#             cv2.imshow("character.png", character)
#             cv2.waitKey(0)
            
#         print(txt)

#     cv2.destroyAllWindows()

## to do:
# is input image in lbp inverted or not?
# normalized or not?
# M A K E  S U R E both test and train sets undergo the same processes
# do the same processes made on dataset
# add more attributes
# train KNN on sample data and (preprocessed) NIST

## to do:
# overhaul the fns
#   process:
#       - preprocess the image
#           > read as grayscale already
#           > align with template
#           > use adaptive thresholding
#           > use opening/closing
#           > get connected components as fields
#           > get connected components as characters
#           > reorder fields (hardcoded, probably?)
#       - predict
#           > use the model from SO
#           > ask how to add characters ".", ",", "/", "-"
#       - output
#           > output to csv
#   problems
#       - find better datasets to recognize other symbols too
#       - accuracy of model
#       - aligning and making sure fields are read in order
#       - account for documents taken with camera
# limit input as those from scanner
# test usability