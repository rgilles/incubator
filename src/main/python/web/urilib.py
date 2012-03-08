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
from http.client import HTTPConnection
from urllib.parse import urlsplit, SplitResult
from .assertion import iterable, assert_that_argument_type_is
from web import HTTP_GET as GET, HTTP_METHODS, HTTP_PUT as PUT, HTTP_DELETE as DELETE, HTTP_POST as POST\
, HTTP_HEAD as HEAD, HTTP_OPTIONS as OPTIONS, HTTP_TRACE as TRACE, HTTP_CONNECT as CONNECT, FRAGMENT_SEPARATOR, SEGMENT_SEPARATOR, QUERY_SEPARATOR

EMPTY_PATH = ""
ROOT_PATH = "/"
EMPTY_SEGMENT = EMPTY_PATH
EMPTY_SEGMENTS = ()

def _is_supported_method(method):
    """
    Test if the given method name is part of web.HTTP_METHODS.
    """
    return method in HTTP_METHODS

def _fail_if_not_supported(http_method):
        """
        Throws an UnsupportedMethodError if the given method name is not supported.
        @see _is_supported_method
        """
        if not _is_supported_method(http_method):
            raise UnsupportedMethodError(http_method)

class UnsupportedMethodError (Exception):
    """
    This error is raised when the method does not exist
    in the supported http method
    @see web.HTTP_METHODS
    """
    def __init__(self, bad_method):
        super().__init__(bad_method)
        self.unsupported_method = bad_method
    @property
    def message(self):
        return "unsupported method: {0}".format(self.unsupported_method)

def valid_segment(segment):
    """
    Returns True< if the specified segment would be
    a valid path segment of a URI; False otherwise.

    A valid path segment must be non-null and not contain any of the
    following characters: / ? #

    @param segment the not null segment string to validate.
    """
    return segment is not None and SEGMENT_SEPARATOR not in segment and QUERY_SEPARATOR not in segment and FRAGMENT_SEPARATOR not in segment

def valid_segments(segments):
    """
    Returns True if the specified segments would be
    a valid path segment list of a URI; False otherwise.

    A valid path segment list must be non-null and contain only path
    segments that are valid according to valid_segment method.

    Valid segments parameters are:
    a list:   ['segment1', 'segment2', ...]
    a tuple:  ('segment1', 'segment2', ...)
    a string: 'segment1/segment2/...'
    """
    if isinstance(segments, str) or not iterable(segments):
        return False

    for segment in segments:
        if not valid_segment(segment):
            return False
    return True

def _is_absolute_path(segments):
    return len(segments) > 1 and segments[0] == EMPTY_SEGMENT

def _convert_to_segment(path, trim_root_segment = True):
    assert_that_argument_type_is(path, (str,tuple),"path")
    result = None
    if isinstance(path, str):
        if len(path) < 1 or path == ROOT_PATH:
            result = EMPTY_SEGMENTS
        else :
            result = path.split(SEGMENT_SEPARATOR)

    if trim_root_segment and _is_absolute_path(result):
        result = tuple(result[1:len(result)])

    return result

