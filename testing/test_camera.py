from trackers.realsense_tracker import RealsenseTracker
from src.vision.realsense import UsbRealsenseCamera, cv2

tracker = RealsenseTracker(tuple(x / 2 for x in UsbRealsenseCamera.shape()), True)

while True:
    print("CURRENT ERROR: ", tracker.get_error_vector(return_on_lost=[-999, -999]))
    cv2.waitKey(5)
