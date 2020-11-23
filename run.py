import threading
import subprocess
import unit_test as UT
import random
import string
import os


# generateCreatorFile will create the creator_in.txt file that contains the test data for the job_creator.py file
# portnumber - is the port for the connection
# seekers - is the number of seekers the server will iterate through
def generateCreatorFile(portnumber, seekers):
    # open the creator's test case file
    with open('creator_in.txt', 'w') as f:
        f.write(str(portnumber))
        # if the seeker's test case file exists delete it (this is to eliminate any issues if the program is run
        # repeatedly)
        if os.path.exists('seeker_in.txt'):
            os.remove('seeker_in.txt')
        # create enough jobs for every seeker that will connect
        UT.generate_jobs(seekers)
        for i in range(seekers):
            f.write('\n')
            # select a random job from list and append to creator's dummy data
            job = UT.getRandJob('jobs.json')
            f.write(str(job))
            # Create seeker data
            generateSeekerFile(portnumber, job['id'])
        f.close()
    return seekers


# generateSeekerFile will create the seeker_in.txt file that contains the test data for the job_seeker.py file
# portnumber - is the port for the connection
# id - is the id for the job they are going to be offered
def generateSeekerFile(portnumber, id):
    # open the seekers' test case file
    with open('seeker_in.txt', 'a') as f:
        f.write(str(portnumber))
        f.write('\n')
        # add a list of random skills
        f.write(str(UT.generate_skills(max_skills=4)))
        f.write('\n')
        # generate random data (following our protocol format)
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


# generateCases will select a random port number and will create random test cases
def generateCases():
    portNumber = random.randint(1000, 9999)
    return generateCreatorFile(portNumber, random.randint(1, 7))


# will run the job_creator script, redirecting its input to the generated data and the output to a log file
def runCreator():
    with open('creator_log.txt', 'a') as outfile:
        with open('creator_in.txt', 'r') as infile:
            subprocess.call('python job_creator.py', stdout=outfile, stdin=infile)


# will run the job_seeker script, redirecting its input to the generated data and the output to a log file
def runSeeker():
    with open('seeker_log.txt', 'a') as outfile:
        with open('seeker_in.txt', 'r') as infile:
            subprocess.call('python job_seeker.py', stdout=outfile, stdin=infile)


# generate random test cases
numSeekers = generateCases()
# start server subprocess
t1 = threading.Thread(target=runCreator)
t1.start()
# iterate through and create a subprocess for each seeker (waiting for one to complete before the next is created)
for i in range(numSeekers):
    t2 = threading.Thread(target=runSeeker)
    t2.start()
    t2.join()
