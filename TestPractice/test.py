import unittest
from next_day import NextDay
from triangle import triangle

class MyTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_nextday(self):
        ret = NextDay(2020,5,30)
        self.assertEqual(ret, [2020,5,31])

    def test_triangle(self):
        ret = triangle(2,2,2)
        self.assertEqual(ret, "Yes: Equilateral")


if __name__ == '__main__':
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(MyClassTest('test_nextday'))
    suite.addTest(MyClassTest('test_triangle'))
    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)