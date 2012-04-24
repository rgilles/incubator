#
# Copyright 2012 Romain Gilles
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from web.assertion import iterable, is_class, IllegalArgumentError, raise_illegal_argument, assert_that_argument_is_not_none, assert_that_argument_type_is

__author__ = 'Romain Gilles'

import unittest


def generator_method():
    yield None

class AClass:
    pass

class AssertionTest(unittest.TestCase):

    def test_iterable_with_built_in_type_sequence(self):
        self.assertTrue(iterable(str))
        self.assertTrue(iterable(tuple))
        self.assertTrue(iterable(list))
        self.assertTrue(iterable(range))
        self.assertTrue(iterable(dict))

    def test_iterable_with_generator(self):
        self.assertTrue(iterable(generator_method()))

    def test_is_class_with_built_in_type(self):
        self.assertTrue(is_class(str))
        self.assertTrue(is_class(int))
        self.assertTrue(is_class(float))
        self.assertTrue(is_class(tuple))
        self.assertTrue(is_class(dict))
        self.assertTrue(is_class(range))
        self.assertTrue(is_class(bool))

    def test_raise_illegal_argument(self):
        self.assertRaises(IllegalArgumentError, raise_illegal_argument, "illegal arg message")

    def test_assert_that_argument_is_not_none(self):
        self.assertRaises(IllegalArgumentError, assert_that_argument_is_not_none, None, "argument_name")
        try:
            assert_that_argument_is_not_none("Not none param", "argument_name")
        except IllegalArgumentError:
            self.fail("no error must be raised on not None parameter")

    def test_assert_that_argument_type_is(self):
        self.assertRaises(IllegalArgumentError, assert_that_argument_type_is, None, str, "argument_name" )
        try:
            assert_that_argument_type_is("", str, "argument_name")
        except IllegalArgumentError:
            self.fail("no error must be raised when we test if the type of an string is str")

def suite():
#    tests = ['test_default_size', 'test_resize']

#    return unittest.TestSuite(map(WidgetTestCase, tests))
    return unittest.TestLoader().loadTestsFromTestCase(AssertionTest)

if __name__ == '__main__':
    unittest.main()
