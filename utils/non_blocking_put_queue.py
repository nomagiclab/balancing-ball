from time import monotonic as time
from queue import Queue
from collections import deque

class NonBlockingPutQueue(Queue):
    def put(self, item, block=True, timeout=None):
        with self.not_full:
            self._put(item)
            self.unfinished_tasks += 1
            self.not_empty.notify()

    def _init(self, maxsize):
        self.queue = deque(maxlen=maxsize)