from src.vision.realsense import UsbRealsenseCamera
import argparse
import time


DEFAULT_TEST_TIME = 5.0

parser = argparse.ArgumentParser(description="Mode manager")
parser.add_argument("--test_time", action="store", type=float, default=DEFAULT_TEST_TIME)
args = parser.parse_args()

test_time = args.test_time

print(f"MEASURING PERFORMANCE WITH TEST_TIME: {test_time}")

camera = UsbRealsenseCamera()
test_functions = [camera.take_photo, camera.object_position]

def measure_performance(test_time, function):
    counter = 0
    test_start_time = time.time()
    while time.time() - test_start_time <= test_time:
        function()
        counter += 1
    return counter

for function in test_functions:
    print("testing: ", function)
    counter = measure_performance(test_time, function)
    print(f"function: {function.__name__}, amount of calls: {counter}, avg amount of calls: {counter/test_time}")