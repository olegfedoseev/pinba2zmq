#!/usr/bin/env python
"""Auto-generated unit tests."""

import unittest
import Pinba


class Test_Pinba(unittest.TestCase):
    def testRequest_Basics(self):
        pb = Pinba.Request()

        pb.hostname = u'1'
        self.assertEquals(u'1', pb.hostname)

        pb.server_name = u'2'
        self.assertEquals(u'2', pb.server_name)

        pb.script_name = u'3'
        self.assertEquals(u'3', pb.script_name)

        pb.request_count = 4
        self.assertEquals(4, pb.request_count)

        pb.document_size = 5
        self.assertEquals(5, pb.document_size)

        pb.memory_peak = 6
        self.assertEquals(6, pb.memory_peak)

        pb.request_time = 7.0
        self.assertEquals(7.0, pb.request_time)

        pb.ru_utime = 8.0
        self.assertEquals(8.0, pb.ru_utime)

        pb.ru_stime = 9.0
        self.assertEquals(9.0, pb.ru_stime)

        pb.timer_hit_count = (10,)
        self.assertEquals((10,), pb.timer_hit_count)

        pb.timer_value = (11.0,)
        self.assertEquals((11.0,), pb.timer_value)

        pb.timer_tag_count = (12,)
        self.assertEquals((12,), pb.timer_tag_count)

        pb.timer_tag_name = (13,)
        self.assertEquals((13,), pb.timer_tag_name)

        pb.timer_tag_value = (14,)
        self.assertEquals((14,), pb.timer_tag_value)

        pb.dictionary = (u'15',)
        self.assertEquals((u'15',), pb.dictionary)

        pb.status = 16
        self.assertEquals(16, pb.status)

        pb2 = Pinba.Request()
        pb2.ParseFromString(pb.SerializeToString())

        self.assertEquals(pb.hostname, pb2.hostname)
        self.assertEquals(pb.server_name, pb2.server_name)
        self.assertEquals(pb.script_name, pb2.script_name)
        self.assertEquals(pb.request_count, pb2.request_count)
        self.assertEquals(pb.document_size, pb2.document_size)
        self.assertEquals(pb.memory_peak, pb2.memory_peak)
        self.assertEquals(pb.request_time, pb2.request_time)
        self.assertEquals(pb.ru_utime, pb2.ru_utime)
        self.assertEquals(pb.ru_stime, pb2.ru_stime)
        self.assertEquals(pb.timer_hit_count, pb2.timer_hit_count)
        self.assertEquals(pb.timer_value, pb2.timer_value)
        self.assertEquals(pb.timer_tag_count, pb2.timer_tag_count)
        self.assertEquals(pb.timer_tag_name, pb2.timer_tag_name)
        self.assertEquals(pb.timer_tag_value, pb2.timer_tag_value)
        self.assertEquals(pb.dictionary, pb2.dictionary)
        self.assertEquals(pb.status, pb2.status)


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(Test_Pinba))
    return suite
