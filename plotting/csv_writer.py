import csv
import time
import pathlib

from datetime import datetime


class CsvWriter:
    rownames = ["Time", "P", "I", "D", "out", "input", "center_point"]

    def __init__(self, name: str):
        self.file_name = (
            str(pathlib.Path(__file__).parent.resolve())
            + "/data/"
            + datetime.now().strftime("%H:%M:%S")
            + "_"
            + name
        )

        with open(self.file_name, "a") as f:
            fw = csv.writer(f)
            fw.writerow(self.rownames)

        self.start_time = time.time()

    def update(self, values):
        assert len(values) == 6

        with open(self.file_name, "a") as f:
            fw = csv.writer(f)
            fw.writerow([1000 * (time.time() - self.start_time)] + values)
