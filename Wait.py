import time
import sys

def wait_time(seconds):
    start = time.time()
    while time.time() - start < float(seconds):
        print 'wait'
        time.sleep(float(seconds)/10)
    # time.sleep(float(seconds))
    print 'Done'

if __name__=="__main__":
    waittime = sys.argv[1]
    print waittime
    #wait_time(waittime)