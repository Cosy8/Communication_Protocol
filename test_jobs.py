from job_creator import creator
from job_seeker import seeker
import random

def test_scan_port():
    assert seeker().scanPort() == 1

def test_check_host():
    assert seeker().checkHost('www.stackoverflow.com') == 1

def test_TCP_flood_attack():
    assert seeker().SYN_TCP_Flood(dstIP='127.0.0.1', dstPort=random.randint(1000,9000), counter=5) == 1

def test_UDP_flood_attack():
    assert seeker().SYN_UDP_Flood(dstIP='127.0.0.1', dstPort=random.randint(1000,9000), counter=5) == 1