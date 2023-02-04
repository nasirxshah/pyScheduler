import time
from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import Callable, Dict, Tuple
import datetime as dt
import threading

@dataclass(slots=True, order=True)
class Task:
    when: float = field(default_factory=time.monotonic, compare=True)
    callback: Callable = field(compare=False, init=False)
    args: Tuple = field(default=(), compare=False)
    kwargs: Dict = field(default_factory=dict, compare=False)
    repeat:int = field(compare=False,default=0)
    steps:int = field(compare=False, init=False)
    counter :int = field(compare=False, default=0)
    threaded:bool = False

class Scheduler:
    def __init__(self) -> None:
        self.readyQueue: PriorityQueue[Task] = PriorityQueue()
        self.running: Task | None = None
    
    def do(self, callback, args=(), kwargs={}, threaded:bool = False):
        new_task = Task()
        new_task.when = time.monotonic()
        new_task.callback = callback
        new_task.args = args
        new_task.kwargs = kwargs
        new_task.threaded = threaded
        return Timer(new_task,self)

    def addTask(self, new_task):
        self.readyQueue.put(new_task)

    def run(self):
        while True:
            if self.running is not None:
                if self.running.threaded:
                    thread = threading.Thread(target=self.running.callback, args=self.running.args, kwargs=self.running.kwargs)
                    thread.start()
                else:
                    self.running.callback(*self.running.args,
                                      **self.running.kwargs)
                
                self.running.counter += 1
                if  self.running.repeat == -1 or self.running.repeat > self.running.counter:
                    self.running.when += self.running.steps
                    self.readyQueue.put(self.running)

                time.sleep(0)

            self.running = self.readyQueue.get()
            if self.running.when > time.monotonic():
                self.readyQueue.put(self.running)
                self.running = None
                time.sleep(0.1)


class Timer:
    def __init__(self,task:Task, scheduler:Scheduler) -> None:
        self.task = task
        self.scheduler = scheduler
        
    def at(self, when:str):
        h,m,s = when.split(":")
        tdelta = dt.datetime.combine(dt.date.today(),dt.time(int(h),int(m),int(s))) - dt.datetime.now()
        self.task.when = time.monotonic() + tdelta.total_seconds()

        self.scheduler.addTask(self.task)
        return Repeat(self.task)

    def now(self):
        self.task.when = time.monotonic()
        self.scheduler.addTask(self.task)
        return Repeat(self.task)

class Repeat:
    def __init__(self,task:Task) -> None:
        self.task = task

    def repeat(self, limit:int =-1):
        self.task.repeat = limit
        return Every(self.task)



class Every:
    def __init__(self,task:Task) -> None:
        self.task = task

    def every(self, interval=1):
        return Step(interval,self.task)

class Step:
    def __init__(self, interval, task:Task) -> None:
        self.interval = interval
        self.task = task

    def second(self):
        self.task.steps = 1*self.interval

    def minute(self):
        self.task.steps = 60*self.interval

    def hour(self):
        self.task.steps = 3600*self.interval

    def day(self):
        self.task.steps = 3600*24*self.interval
