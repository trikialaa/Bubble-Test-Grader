# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 19:52:52 2020

@author: alaa_
"""

# import the necessary packages
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import imutils
import cv2
from math import sqrt, floor

# Import image
cv2.namedWindow("output", cv2.WINDOW_NORMAL)
img = cv2.imread("template.jpg")

NUM_QUESTIONS = 25
ANSWER_KEY = {0: [0], 1: [4], 2: [0], 3: [3,4], 4: [1], 5: [4]}

# Apply conversion to grayscale and blur
warped = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
warped = cv2.GaussianBlur(warped, (5, 5), 0)

# Create binary image
thresh = cv2.threshold(warped, 0, 255,
	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# Define the borders of both inscription number area and answers area
# format = [x y w h]
(height, width) = warped.shape

INS_NUM_AREA = [width*0.14, height*0.175, width*0.25, height*0.165]
ANSWERS_AREA = [0, height*0.32, width, height*0.68]

# Find contours in the thresholded image
cnts = cv2.findContours(thresh.copy(), cv2.RETR_TREE,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# loop over the contours

INS_NUM_Cnts = []
ANSWERS_Cnts = []
    
previous_ins_cnt = [0, 0]
previous_ans_cnt = [0, 0]

ins_thresh = 3
ans_thresh = 8

for c in cnts:
	# Get coordinatees 
    (x, y, w, h) = cv2.boundingRect(c)
    # Define restrictions for dimensions
    if w >= 35 and h >= 35 and w <= 70 and h <= 70:
        # Case 1: Inscription number area
        if x >= INS_NUM_AREA[0] and x <= INS_NUM_AREA[0]+INS_NUM_AREA[2] and y >= INS_NUM_AREA[1] and y <= INS_NUM_AREA[1]+INS_NUM_AREA[3]:
            if sqrt( (x-previous_ins_cnt[0])**2 + (y-previous_ins_cnt[1])**2  ) >= ins_thresh:
#                cv2.drawContours(img, c, -1, (255, 0, 0), 5);
                INS_NUM_Cnts.append(c)
                previous_ins_cnt = [x, y]
        # Case 2: Answers area
        elif x >= ANSWERS_AREA[0] and x <= ANSWERS_AREA[0]+ANSWERS_AREA[2] and y >= ANSWERS_AREA[1] and y <= ANSWERS_AREA[1]+ANSWERS_AREA[3]:
            if sqrt( (x-previous_ans_cnt[0])**2 + (y-previous_ans_cnt[1])**2  ) >= ans_thresh:
#                cv2.drawContours(img, c, -1, (0, 0, 255), 5)
                ANSWERS_Cnts.append(c)
                previous_ans_cnt = [x, y]

detected_ins_num = ''

INS_NUM_Cnts = contours.sort_contours(INS_NUM_Cnts, method="left-to-right")[0]

for (q, i) in enumerate(np.arange(0, len(INS_NUM_Cnts), 10)):
    cnts = contours.sort_contours(INS_NUM_Cnts[i:i + 10], method="top-to-bottom")[0]
    bubbled = None
    for (j, c) in enumerate(cnts):
        mask = np.zeros(thresh.shape, dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1)
        mask = cv2.bitwise_and(thresh, thresh, mask=mask)
        total = cv2.countNonZero(mask)
        if bubbled is None or total > bubbled[0]:
            bubbled = (total, j)
    detected_ins_num += str(bubbled[1])

print('INSCRIPTION NUM: ' + detected_ins_num)


ANSWERS_Cnts = contours.sort_contours(ANSWERS_Cnts, method="top-to-bottom")[0]

for (q, i) in enumerate(np.arange(0, len(ANSWERS_Cnts), 5)):
    cnts = contours.sort_contours(ANSWERS_Cnts[i:i + 5])[0]
    true_q = 25 * (q % 4) + floor(q / 4)
    if true_q in ANSWER_KEY:
        k = ANSWER_KEY[true_q]
        answer = True
        for (j, c) in enumerate(cnts):
            mask = np.zeros(thresh.shape, dtype="uint8")
            cv2.drawContours(mask, [c], -1, 255, -1)
            mask = cv2.bitwise_and(thresh, thresh, mask=mask)
            total = cv2.countNonZero(mask)
            if j in k:
                if total > 1000:
                    cv2.drawContours(img, [c], -1, (0,255,0), 3)
                else:
                    cv2.drawContours(img, [c], -1, (0,0,255), 3)
                    answer = False
            else:
                if total > 1000:
                    cv2.drawContours(img, [c], -1, (0,0,255), 3)
                    answer = False
cv2.imshow("output",img)
cv2.imwrite('out.png', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)