class URI(object):
    """
    URI
    """
    __slots__ = '__uri', '__structure', '__http_handler'

    def __init__(self, uri, http_handler):
        """
        URI constructor
        """
        self.__uri = uri
        self.__structure = urlsplit(uri)
        self.__http_handler = http_handler

    def __str__(self):
        return self.__uri

    @property
    def scheme(self):
        """
        URI scheme specifier.
        If not present returns an empty string.
        """
        return self.__structure.scheme
    @property
    def authority(self):
        """
        Network location part also known as the authority of
        hierarchical URI. If not present returns an empty string.
        The authority component of a hierarchical URI is, if
        specified, either server-based or registry-based.
        A server-based authority parses according to the familiar syntax:
        [user-info@]host[:port]
        where the characters @ and : stand for themselves. Nearly all
        URI schemes currently in use are server-based.
        An authority component that does not parse in this way
        is considered to be registry-based.
        """
        return self.__structure.netloc
    @property
    def path(self):
        """
        If this is a hierarchical URI with a path, returns a string
        representation of the path; an empty string otherwise.  The path
        consists of a leading segment separator character (a slash), if the
        path is absolute, followed by the slash-separated path segments.
        """
        return self.__structure.path
    @property
    def query(self):
        """
        If this is a hierarchical URI with a query component, returns it;
        an empty string otherwise.
        """
        return self.__structure.query
    @property
    def fragment(self):
        """
        If this URI has a fragment component, returns it; an empty string
        otherwise.
        """
        return self.__structure.fragment
    @property
    def username(self):
        return self.__structure.username
    @property
    def password(self):
        return self.__structure.password
    @property
    def hostname(self):
        return self.__structure.hostname
    @property
    def port(self):
        return self.__structure.port

    @property
    def segments(self):
        """
        If this is a hierarchical URI with a path, returns an array containing
        the segments of the path; an empty array otherwise. The leading separator
        in an absolute path is not represented in this array, but a trailing
        separator is represented by an empty-string segment as the final element.
        """
        return _convert_to_segment(self.path)

    def GET(self, headers = None, body = None):
        self.call(GET, headers, body)
    
    def PUT(self, headers = None, body = None):
        self.call(PUT, headers, body)
    
    def POST(self, headers = None, body = None):
        self.call(POST, headers, body)

    def DELETE(self, headers = None, body = None):
        self.call(DELETE, headers, body)

    def HEAD(self, headers = None, body = None):
        self.call(HEAD, headers, body)
    
    def OPTIONS(self, headers = None, body = None):
        self.call(OPTIONS, headers, body)

    def TRACE(self, headers = None, body = None):
        self.call(TRACE, headers, body)

    def CONNECT(self, headers = None, body = None):
        self.call(CONNECT, headers, body)

    def call(self, method = GET, headers = None, body = None):
        _fail_if_not_supported(method)
        self.__http_handler.call(self, method, headers, body)

    def append_segment(self, segment):
        """
        Returns the URI formed by appending the specified segment on to the end
        of the path of this URI, if hierarchical; this URI unchanged,
        otherwise.  If this URI has an authority and/or device, but no path,
        the segment becomes the first under the root in an absolute path.

        @exception AssertionError if segment is not a valid segment according
                                  to valid_segment method.
        """
        if not valid_segment(segment):
            raise AssertionError("{0} is an invalid segment it must be not null string and not contain any of the following characters: '/' '?' '#'".format(str(segment)))
        return self.append_segments((segment,))

    def append_segments(self, segments):
        """
        Returns the URI formed by appending the specified segments on to the
        end of the path of this URI, if hierarchical; this URI unchanged,
        otherwise.  If this URI has an authority and/or device, but no path,
        the segments are made to form an absolute path.

        @param segments a list or tuple of non-null strings, each representing one
                        segment of the path. Or a string representing a path.
                        If desired, a trailing separator should be represented
                        by an empty-string segment as the last element of the
                        array.

        raise AssertionError if segments is not a valid segments list or tuple
                             or string according to valid_segments method.
        """
        if isinstance(segments, str):
            segments = segments.split(SEGMENT_SEPARATOR)

        return self.append_path(self.segments + tuple(segments))

    def create_root_uri_from(self):
        return self.append_path(ROOT_PATH)

    def trim_segments(self, nb):
        """
        Returns the URI formed by trimming the specified number of segments
        (including empty segments, such as one representing a trailing
        separator) from the end of the path of this URI, if hierarchical;
        otherwise, this URI is returned unchanged.

        Note that if all segments are trimmed from an absolute path, the
        root absolute path remains.

        @param nb the number of segments to be trimmed in the returned URI.  If
                  less than 1, this URI is returned unchanged; if equal to or greater
                  than the number of segments in this URI's path, all segments are
                  trimmed.
        """
        if nb < 1:
            return self
        #split path
        segments = self.segments
        #return self if there is no segments to trim
        if segments is EMPTY_SEGMENTS:
            return self
        if len(segments) <= nb:
            return self.create_root_uri_from()
        else:
            return self.append_path(segments[0:len(segments) - nb])


    def append_path(self, path):
        """
        Returns the URI formed by appending the specified path by replacing
        the path of this URI, if hierarchical; this URI unchanged,
        otherwise.  If this URI has an authority and/or device, but no path,
        the segment becomes the first under the root in an absolute path.

        @param path the path of the new URI. It can be of type string or tuple or list or iterable string

        @exception AssertionError if path is not a valid segment according
                                  to valid_segment method.
        """

        segments = path
        if isinstance(path, str):
            segments = _convert_to_segment(path)

        if not valid_segments(segments):
            raise AssertionError("invalid segments: {0}".format(str(segments)))

        path = SEGMENT_SEPARATOR.join(segments) if _is_absolute_path(segments) else SEGMENT_SEPARATOR.join(("", ) + segments)

        return _create_uri_from_elements(self.scheme, self.authority, path, self.query, self.fragment, self.__http_handler)

    def trim_path(self):
        """
        If this URI has a not empty path, returns the URI
        formed by removing it; this URI unchanged, otherwise.
        """
        if len(self.path) > 0:
            return self.append_path(EMPTY_PATH)
        else:
            return self


    def valid_query(self, query):
        """
        Returns True if the specified query would be
        valid as the query component of a URI; False otherwise.

        A valid query may be null or contain any characters except for #
        """
        return FRAGMENT_SEPARATOR not in str(query)

    def append_query(self, query, separator = "&"):
        """
        Returns the URI formed from this URI and the given query.

        raise AssertionError if query is not a valid query (portion) according
        to valid_query method.

        @param query a not null query portion. It can be of type string or
                     tuple of tuple as ((param1, value1), (param2, value2)).

        @return the URI formed from this URI and the given query.
        """
        if query is not None and not isinstance(query, (str, tuple)):
            raise AssertionError("{0} must be a string or a tuple of tuple like ((param1, value1),(param2, value2))".format(str(query)))
        # create the string representation of the query
        str_query = ""
        if isinstance(query, str):
            str_query = query
        if isinstance(query, tuple):
            nb_params = len(query)
            for index in range(nb_params):
                key, value = query[index]
                str_query = "{0}{1}={2}{3}".format(str_query, key, value, separator if index + 1 < nb_params else "")

        if not self.valid_query(str_query):
            raise AssertionError("{0} is not a valid query".format(str(query)))
        return _create_uri_from_elements(self.scheme, self.authority, self.path, str_query, self.fragment, self.__http_handler)

    def trim_query(self):
        """
        If this URI has a not empty query, returns the URI
        formed by removing it; this URI unchanged, otherwise.
        """
        if len(self.query) > 0:
            return _create_uri_from_elements(self.scheme, self.authority, self.path, None, self.fragment, self.__http_handler)
        else:
            return self

    def append_fragment(self, fragment):
        """
        Returns the URI formed from this URI and the given fragment.
        """
        return _create_uri_from_elements(self.scheme, self.authority, self.path, self.query, fragment, self.__http_handler)

    def trim_fragment(self):
        """
        If this URI has a non-null fragment, returns the URI
        formed by removing it; this URI unchanged, otherwise.
        """
        if len(self.fragment) > 0:
            return _create_uri_from_elements(self.scheme, self.authority, self.path, self.query, None, self.__http_handler)
        else:
            return self


