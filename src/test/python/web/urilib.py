import unittest
from web import uri


class URITest(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testScheme(self):
        google = uri("http://www.google.com")
        self.assertEqual(google.scheme(), "http")
        
        
    def testAuthority(self):
        google = uri("http://www.google.com")
        self.assertEqual(google.authority(), "www.google.com")
        
    def testUserInfo(self):
        google = uri("http://romain.gilles:tutu@www.google.com")
        self.assertEqual(google.authority(), "romain.gilles:tutu@www.google.com")
        self.assertEqual(google.username(), "romain.gilles")
        self.assertEqual(google.password(), "tutu")

if __name__ == "__main__":
#    import sys;sys.argv = ['', 'URITest.testScheme']
    unittest.main()