from realsense import UsbRealsenseCamera
import time
camera = UsbRealsenseCamera()
for i in range(5):
    print(camera.raw_photo())
    time.sleep(1)
