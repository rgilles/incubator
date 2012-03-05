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
from web import uri


class URITest(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_scheme(self):
        google = uri("http://www.google.com")
        self.assertEqual(google.scheme, "http")
        
        
    def test_authority(self):
        google = uri("http://www.google.com")
        self.assertEqual(google.authority, "www.google.com")

    def test_user_info(self):
        google = uri("http://romain.gilles:tutu@www.google.com")
        self.assertEqual(google.authority, "romain.gilles:tutu@www.google.com")
        self.assertEqual(google.username, "romain.gilles")
        self.assertEqual(google.password, "tutu")

    def test_uri_elements(self):
        google = uri("http://romain.gilles:tutu@www.google.com:8080/apath/aparam1;aparam2/subpath?q=myquery#afragment")
        self.assertEqual(google.authority, "romain.gilles:tutu@www.google.com:8080")
        self.assertEqual(google.username, "romain.gilles")
        self.assertEqual(google.password, "tutu")
        self.assertEqual(google.port, 8080)
        self.assertEqual(google.path, '/apath/aparam1;aparam2/subpath')
        self.assertEqual(google.query, 'q=myquery')
        self.assertEqual(google.fragment, 'afragment')

    def test_append_fragment(self):
        google = uri("http://www.google.com")
        google = google.append_fragment("fragment")
        self.assertEqual("http://www.google.com#fragment",str(google))
        google = google.append_fragment("fragment2")
        self.assertEqual("http://www.google.com#fragment2",str(google))
        google = google.append_fragment(None)
        self.assertEqual("http://www.google.com",str(google))
        google = google.append_fragment("")
        self.assertEqual("http://www.google.com",str(google))

    def test_append_query(self):
        google = uri("http://www.google.com")
        google = google.append_query("param1=value1&param2=value2") #string approach
        self.assertEqual("http://www.google.com?param1=value1&param2=value2",str(google))

        google = google.append_query((("param1","value1"),("param2","value2"))) #list key value tuple approach for ordered result
        self.assertEqual("http://www.google.com?param1=value1&param2=value2",str(google))

        google = google.append_query(None) #list key value tuple approach for ordered result
        self.assertEqual("http://www.google.com",str(google))


    def test_append_segments_list(self):
        google = uri("http://www.google.com")
        google = google.append_segments(["segment1", "segment2"])
        self.assertEqual("http://www.google.com/segment1/segment2",str(google))

    def test_append_segments_tuple(self):
        google = uri("http://www.google.com")
        google = google.append_segments(("segment1", "segment2"))
        self.assertEqual("http://www.google.com/segment1/segment2",str(google))

    def test_append_segments_string(self):
        google = uri("http://www.google.com")
        google = google.append_segments("segment1/segment2") #string approach
        self.assertEqual("http://www.google.com/segment1/segment2",str(google))

    def test_append_segments_with_trailing_separator(self):
        google = uri("http://www.google.com")
        google = google.append_segments(("segment1", "segment2", ""))
        self.assertEqual("http://www.google.com/segment1/segment2/",str(google))

    def test_append_segment(self):
        google = uri("http://www.google.com")
        google = google.append_segment("segment1")
        self.assertEqual("http://www.google.com/segment1",str(google))

        google = google.append_segment("segment2") #string approach
        self.assertEqual("http://www.google.com/segment1/segment2",str(google))

    def test_append_segment_with_segment_separator(self):
        self._segment_test("segment1/")
        self._segment_test("/segment2")

    def test_append_segment_with_query_separator(self):
        self._segment_test("?segment1")
        self._segment_test("segment2?")

    def test_append_segment_with_fragment_separator(self):
        self._segment_test("#segment1")
        self._segment_test("segment2#")

    def _segment_test(self, segment):
        google = uri("http://www.google.com")
        try:
            google.append_segment(segment)
        except AssertionError:
            pass
        else:
            self.fail("{0} is an invalid segment then a exception must be raised".format(str(segment)))

    def test_trim_query_on_no_query(self):
        """
        Test trim_query method on a URI that does not contain any query portion.
        The expected result is the original instance URI.
        """
        google = uri("http://www.google.com")
        google_result = google.trim_query()
        self.assertEqual(google_result, google)

    def test_trim_query_on_existing_query(self):
        """
        Test trim_query method on a URI that contains a query portion.
        The expected result a new instance URI.
        """
        google = uri("http://www.google.com?param1=value1&param2=value2")
        trim_result = google.trim_query()
        self.assertNotEqual(trim_result, google)
        self.assertEqual("http://www.google.com", str(trim_result))

    def test_trim_query_on_existing_query_with_path(self):
        """
        Test trim_query method on a URI that contains a query portion and a path portion.
        The expected result is a new URI with the path.
        """
        google = uri("http://www.google.com/segment1/segment2?param1=value1&param2=value2")
        trim_result = google.trim_query()
        self.assertNotEqual(trim_result, google)
        self.assertEqual("http://www.google.com/segment1/segment2", str(trim_result))

    def test_trim_query_on_existing_query_with_fragment(self):
        """
        Test trim_query method on a URI that contains a query portion and a fragment portion.
        The expected result is a new URI with the fragment.
        """
        google = uri("http://www.google.com?param1=value1&param2=value2#fragment")
        trim_result = google.trim_query()
        self.assertNotEqual(trim_result, google)
        self.assertEqual("http://www.google.com#fragment", str(trim_result))

    def test_trim_fragment_on_no_fragment(self):
        """
        Test trim_fragment method on a URI that does not contain any fragment portion.
        The expected result is the original instance URI.
        """
        google = uri("http://www.google.com")
        google_result = google.trim_fragment()
        self.assertEqual(google_result, google)

    def test_trim_fragment_on_existing_fragment(self):
        """
        Test trim_fragment method on a URI that contains a fragment portion.
        The expected result a new instance URI.
        """
        google = uri("http://www.google.com#fragment")
        trim_result = google.trim_fragment()
        self.assertNotEqual(trim_result, google)
        self.assertEqual("http://www.google.com", str(trim_result))

    def test_trim_fragment_on_existing_fragment_with_path(self):
        """
        Test trim_fragment method on a URI that contains a fragment portion and a path portion.
        The expected result is a new URI with the path.
        """
        google = uri("http://www.google.com/segment1/segment2#fragment")
        trim_result = google.trim_fragment()
        self.assertNotEqual(trim_result, google)
        self.assertEqual("http://www.google.com/segment1/segment2", str(trim_result))

    def test_trim_fragment_on_existing_fragment_with_query(self):
        """
        Test trim_fragment method on a URI that contains a fragment portion and a query portion.
        The expected result is a new URI with the fragment.
        """
        google = uri("http://www.google.com?param1=value1&param2=value2#fragment")
        trim_result = google.trim_fragment()
        self.assertNotEqual(trim_result, google)
        self.assertEqual("http://www.google.com?param1=value1&param2=value2", str(trim_result))

    def test_trim_path_on_no_path(self):
        """
        Test trim_path method on a URI that does not contain any path portion.
        The expected result is the original instance URI.
        """
        google = uri("http://www.google.com")
        google_result = google.trim_path()
        self.assertEqual(google_result, google)

    def test_trim_path_on_existing_path(self):
        """
        Test trim_path method on a URI that contains a path portion.
        The expected result a new instance URI.
        """
        google = uri("http://www.google.com/segment1/segment2")
        trim_result = google.trim_path()
        self.assertNotEqual(trim_result, google)
        self.assertEqual("http://www.google.com", str(trim_result))

    def test_trim_path_on_existing_path_with_fragment(self):
        """
        Test trim_path method on a URI that contains a path portion and a path portion.
        The expected result is a new URI with the path.
        """
        google = uri("http://www.google.com/segment1/segment2#fragment")
        trim_result = google.trim_path()
        self.assertNotEqual(trim_result, google)
        self.assertEqual("http://www.google.com#fragment", str(trim_result))

    def test_trim_path_on_existing_path_with_query(self):
        """
        Test trim_path method on a URI that contains a path portion and a query portion.
        The expected result is a new URI with the path.
        """
        google = uri("http://www.google.com/segment1/segment2?param1=value1&param2=value2")
        trim_result = google.trim_path()
        self.assertNotEqual(trim_result, google)
        self.assertEqual("http://www.google.com?param1=value1&param2=value2", str(trim_result))

if __name__ == "__main__":
#    import sys;sys.argv = ['', 'URITest.test_scheme']
    unittest.main()