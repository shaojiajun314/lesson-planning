from education.celery import app
import time


@app.task
def hello_world(a):
    print a
    print 2837837198713897183
    time.sleep(10)
    print '*'*20
    print('Hello World', 123)
    return 'asdadadadads'
