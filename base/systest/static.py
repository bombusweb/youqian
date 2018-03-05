# -*- coding: utf-8 -*-
from widget import Widget
import unittest
#执行测试的类
class WidgetTestCase(unittest.TestCase):
    def runTest(self):
        widget = Widget()
        self.assertEqual(widget.getSize(), (40, 40))
#测试
if __name__ == "__main__":
    testCase = WidgetTestCase()
    testCase.runTest()