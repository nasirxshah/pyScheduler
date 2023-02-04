from scheduler import Scheduler
import time

def mytask(id):
    print(f'Task/{id} is running')

def heavytask(id):
    print(f'Task/{id} is running')
    time.sleep(3)


sched = Scheduler()


sched.do(mytask,args=(1,)).now().repeat().every().second()
sched.do(heavytask,args=(2,), threaded=True).now().repeat().every().second()

sched.run()