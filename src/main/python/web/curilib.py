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
REQUEST_OPTION_DESTINATION = 'request'
REQUEST_OPTION_LONG = '--request'
REQUEST_OPTION_SHORT = '-X'

__author__ = 'romain.gilles'

from web import HTTP_METHODS, HTTP_GET, uri, request, HTTP_PUT, HTTP_POST, HTTP_DELETE, HTTP_HEAD, HTTP_OPTIONS, HTTP_CONNECT, HTTP_TRACE
import argparse

version = '${version}'


def validate_method(method):
    return method in HTTP_METHODS


def _print(response):
    print(str(response))


def main(args):
    parser = argparse.ArgumentParser(description='Process uri to create request.')
    parser.add_argument('--version', action='version', version='%(prog)s {0}'.format(version))
    parser.add_argument('uri', help="the uri where the request will be sent")
    group = parser.add_mutually_exclusive_group()

    group.add_argument(REQUEST_OPTION_SHORT, REQUEST_OPTION_LONG, dest=REQUEST_OPTION_DESTINATION,
                       help="(HTTP) Specifies a custom request method to use when communicating with the HTTP server. The specified request will be used instead of the method otherwise used (which defaults to GET). Read the HTTP 1.1 specification for details and explanations. (Common additional HTTP requests include PUT and DELETE, but related technologies like WebDAV offers PROPFIND, COPY, MOVE and more). It can be: {0}".format(
                           ", ".join(HTTP_METHODS)), default=HTTP_GET)
    group.add_argument('-G', '--get', help="Activate the get method", dest=REQUEST_OPTION_DESTINATION,
                       action='store_const', const=HTTP_GET)
    group.add_argument('--put', help="Activate the put method", dest=REQUEST_OPTION_DESTINATION, action='store_const',
                       const=HTTP_PUT)
    group.add_argument('--post', help="Activate the post method", dest=REQUEST_OPTION_DESTINATION, action='store_const',
                       const=HTTP_POST)
    group.add_argument('--del', help="Activate the delete method", dest=REQUEST_OPTION_DESTINATION, action='store_const'
                       , const=HTTP_DELETE)
    group.add_argument('--head', help="Activate the head method", dest=REQUEST_OPTION_DESTINATION, action='store_const',
                       const=HTTP_HEAD)
    group.add_argument('--opts', help="Activate the options method", dest=REQUEST_OPTION_DESTINATION,
                       action='store_const', const=HTTP_OPTIONS)
    group.add_argument('--trace', help="Activate the trace method", dest=REQUEST_OPTION_DESTINATION,
                       action='store_const', const=HTTP_TRACE)
    group.add_argument('--conn', help="Activate the connect method", dest=REQUEST_OPTION_DESTINATION,
                       action='store_const', const=HTTP_CONNECT)
    args = parser.parse_args(args)
    target = uri(args.uri)
    if not validate_method(args.request):
        parser.error("invalid method name: {0}".format(args.request))

    response = request(target, args.request)
    _print(response)
