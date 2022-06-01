from trackers.realsense_tracker import RealsenseTracker

tracker = RealsenseTracker((200, 296), True)
tracker.camera.measure_paddle(True)

while True:
    try:
        tracker.get_error_vector()
    except:
        print("OUT OF RANGE")
