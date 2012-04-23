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
