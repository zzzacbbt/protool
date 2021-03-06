import unittest
import HtmlTestRunner
from configparser import ConfigParser
from telnetlib import Telnet
import time
import os
import logging
from basedir import basedir
logging.basicConfig(level=logging.INFO)


class ProburnTestCase(unittest.TestCase):
    def setUp(self):
        global config
        config = ConfigParser()
        path = os.path.join(basedir, 'config.ini')
        config.read(path, encoding='utf-8')
        host = "192.168.100.1"
        user = "Silknet"
        password = "Silknet@dmin"
        global tn
        tn = Telnet(host, port=23)
        tn.read_until(b'login')
        tn.write(user.encode('ascii') + b"\n")
        tn.read_until(b'Password')
        tn.write(password.encode('ascii') + b"\n")

    def tearDown(self):
        time.sleep(1)
        tn.close()


    def test_MACburn(self):
        tn.write(b"echo 1 > /proc/tc3162/Mtd_Erase" + b"\n")
        time.sleep(1)
        tn.write(b"prolinecmd clear 1" + b"\n")
        comvalupper = config['produce']['MAC'].upper()
        comvallower = config['produce']['MAC'].lower()
        value = ''.join(comvalupper.split(':'))
        tn.write("sys mac {}\n".format(value).encode('ascii'))
        judge = "new mac addr = {}".format(comvallower)
        try:
            content = tn.read_until(judge.encode('ascii'), timeout=2).decode()
            logging.info(content)
        except EOFError:
            logging.info("read GPONSN error .....")
            time.sleep(100)
        time.sleep(100)
        self.assertIn(judge, content)

    def test_productclassburn(self):
        tn.write(b"echo 1 > /proc/tc3162/Mtd_Erase" + b"\n")
        comval = config['produce']['productclass']
        tn.write("prolinecmd productclass set {}\n".format(comval).encode('ascii'))

        judge = "buf is:{}".format(comval)
        try:
            content = tn.read_until(judge.encode('ascii'), timeout=2).decode()
            logging.info(content)
        except EOFError:
            logging.info("read GPONSN error .....")
            time.sleep(100)
        self.assertIn(judge, content)

    def test_OUIburn(self):
        tn.write(b"echo 1 > /proc/tc3162/Mtd_Erase" + b"\n")
        comvalupper = config['produce']['MAC'].upper()
        value = ''.join(comvalupper.split(':'))[:6]
        tn.write("prolinecmd manufacturerOUI set {}\n".format(value).encode('ascii'))

        judge = "buf is:{}".format(value)
        try:
            content = tn.read_until(judge.encode('ascii'), timeout=2).decode()
            logging.info(content)
        except EOFError:
            logging.info("read GPONSN error .....")
            time.sleep(100)
        self.assertIn(judge, content)

    def test_serialnumburn(self):
        tn.write(b"echo 1 > /proc/tc3162/Mtd_Erase" + b"\n")
        comvalupper = config['produce']['MAC'].upper()
        value = ''.join(comvalupper.split(':'))
        tn.write("prolinecmd serialnum set {}\n".format(value).encode('ascii'))

        judge = "buf is:{}".format(value)
        try:
            content = tn.read_until(judge.encode('ascii'), timeout=2).decode()
            logging.info(content)
        except EOFError:
            logging.info("read GPONSN error .....")
            time.sleep(100)
        self.assertIn(judge, content)

    def test_restoredefault(self):

        tn.write(b"echo 1 > /proc/tc3162/Mtd_Erase" + b"\n")
        tn.write(b"killall boa" + b"\n")
        tn.write(b"/userfs/bin/mtd write /userfs/romfile.cfg romfile" + b"\n")
        tn.write(b"prolinecmd restore default" + b"\n")
        judge = 'restore default success'
        try:
            content = tn.read_until(judge.encode('ascii'), timeout=2).decode()
            logging.info(content)
        except EOFError:
            logging.info("restore default .....")
            time.sleep(100)
        time.sleep(100)

        self.assertIn(judge, content)

    def test_createwan(self):
        tn.write(b"echo 1 > /proc/tc3162/Mtd_Erase" + b"\n")
        path = os.path.join(basedir, 'produce_Georgia(1.2).txt')
        with open(path, 'r') as fp:
            for line in fp:
                tn.write(line.encode("ascii") + b'\n')


if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='basedir'))


