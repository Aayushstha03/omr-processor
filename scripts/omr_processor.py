# import the necessary packages
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import imutils
import cv2
import pandas as pd


def getSheetData(image_path):
	# load the image, convert it to grayscale, blur it
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Scale down the image to a max height of 800 pixels
    max_height = 800
    height, width = image.shape[:2]
    if height > max_height:
        scaling_factor = max_height / float(height)
        image = cv2.resize(image, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
        gray = cv2.resize(gray, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
        blurred = cv2.resize(blurred, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

    # * thresholding the image and binarizing it
    # apply Otsu's thresholding method to binarize the warped
    # piece of paper
    thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    # cv2.imshow("thresh", thresh)
    # cv2.waitKey(0)
    cv2.destroyAllWindows

    # * finding contours or circles now
    # find contours in the thresholded image, then initialize
    # the list of contours that correspond to questions
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    detectedCnts = []
    # loop over the contours
    for c in cnts:
        # compute the bounding box of the contour, then use the
        # bounding box to derive the aspect ratio
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)
        # in order to label the contour as a question, region
        # should be sufficiently wide, sufficiently tall, and
        # have an aspect ratio approximately equal to 1
        if w >= 13 and h >= 13 and ar >= 0.9 and ar <= 1.1:
            detectedCnts.append(c)

    # Keep only the first 5 and last 20 circles
    detectedCnts = detectedCnts[:5] + detectedCnts[-20:]

    # Sort all 25 detected circles top-to-bottom
    sorted_cnts = contours.sort_contours(detectedCnts, method="top-to-bottom")[0]

    # The first 5 bubbles are the set identification bubbles (left to right)
    set_bubbles = contours.sort_contours(sorted_cnts[:5], method="left-to-right")[0]

    # Extract the remaining 20 answer bubbles
    answer_bubbles = sorted_cnts[5:]

    # Step 2: Split into rows (assuming correct detection of 8-8-4 structure)
    row1 = answer_bubbles[:8]   # First 8 bubbles (Row 1)
    row2 = answer_bubbles[8:16] # Next 8 bubbles (Row 2)
    row3 = answer_bubbles[16:]  # Last 4 bubbles (Row 3)

    # Step 3: Sort each row from left to right
    sorted_row1 = contours.sort_contours(row1, method="left-to-right")[0]
    sorted_row2 = contours.sort_contours(row2, method="left-to-right")[0]
    sorted_row3 = contours.sort_contours(row3, method="left-to-right")[0]

    # Step 4: Rearrange into final order (grouping based on your description)
    final_sorted_answer_cnts = (
        sorted_row1[:4] +  # First 4 from Row 1
        sorted_row1[4:] +  # Last 4 from Row 1
        sorted_row2[:4] +  # First 4 from Row 2
        sorted_row2[4:] +  # Last 4 from Row 2
        sorted_row3        # All 4 from Row 3
    )

    # Now `set_bubbles` has the correctly ordered set identifier bubbles
    # and `final_sorted_answer_cnts` has the correctly ordered answer bubbles.
    toExport = []

    # Process the first group of 5 contours to identify the set
    bubbled = None
    for (j, c) in enumerate(set_bubbles):
        mask = np.zeros(thresh.shape, dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1)
        mask = cv2.bitwise_and(thresh, thresh, mask=mask)
        
        # check if detected set marks
        # cv2.imshow("mask", mask)
        # cv2.waitKey(0)
        cv2.destroyAllWindows

        total = cv2.countNonZero(mask)
        if bubbled is None or total > bubbled[0]:
            bubbled = (total, j)

    # Determine the set based on the marked bubble in the first group
    marked_set = bubbled[1]
    print(f"Marked set identified: {marked_set}")
    toExport.append(marked_set)

    # Process the remaining groups of 4 contours each
    for i in range(0, len(final_sorted_answer_cnts), 4):
        group = final_sorted_answer_cnts[i:i + 4]  # Get the next set of 4 bubbles
        bubbled = None  # Store the most filled bubble

        for j, c in enumerate(group):
            mask = np.zeros(thresh.shape, dtype="uint8")
            cv2.drawContours(mask, [c], -1, 255, -1)
            mask = cv2.bitwise_and(thresh, thresh, mask=mask)

            # Uncomment below lines to visualize each mask
            # cv2.imshow("Mask", mask)
            # cv2.waitKey(0)
            cv2.destroyAllWindows()

            total = cv2.countNonZero(mask)  # Count non-zero (filled) pixels
            if bubbled is None or total > bubbled[0]:
                bubbled = (total, j)  # Store the most filled bubble and index

        # Store the detected answer (index of the bubbled answer)
        
        toExport.append(bubbled[1])
    return toExport
  
    

    

# Convert the toExport list to a DataFrame
# df = pd.DataFrame(toExport, columns=["Marked Bubbles"])

# # Export the DataFrame to a CSV file
# df.to_csv("marked_bubbles.csv", index=False)

# print("Exported DataFrame to marked_bubbles.csv")