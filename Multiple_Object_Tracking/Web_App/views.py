from django.shortcuts import render
import numpy as np
from matplotlib import pyplot as plt
import cv2
import sys
import time

def otsu_binary(img):
    """
    Otsu binarization function.
    :param img: Image to binarize - should be in greyscale.
    :return: Image after binarization.
    """
    # check if input image is in grayscale (2D)
    try:
        if img.shape[2]:
            # if there is 3rd dimension
            sys.exit('otsu_binary(img) input image should be in grayscale!')
    except IndexError:
        pass  # image doesn't have 3td dimension - proceed

    plt.close('all')
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    # find normalized_histogram, and its cumulative distribution function
    hist = cv2.calcHist([blur], [0], None, [256], [0, 256])
    hist_norm = hist.ravel() / hist.max()
    Q = hist_norm.cumsum()
    bins = np.arange(256)
    fn_min = np.inf
    thresh = -1

    for i in range(1, 255):
        p1, p2 = np.hsplit(hist_norm, [i])  # probabilities
        q1 = Q[i]
        q2 = Q[255] - q1  # cum sum of classes
        b1, b2 = np.hsplit(bins, [i])  # weights
        # finding means and variances
        m1 = np.sum(p1 * b1) / q1
        m2 = np.sum(p2 * b2) / q2
        v1, v2 = np.sum(((b1 - m1) ** 2) * p1) / q1, np.sum(
            ((b2 - m2) ** 2) * p2) / q2
        # calculates the minimization function
        fn = v1 * q1 + v2 * q2
        if fn < fn_min:
            fn_min = fn
            thresh = i
    # find otsu's threshold value with OpenCV function
    ret, otsu = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    print("{} {}".format(thresh, ret))

    ret, img_thresh1 = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)
    return img_thresh1

# img = cv2.imread('static/files/hardware.jpg')
# img_thresh1 = otsu_binary(img)
# titles = ['Original Image', 'BINARY']
#
#
# images = [img, img_thresh1]
# for i in range(2):
#     plt.subplot(1, 2, i + 1), plt.imshow(images[i], 'gray')
#     plt.title(titles[i])
#     plt.xticks([]), plt.yticks([])
# plt.show()


# list of all VideoCapture methods and attributes
# [print(method) for method in dir(cap) if callable(getattr(cap, method))]

cap = cv2.VideoCapture('static/files/small.avi')
ret, frame = cap.read()

print(ret)
print(cap.isOpened())


while(cap.isOpened()):
    ret, frame = cap.read()
    print(cap.read())
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    plt.imshow(gray)
    plt.show()

cap.release()
