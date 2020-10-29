import json
import random


# Will save the list as a JSON file
def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=3)
    f.close()


# Will append an object to the JSON file
def append_json(add, filename='jobs.json'):
    with open(filename) as json_file:
        data = json.load(json_file)
        data.append(add)
    json_file.close()
    write_json(data, filename)
    json_file.close()


# Creating new Jobs and append to JSON file
def generate_jobs(number, jobFile='jobs.json', typeFile='job_type.JSON'):
    # Load Job Types
    with open(typeFile) as typeFile:
        types = json.loads(typeFile.read())
        # print("Starting number of job types: " + str(len(types)))
    typeFile.close()

    # Load Jobs
    with open(jobFile) as file:
        jobs = json.loads(file.read())
        num_jobs = len(jobs)
        # print("Number of jobs in file: " + str(num_jobs))
    file.close()

    for i in range(number):
        data = {
            "id": str(num_jobs + i),
            "job_type": random.randint(0, len(types) - 1),
            "size": random.randint(1, 5),
            "assigned": "0",
            "status": "New",
            "results": ""
        }
        append_json(data, jobFile)

    return num_jobs + number


def getRandJob(filename):
    with open(filename, 'r') as f:
        jobs = json.loads(f.read())
        random.shuffle(jobs)
        return jobs[0]


# Generate and return a random set of skills with random length
def generate_skills(filename='skills.txt', **kwargs):
    max_skills = kwargs.get('max_skills', None)
    if max_skills <= 0:
        max_skills = 1
    with open(filename) as f:
        lines = f.read().splitlines()
        if len(lines) == 0:
            return "No skills in file"
    random.shuffle(lines)
    num_lines = len(lines)
    if max_skills is not None and max_skills <= num_lines:
        return random.sample(lines, random.randint(1, max_skills))
    else:
        return random.sample(lines, random.randint(1, num_lines))
