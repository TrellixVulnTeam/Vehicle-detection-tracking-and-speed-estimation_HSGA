# USAGE
# python object_tracker.py --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel

# import the necessary packages
import cv2
from pyimagesearch.centroidtracker import CentroidTracker
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
	help="path to Tensorflow 'deploy' prototxt file")
ap.add_argument("-m", "--inference_model", required=True,
	help="path to trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# initialize our centroid tracker and frame dimensions
ct = CentroidTracker()
(H, W) = (None, None)

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromTensorflow(args["inference_model"], args["prototxt"])

# initialize the video stream and allow the camera sensor to warmup
print("[INFO] starting video stream...")
image = cv2.imread("image3.jpg")
time.sleep(2.0)

# loop over the frames from the video stream


	# read the next frame from the video stream and resize it
	
	

	# if the frame dimensions are None, grab them
if W is None or H is None:
	(H, W) = image.shape[:2]

	# construct a blob from the frame, pass it through the network,
	# obtain our output predictions, and initialize the list of
	# bounding box rectangles
blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
	(104.0, 177.0, 123.0))
net.setInput(blob)
detections = net.forward()
rects = []

# loop over the detections
for i in range(0, detections.shape[2]):
	# filter out weak detections by ensuring the predicted
	# probability is greater than a minimum threshold
	if detections[0, 0, i, 2] > args["confidence"]:
		# compute the (x, y)-coordinates of the bounding box for
		# the object, then update the bounding box rectangles list
		box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
		rects.append(box.astype("int"))

		# draw a bounding box surrounding the object so we can
		# visualize it
		(startX, startY, endX, endY) = box.astype("int")
		cv2.rectangle(image, (startX, startY), (endX, endY),
			(0, 255, 0), 2)

# update our centroid tracker using the computed set of bounding
# box rectangles
objects = ct.update(rects)

# loop over the tracked objects
for (objectID, centroid) in objects.items():
	# draw both the ID of the object and the centroid of the
	# object on the output frame
	text = "ID {}".format(objectID)
	cv2.putText(image, text, (centroid[0] - 10, centroid[1] - 10),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.circle(image, (centroid[0], centroid[1]), 4, (0, 0, 255), -1)

# show the output frame
cv2.imshow("frame", image)
time.sleep(5.0)
cv2.imwrite('tracked_image2.jpg',image)
cv2.waitKey(1)

# if the `q` key was pressed, break from the loop


# do a bit of cleanup

