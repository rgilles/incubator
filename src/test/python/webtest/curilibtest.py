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
__author__ = 'romain.gilles'
import unittest
from hamcrest import assert_that, is_, not_none
from web import  set_request_handler, HTTP_GET, HTTP_PUT, HTTP_DELETE, curilib, HTTP_POST, HTTP_HEAD, HTTP_OPTIONS, HTTP_TRACE, HTTP_CONNECT
from web.curilib import main
from web.urilib import AbstractRequestHandler

GOOGLE_URL = "http://www.google.com/segment1?query=value#fragment"

original_print_method = curilib._print

def print_mock(response):
    pass


class RequestHandlerMock(AbstractRequestHandler):
    def __init__(self):
        self.parameters = None

    def request(self, uri, method=None, headers=None, body=None):
        self.parameters = (uri, method, body, headers)


class CuriMainTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        curilib._print = print_mock

    @classmethod
    def tearDownClass(cls):
        curilib._print = original_print_method

    def setUp(self):
        self.request_handler_mock = RequestHandlerMock()
        set_request_handler(self.request_handler_mock)

    def test_main_uri(self):
        global parameters
        main(GOOGLE_URL.split())
        assert_that(self.request_handler_mock.parameters, is_(not_none()))
        assert_that(str(self.request_handler_mock.parameters[0]), is_(GOOGLE_URL))
        assert_that(str(self.request_handler_mock.parameters[1]), is_(HTTP_GET))

    def test_main_uri_method(self):
        main(["-X", HTTP_PUT, GOOGLE_URL])
        assert_that(self.request_handler_mock.parameters, is_(not_none()))
        assert_that(str(self.request_handler_mock.parameters[0]), is_(GOOGLE_URL))
        assert_that(str(self.request_handler_mock.parameters[1]), is_(HTTP_PUT))
        main(["--request", HTTP_DELETE, GOOGLE_URL])
        assert_that(self.request_handler_mock.parameters, is_(not_none()))
        assert_that(str(self.request_handler_mock.parameters[0]), is_(GOOGLE_URL))
        assert_that(str(self.request_handler_mock.parameters[1]), is_(HTTP_DELETE))

    def test_main_uri_method_shortcut_get(self):
        main(["--get", GOOGLE_URL])
        assert_that(str(self.request_handler_mock.parameters[0]), is_(GOOGLE_URL))
        assert_that(str(self.request_handler_mock.parameters[1]), is_(HTTP_GET))

    def test_main_uri_method_shortcut_put(self):
        main(["--put", GOOGLE_URL])
        assert_that(str(self.request_handler_mock.parameters[0]), is_(GOOGLE_URL))
        assert_that(str(self.request_handler_mock.parameters[1]), is_(HTTP_PUT))

    def test_main_uri_method_shortcut_post(self):
        main(["--post", GOOGLE_URL])
        assert_that(str(self.request_handler_mock.parameters[0]), is_(GOOGLE_URL))
        assert_that(str(self.request_handler_mock.parameters[1]), is_(HTTP_POST))

    def test_main_uri_method_shortcut_head(self):
        main(["--head", GOOGLE_URL])
        assert_that(str(self.request_handler_mock.parameters[0]), is_(GOOGLE_URL))
        assert_that(str(self.request_handler_mock.parameters[1]), is_(HTTP_HEAD))

    def test_main_uri_method_shortcut_delete(self):
        main(["--del", GOOGLE_URL])
        assert_that(str(self.request_handler_mock.parameters[0]), is_(GOOGLE_URL))
        assert_that(str(self.request_handler_mock.parameters[1]), is_(HTTP_DELETE))

    def test_main_uri_method_shortcut_options(self):
        main(["--opts", GOOGLE_URL])
        assert_that(str(self.request_handler_mock.parameters[0]), is_(GOOGLE_URL))
        assert_that(str(self.request_handler_mock.parameters[1]), is_(HTTP_OPTIONS))

    def test_main_uri_method_shortcut_trace(self):
        main(["--trace", GOOGLE_URL])
        assert_that(str(self.request_handler_mock.parameters[0]), is_(GOOGLE_URL))
        assert_that(str(self.request_handler_mock.parameters[1]), is_(HTTP_TRACE))

    def test_main_uri_method_shortcut_connect(self):
        main(["--conn", GOOGLE_URL])
        assert_that(str(self.request_handler_mock.parameters[0]), is_(GOOGLE_URL))
        assert_that(str(self.request_handler_mock.parameters[1]), is_(HTTP_CONNECT))


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(CuriMainTest)

if __name__ == '__main__':
    unittest.main()
