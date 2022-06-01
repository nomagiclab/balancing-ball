from typing import List

from matplotlib import pyplot as plt


class PlotMaker:
    def __init__(self, labels: List[str]):
        self.data = {label: ([], []) for label in labels}

    def add(self, label, x, y):
        self.data[label][0].append(x)
        self.data[label][1].append(y)

    def __plot(self, p, labels):
        for label in labels:
            p.plot(self.data[label][0], self.data[label][1], label=label)

    def plot(self):
        self.__plot(plt, self.data.keys())
        plt.legend()
        plt.show()

    def plot_subplots(
        self,
        labels: List[List[str]],
        title=None,
        titles: List[str] = None,
        ylabels: List[str] = None,
    ):
        n_subplots = len(labels)
        fig, axs = plt.subplots(n_subplots)
        if title is not None:
            fig.suptitle(title)
        for i in range(n_subplots):
            if titles is not None:
                axs[i].set_title(titles[i])
            if ylabels is not None:
                axs[i].set_ylabel(ylabels[i])
            self.__plot(axs[i], labels[i])
        plt.show()
