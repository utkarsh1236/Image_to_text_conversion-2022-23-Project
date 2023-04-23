from collections import namedtuple
import pytesseract 
import argparse
import imutils 
import cv2 
import streamlit as st

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def cleanup_text(text):
	# strip out non-ASCII text so we can draw the text on the image
	# using OpenCV
	return "".join([c if ord(c) < 128 else "" for c in text]).strip()

# construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True,
# 	help="path to input image that we'll align to template")
# ap.add_argument("-t", "--template", required=True,
# 	help="path to input template image")
# args = vars(ap.parse_args())

# create a named tuple which we can use to create locations of the
# input document which we wish to OCR
OCRLocation = namedtuple("OCRLocation", ["id", "bbox",
	"filter_keywords"])

# define the locations of each area of the document we wish to OCR
OCR_LOCATIONS = [
	OCRLocation("name", (410, 70, 712, 77),
		[]),
	OCRLocation("phone", (63, 440, 159, 22),
		[]),
	OCRLocation("email", (65, 514, 313, 23),
		[]),
	OCRLocation("address", (63, 590, 324, 66),
		[]),
	OCRLocation("expertise", (87, 1034, 297, 302),
		[]),
	OCRLocation("languages", (56, 1400, 331, 194),
		[])
]

# load the input image and template from disk
# print("[INFO] loading images...")
# image = cv2.imread(args["image"])
# template = cv2.imread(args["template"])
# aligned = image

# initialize a results list to store the document OCR parsing results
# print("[INFO] OCR'ing document...")
# parsingResults = []
# # loop over the locations of the document we are going to OCR
# for loc in OCR_LOCATIONS:
# 	# extract the OCR ROI from the aligned image
# 	(x, y, w, h) = loc.bbox
# 	roi = aligned[y:y + h, x:x + w]
# 	# OCR the ROI using Tesseract
# 	rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
# 	text = pytesseract.image_to_string(rgb)

# 	# break the text into lines and loop over them
# 	for line in text.split("\n"):
# 		# if the line is empty, ignore it
# 		if len(line) == 0:
# 			continue
# 		# convert the line to lowercase and then check to see if the
# 		# line contains any of the filter keywords (these keywords
# 		# are part of the *form itself* and should be ignored)
# 		lower = line.lower()
# 		count = sum([lower.count(x) for x in loc.filter_keywords])
# 		# if the count is zero then we know we are *not* examining a
# 		# text field that is part of the document itself (ex., info,
# 		# on the field, an example, help text, etc.)
# 		if count == 0:
# 			# update our parsing results dictionary with the OCR'd
# 			# text if the line is *not* empty
# 			parsingResults.append((loc, line))

# # initialize a dictionary to store our final OCR results
# results = {}
# # loop over the results of parsing the document
# for (loc, line) in parsingResults:
# 	# grab any existing OCR result for the current ID of the document
# 	r = results.get(loc.id, None)
# 	# if the result is None, initialize it using the text and location
# 	# namedtuple (converting it to a dictionary as namedtuples are not
# 	# hashable)
# 	if r is None:
# 		results[loc.id] = (line, loc._asdict())
# 	# otherwise, there exists an OCR result for the current area of the
# 	# document, so we should append our existing line
# 	else:
# 		# unpack the existing OCR result and append the line to the
# 		# existing text
# 		(existingText, loc) = r
# 		text = "{}\n{}".format(existingText, line)
# 		# update our results dictionary
# 		results[loc["id"]] = [text, loc]

# loop over the results
# for (locID, result) in results.items():
# 	# unpack the result tuple
# 	(text, loc) = result
# 	# display the OCR result to our terminal
# 	print(loc["id"])
# 	print("=" * len(loc["id"]))
# 	print("{}\n\n".format(text))
# 	# extract the bounding box coordinates of the OCR location and
# 	# then strip out non-ASCII text so we can draw the text on the
# 	# output image using OpenCV
# 	(x, y, w, h) = loc["bbox"]
# 	clean = cleanup_text(text)
# 	# draw a bounding box around the text
# 	cv2.rectangle(aligned, (x, y), (x + w, y + h), (0, 255, 0), 2)
# 	# loop over all lines in the text
# 	for (i, line) in enumerate(text.split("\n")):
# 		# draw the line on the output image
# 		startY = y + (i * 70) + 40
# 		cv2.putText(aligned, line, (x, startY),
# 			cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 0, 255), 5)

with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.set_option('deprecation.showfileUploaderEncoding', False)
st.title("Extracting Information From Resumes")
resume = st.file_uploader("Upload image", type=["jpg", "png", "jpeg"], label_visibility="hidden")
from PIL import Image, ImageOps
if resume is None:
    st.text("Please upload an image file")
else:
    resume_image = cv2.imread(r'{}'.format(resume.name))
    st.image(cv2.cvtColor(resume_image, cv2.COLOR_BGR2RGB), use_column_width=True)
    aligned = resume_image
    parsingResults = []
    # loop over the locations of the document we are going to OCR
    for loc in OCR_LOCATIONS:
        # extract the OCR ROI from the aligned image
        (x, y, w, h) = loc.bbox
        roi = aligned[y:y + h, x:x + w]
        # OCR the ROI using Tesseract
        rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(rgb)

        # break the text into lines and loop over them
        for line in text.split("\n"):
            # if the line is empty, ignore it
            if len(line) == 0:
                continue
            # convert the line to lowercase and then check to see if the
            # line contains any of the filter keywords (these keywords
            # are part of the *form itself* and should be ignored)
            lower = line.lower()
            count = sum([lower.count(x) for x in loc.filter_keywords])
            # if the count is zero then we know we are *not* examining a
            # text field that is part of the document itself (ex., info,
            # on the field, an example, help text, etc.)
            if count == 0:
                # update our parsing results dictionary with the OCR'd
                # text if the line is *not* empty
                parsingResults.append((loc, line))

    # initialize a dictionary to store our final OCR results
    results = {}
    # loop over the results of parsing the document
    for (loc, line) in parsingResults:
        # grab any existing OCR result for the current ID of the document
        r = results.get(loc.id, None)
        # if the result is None, initialize it using the text and location
        # namedtuple (converting it to a dictionary as namedtuples are not
        # hashable)
        if r is None:
            results[loc.id] = (line, loc._asdict())
        # otherwise, there exists an OCR result for the current area of the
        # document, so we should append our existing line
        else:
            # unpack the existing OCR result and append the line to the
            # existing text
            (existingText, loc) = r
            text = "{}\n{}".format(existingText, line)
            # update our results dictionary
            results[loc["id"]] = [text, loc]
    for (locID, result) in results.items():
        (text, loc) = result 
        st.subheader(loc["id"].title())
        if loc["id"] in ["expertise",  "languages"]:
            lines = text.split('\n')
            for line in lines:
                st.write("{}".format(line))
        else:
            st.write("{}\n\n".format(text))
        st.divider() 
