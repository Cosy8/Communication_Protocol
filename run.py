import threading
import subprocess


def runCreator():
    with open('creator_log.txt', 'w') as outfile:
        with open('creator_in.txt', 'r') as infile:
            subprocess.call('python job_creator.py', stdout=outfile, stdin=infile)


def runSeeker():
    with open('seeker_log.txt', 'w') as outfile:
        with open('seeker_in.txt', 'r') as infile:
            subprocess.call('python job_seeker.py', stdout=outfile, stdin=infile)


t1 = threading.Thread(target=runCreator)
t2 = threading.Thread(target=runSeeker)
t1.start()
t2.start()

