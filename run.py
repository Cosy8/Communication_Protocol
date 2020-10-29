import threading
import subprocess
import unit_test as UT
import random
import string
import os


def generateCreatorFile(portnumber, seekers):
    with open('creator_in.txt', 'w') as f:
        f.write(str(portnumber))
        if os.path.exists('seeker_in.txt'):
            os.remove('seeker_in.txt')
        UT.generate_jobs(seekers)
        for i in range(seekers):
            f.write('\n')
            job = UT.getRandJob('jobs.json')
            f.write(str(job))
            generateSeekerFile(portnumber, job['id'])
        f.close()
    return seekers


def generateSeekerFile(portnumber, id):
    with open('seeker_in.txt', 'a') as f:
        f.write(str(portnumber))
        f.write('\n')
        f.write(str(UT.generate_skills(max_skills=4)))
        f.write('\n')
        if random.randint(0, 1) == 1:
            f.write("1")
            f.write('\n')
            f.write(id)
            f.write('\n')
            f.write("Complete")
            f.write('\n')
            f.write(''.join(random.choice(string.ascii_letters) for x in range(random.randint(3, 32))))
            f.write('\n')
        else:
            f.write("0")
            f.write('\n')
        f.close()


def generateCases():
    portNumber = random.randint(1000, 9999)
    return generateCreatorFile(portNumber, random.randint(1, 7))


def runCreator():
    with open('creator_log.txt', 'a') as outfile:
        with open('creator_in.txt', 'r') as infile:
            subprocess.call('python job_creator.py', stdout=outfile, stdin=infile)


def runSeeker():
    with open('seeker_log.txt', 'a') as outfile:
        with open('seeker_in.txt', 'r') as infile:
            subprocess.call('python job_seeker.py', stdout=outfile, stdin=infile)


numSeekers = generateCases()
t1 = threading.Thread(target=runCreator)
t1.start()
for i in range(numSeekers):
    t2 = threading.Thread(target=runSeeker)
    t2.start()
    t2.join()

