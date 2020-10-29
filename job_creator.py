from socket import *
import json

class creator:

    def __init__(self, port):
        self.creatorPort = int(port)
        self.start()
        self.creatorSocket.listen(1)
        print('Job-Creator is ready to recieve Job-Seeker')
        self.listen()

    #   Create the original socket
    def start(self):
        self.creatorSocket = socket(AF_INET, SOCK_STREAM)
        self.creatorSocket.bind(('',self.creatorPort))

    #   Listen for new job-seekers
    def listen(self):
        while True:
            connection, addr = self.creatorSocket.accept()
            print('\nSeeker ' + str(addr) + ' accepted at creator address ' + str(connection.getsockname()))

            #   Recieve services
            print('Services message received from job-seeker')
            self.decode(connection.recv(1024).decode())

            #   Send Job
            connection.send(self.encode(messageType=1, job='computational task'))
            print('Job message sent to job-seeker\n')

            #   Recieve accept
            print('Accept message received from job-seeker')
            self.decode(connection.recv(1024).decode())

            #   Send acknowledge
            connection.send(self.encode(messageType=2, acknowledge=True))
            print('Acknowledge message sent to job-seeker\n')

            #   Recieve completed
            print('Completed message received from job-seeker')
            self.decode(connection.recv(1024).decode())
            connection.close()

    #   Encode the message format
    #   messageType -The type of message being sent
    #   job         -The job
    #   acknowledge -Boolean for acknowledging the response from the seeker
    #   Returns the encoded message
    def encode(self, messageType, job='', acknowledge=True):
        message = {}    #!Temp dictionary

        #   Switch case for different message types
        if messageType == 1:
            #   Job message
            message =   {'header':messageType,
                        'job':job}
        else:
            #   Acknowledge message
            message =   {'header':messageType,
                        'acknowledge':acknowledge}

        messageEncoded = json.dumps(message).encode()
        return messageEncoded

    #   Decode the message from the seeker
    #   message -The message from the seeker
    def decode(self, message):
        messageDecoded = json.loads(message)
        for key in messageDecoded:
            print(key + ' : ' + str(messageDecoded.get(key)))
        print()

if __name__ == "__main__":
    creator(input('Enter port #:'))