# encoding: utf-8

import unittest
from myclass import MyClass


class MyTest(unittest.TestCase):  # 继承父类
    # 初始化工作
    def setUp(self):
        self.tclass = MyClass()  # 实例化了被测试模块中的类

    # 退出清理工作
    def tearDown(self):
        pass

    # 具体的测试用例，一定要以test开头
    def sametest(self, par, ret):
        print "test sum"
        self.assertEqual(self.tclass.sum(1, par), ret)

    def testsum(self):
        # self.assertEqual(self.tclass.sum(1, 2), 2)
        for i in [(1, 2), (2, 2), (3, 3)]:
            self.sametest(i[0], i[1])

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):  # ??
            s.split(2)

    def test_even(self):
        """
        Test that numbers between 0 and 5 are all even.
        """
        for i in range(0, 6):
            # with self.subTest(i=i):
            self.assertEqual(i % 2, 0)


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(MyTest)
    unittest.TextTestRunner(verbosity=2).run(suite)