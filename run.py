import threading
import subprocess


def runCreator():
    with open('creator_log.txt', 'w') as outfile:
        subprocess.call('python job_creator.py', stdout=outfile)


def runSeeker():
    with open('seeker_log.txt', 'w') as outfile:
        subprocess.call('python job_seeker.py', stdout=outfile)


t1 = threading.Thread(target=runCreator)
t2 = threading.Thread(target=runSeeker)
t1.start()
t2.start()