def _create_uri_from_elements(scheme, authority, path, query, fragment, http_handler):
    return URI(SplitResult(scheme, authority, path, query, fragment).geturl(), http_handler)

class Message(object):
    def __init__(self, headers, body):
        self.headers = headers
        self.body = body

#class Response (_Response):
class Response(Message):
#    __slots__ = ()
    def __init__(self, headers, body, status_code, reason_phrase, http_version):
        super().__init__(headers, body)
        self.status_code = status_code
        self.reason_phrase = reason_phrase
        self.http_version = http_version

class Request(Message):
    def __init__(self, headers, body, method, request_uri, http_version):
        super().__init__(headers, body)
        self.method = method
        self.request_uri = request_uri
        self.http_version = http_version

class AbstractRequestHandler(object):
    def call(self, uri, method = GET, headers = None, body = None):
        pass

class HttpClientHandler(AbstractRequestHandler):

    connections = {}

    def as_absolute_path(self, uri):
        result = uri.path
        result = "{0}?{1}".format(result, uri.query) if uri.query else result
        result = "{0}#{1}".format(result, uri.fragment) if uri.fragment else result
        return result

    def call(self, uri, method = GET, headers = None, body = None):
        authority = uri.authority
        connection = self.connections.get(authority)
        if not connection:
            connection = self.connections.setdefault(HTTPConnection(authority))
        connection.request(method, self.as_absolute_path(uri), body, headers)
        response = connection.getresponse()
        result = Response(response.headers, response.read(), response.status, response.reason, response.version)
        return result
