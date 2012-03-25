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
VERSION="${version}"
DEFAULT_HTTP_HANDLER = None

HTTP_GET = 'GET'
HTTP_HEAD = 'HEAD'

HTTP_PUT = 'PUT'
HTTP_POST = 'POST'
HTTP_DELETE = 'DELETE'
HTTP_OPTIONS = 'OPTIONS'
HTTP_TRACE = 'TRACE'
HTTP_CONNECT = 'CONNECT'

HTTP_METHODS = HTTP_GET, HTTP_PUT, HTTP_DELETE, HTTP_POST, HTTP_HEAD, HTTP_OPTIONS, HTTP_TRACE

# Separators for parsing a URI string.
SCHEME_SEPARATOR = ":"
AUTHORITY_SEPARATOR = "//"
DEVICE_IDENTIFIER = ":"
SEGMENT_SEPARATOR = "/"
QUERY_SEPARATOR = "?"
FRAGMENT_SEPARATOR = "#"
USER_INFO_SEPARATOR = "@"
PORT_SEPARATOR = ":"

def uri(uri):
    from web.urilib import URI
    return URI(uri)
