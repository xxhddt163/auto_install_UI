'''
Author: xxh
coding: utf-8
Date: 2022-09-21 22:35:14
LastEditTime: 2022-09-25 12:32:28
FilePath: \PYQT\scripts\PriorityQueue.py
'''
import heapq


class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0     # 当优先级相同时 index值越低优先弹出

    def push(self, item: str, priority: int):
        heapq.heappush(self._queue,(priority, self._index, item))      
        self._index += 1
        
    def pop(self):
        return heapq.heappop(self._queue)[-1]           # 弹出优先级最低的元素
    
    def to_list(self):
        return [self.pop() for _ in range(len(self._queue))]