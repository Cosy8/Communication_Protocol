from socket import *
import json

class seeker:
    creatorName = '127.0.0.1'
    creatorPort = 12000

    def __init__(self):
        self.start()
    
    #   Connected to the job creator
    def start(self):
        try:
            self.seekerSocket = socket(AF_INET, SOCK_STREAM)
            self.seekerSocket.connect((self.creatorName,self.creatorPort))
            print('Connected to creator ' + str(self.creatorName) + ' at port ' + str(self.creatorPort))

            #   Send services
            self.seekerSocket.send(self.encode(messageType=1, services='services'))
            print('Message sent to job-creator')

            #   Recieve job
            self.decode(self.seekerSocket.recv(1024).decode())

            #   Send accept
            self.seekerSocket.send(self.encode(messageType=2, accept=True))
            print('Message sent to job-creator')

            #   Recieve acknowledge
            self.decode(self.seekerSocket.recv(1024).decode())

            #   Send completed
            self.seekerSocket.send(self.encode(messageType=3, job='computational task', status='Done', result='Satisfied'))
            print('Message sent to job-creator')
        except:
            print('***Connection to creator failed***')

    #   Encode the message format
    #   messageType -The type of message being sent
    #   services    -The seekers services available
    #   accept      -Boolean for accepting or declining a job
    #   job         -The job
    #   status      -The status of the job
    #   result      -The result of the job
    #   Returns the message as bytes
    def encode(self, messageType, services='', accept=True, job='', status='', result=''):
        message = {}    #!Temp dictionary

        #   Switch case for different message types
        if messageType == 1:
            #   Services message
            message =   {'header':messageType,
                        'services':services}
        elif messageType == 2:
            #   Accept message
            message =   {'header':messageType,
                        'Accept':accept}
        else:
            #   Completion message
            message =  {'header':messageType,
                        'job':job,
                        'status':status,
                        'result':result}

        messageEncoded = json.dumps(message).encode()
        return messageEncoded

    #   Decode the message from the creator
    #   message -The message from the creator
    def decode(self, message):
        messageDecoded = json.loads(message)
        for key in messageDecoded:
            print(key + ' : ' + str(messageDecoded.get(key)))
        print()

if __name__ == "__main__":
    seeker()