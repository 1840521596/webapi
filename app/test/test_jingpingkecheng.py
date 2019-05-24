#!/usr/bin/python
#-*-coding:utf-8 -*-
import unittest
class wc(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print "setUpClass\n"

    def test_1_a(self):
        print "test_1_a\n"
    def test_2_b(self):
        print "test_2_b\n"
    @classmethod
    def tearDownClass(self):
        """测试结束后执行,断言Req==Resp
        :return:  True OR False"""
        print "tearDownClass\n"
if __name__ == "__main__":
    unittest.main()