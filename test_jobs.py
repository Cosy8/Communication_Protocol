from job_creator import creator
from job_seeker import seeker

def test_scan_port():
    assert seeker().scanPort() == 1

def test_check_host():
    assert seeker().checkHost('www.stackoverflow.com') == 1