from trackers.realsense_tracker import RealsenseTracker
from plotting.csv_writer import CsvWriter
from plotting.plotter import Plotter
from src.vision.realsense import UsbRealsenseCamera, cv2
from threading import Thread

tracker = RealsenseTracker(tuple(x / 2 for x in UsbRealsenseCamera.shape()), True)

csv_writer_x = CsvWriter("x")
csv_writer_y = CsvWriter("y")

p = Plotter([csv_writer_x.file_name, csv_writer_y.file_name])


def x():
    for i in range(0, 100):
        err = tracker.get_error_vector(return_on_lost=[0, 0])
        print("GO")
        csv_writer_x.update([0, 0, 0, 0, err[0], 0])
        csv_writer_y.update([0, 0, 0, 0, err[1], 0])

        print("CURRENT ERROR: ", err)


thread = Thread(target=x)
thread.start()
p.start()
