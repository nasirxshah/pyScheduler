# pyscheduler
A lightweight and fast python task scheduling library without any 3rd party dependency.

## Usage

```python
from scheduler import Scheduler

def mytask(id):
    print(f'Task/{id} is running')


def schedule_another_task(id):
    sched.do(mytask,args=(id,)).now().repeat().every(1).second()

sched = Scheduler()

sched.do(mytask,args=(1,)).now()
sched.do(mytask,args=(2,)).at("20:55:45").repeat(3).every(2).second()
sched.do(mytask,args=(3,)).at("20:55:45").repeat().every(5).second()
sched.do(mytask,args=(4,)).at("20:55:45").repeat().every().minute()
sched.do(schedule_another_task, args=(5,)).now()
sched.run()


```