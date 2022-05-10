from typing import Dict, List
import timeit
from collections import defaultdict


class Timer:
    def __init__(self):
        self.times: Dict[str, List[List[float]]] = defaultdict(list)
        self.start_time: int = -1
        self.stop_time: int = -1

    def is_on(self):
        return self.start_time != -1

    def is_stopped(self):
        return self.stop_time != -1

    def start(self):
        self.start_time = timeit.default_timer()

    def add_start(self, name: str):
        self.times[name].append([timeit.default_timer()])

    def add_stop(self, name: str):
        n = len(self.times[name]) - 1
        assert n >= 0
        self.times[name][n].append(timeit.default_timer())

    def stop(self):
        self.stop_time = timeit.default_timer()

    def summary(self):
        try:
            total_time = self.stop_time - self.start_time
            times = [
                (name, [t[1] - t[0] for t in self.times[name]])
                for name, t in self.times.items()
            ]

            mean_loop_time = 0.0

            for i in range(len(times)):
                mean_loop_time += sum([l[i] for _, l in times])

            mean_loop_time /= len(times)

            print(f"Total time elapsed: {total_time * 1000.0} ms")
            print(f"Section mean times: {[(name, sum(l)/len(l)) for name, l in times]}")
            print(f"Total mean time: {mean_loop_time}")
        except:
            print(
                "This cant be!, probably records are incomplete, error occured during the summary."
            )
