import matplotlib
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation
from typing import List

matplotlib.use("WX")


class Plotter:
    def __init__(self, csv_files: List[str]):
        self.csv_names = csv_files

    def update_plot(self, *args, **kwargs):
        data = [pd.read_csv(x) for x in self.csv_names]

        x_values = data[0]["Time"]
        y_values = [#[d["input"] for d in data],
                    [d["P_x"] for d in data],
                    [d["I_x"] for d in data],
                    [d["D_x"] for d in data]]

        plt.cla()
        i = 0
        l = ["P", "I", "D"]
        colors = ['red', 'blue', 'green']
        for y_values in y_values:
            plt.plot(x_values, y_values[0], color=colors[i])
            i += 1
            #plt.plot(x_values, y_values[1])

        plt.xlabel("Time")
        plt.ylabel("Error")
        plt.title("PID")
        plt.gcf().autofmt_xdate()
        plt.tight_layout()

    def start(self):
        anim = FuncAnimation(plt.gcf(), self.update_plot)

        plt.tight_layout()
        plt.show()
