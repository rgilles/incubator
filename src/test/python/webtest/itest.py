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
import unittest
from hamcrest import assert_that, is_
from web import uri, request

__author__ = 'Romain Gilles'

class ITest(unittest.TestCase):

    def test_hello_word_get(self):
        target = uri("http://localhost:8080/hello/tutu")
        response = request(target)
        assert_that(response.status_code, is_(200))

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(ITest)
