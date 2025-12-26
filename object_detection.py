import cv2
import numpy as np

# Load the pre-trained vehicle cascade classifier (you might need to find a good one)
#  A good source might be: https://github.com/opencv/opencv/tree/master/data/haarcascades
vehicle_cascade = cv2.CascadeClassifier(r'C:\Users\NITREXEE\Desktop\intelligent_traffic_system\haarcascade_car.xml')  # Replace with the actual path

def detect_vehicles_haar(frame):
    """
    Detects vehicles in a frame using Haar Cascades.

    Args:
        frame: The input frame (NumPy array).

    Returns:
        list: A list of bounding boxes [(x, y, w, h)] for detected vehicles.  Returns an empty list if no vehicles are found.
    """
    if vehicle_cascade.empty():
        print("Error: Haar cascade classifier not loaded!")
        return []

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    vehicles = vehicle_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(20, 20))
    return vehicles.tolist()  # Convert to a standard list

def detect_vehicles(frame): #Renamed the main detection function
  return detect_vehicles_haar(frame)

import cv2
import numpy as np

# Load YOLO
net = cv2.dnn.readNet(r"C:\Users\NITREXEE\Desktop\intelligent_traffic_system\yolov3.weights", r"C:\Users\NITREXEE\Desktop\intelligent_traffic_system\yolov3.cfg")  # Replace with your paths
classes = []
with open(r"C:\Users\NITREXEE\Desktop\intelligent_traffic_system\coco.names", "r") as f:  # Replace with your path
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
conf_threshold = 0.5
nms_threshold = 0.4

def detect_vehicles_yolo(frame):
    """
    Detects vehicles in a frame using YOLO.

    Args:
        frame: The input frame (NumPy array).

    Returns:
        list: A list of bounding boxes [(x, y, w, h)] for detected vehicles.
    """
    height, width, channels = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    boxes = []
    confidences = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > conf_threshold and classes[class_id] in ['car', 'truck', 'bus']:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))

    # Apply non-maximum suppression to remove redundant detections
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    final_boxes = [boxes[i] for i in indices] if indices is not None else []
    return final_boxes

def detect_vehicles(frame): #Renamed the main detection function
  return detect_vehicles_yolo(frame)